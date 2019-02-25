from random import shuffle
from urlparse import urlparse, parse_qs
from code42.sdk import util


class CustomSecurityEventFetcherHandlers(object):
    @staticmethod
    def should_process_user(user):
        return True

    @staticmethod
    def get_starting_cursor_position(plan_uid):
        return None

    @staticmethod
    def record_cursor_position(cursor, plan_uid, user):
        pass

    @staticmethod
    def process_security_event_response(response, user):
        pass


class SecurityEventFetcher(object):
    def __init__(self, sdk_client, min_timestamp=None, custom_handlers=None):
        self._sdk = sdk_client
        self._min_timestamp = min_timestamp
        self._handlers = custom_handlers or CustomSecurityEventFetcherHandlers()
        self._guid_to_url_map = {}

    def start(self):
        self._sdk.authority.administration.users.for_each_user(then=self.get_user_locations)
        self._sdk.authority.wait()
        self._sdk.storage.wait_all()

    def get_user_locations(self, user):
        if self._handlers.should_process_user(user):
            def callback(response):
                self.handle_security_event_location_response(response, user)
            self._sdk.authority.securitytools.get_security_event_locations(
                                                                 str(user["userUid"]),
                                                                 then=callback)

    def handle_security_event_location_response(self, response, user):
        # Prior to Code42 6.7, the SecurityEventLocation api returned data back in a completely different format,
        # complete with and array of destinationGuids incorrectly labeled as "storageNodeGuids."
        try:
            if response.status_code != 404 and response.content:
                plan_dict = {}
                destination_list = util.get_obj_from_response(response, "storageNodeGuids")
                if destination_list:
                    plan_uid = util.get_obj_from_response(response, "planUid")
                    plan_dict[plan_uid] = []
                    for destination in destination_list:
                        plan_dict[plan_uid].append({"destinationGuid": destination, "planUid": plan_uid})
                else:
                    location_list = util.get_obj_from_response(response, "securityPlanLocationsByDestination")
                    plans = [{"planUid": z, "destinationGuid": x["destinationGuid"], "nodeGuid": y["nodeGuid"]}
                             for x in location_list
                             for y in x["securityPlanLocationsByNode"]
                             for z in y["securityPlanUids"]]
                    for p in plans:
                        x = plan_dict.get(p["planUid"])
                        if x is None:
                            plan_dict[p["planUid"]] = []
                            x = plan_dict.get(p["planUid"])
                        x.append(
                            {"destinationGuid": p["destinationGuid"], "nodeGuid": p["nodeGuid"],
                             "planUid": p["planUid"]})
                for i in plan_dict:
                    self.locate_storage_client(plan_dict[i], user)
        except Exception as e:
            message = "An error occurred in SecurityEventFetcher while handling security event location responses"
            raise Exception(message + ", caused by: " + e.message)

    def locate_storage_client(self, remaining_locations, user):
        try:
            if remaining_locations is not None and len(remaining_locations) > 0:
                shuffle(remaining_locations)
                plan_location = remaining_locations[0]
                node_guid = plan_location.get("nodeGuid", None)
                storage_url = None
                if node_guid is not None:
                    storage_url = self._guid_to_url_map.get(node_guid, None)

                if not storage_url:
                    plan_uid = plan_location["planUid"]
                    destination_guid = plan_location["destinationGuid"]
                    client = self._sdk.storage.fetch_client_via_plan_info(plan_uid, destination_guid)
                    storage_url = client.host_address

                remaining_locations.remove(plan_location)
                plan_uid = plan_location["planUid"]
                self.get_security_events(storage_url, plan_uid, user, remaining_locations=remaining_locations,
                                         node_guid=node_guid)
        except Exception as e:
            message = "An error occurred in SecurityEventFetcher while locating storage clients"
            raise Exception(message + ", caused by: " + e.message)

    def get_security_events(self, storage_url, plan_uid, user, cursor=None,
                            remaining_locations=None, node_guid=None):
        try:
            # if the chosen destination fails we will re-call this function with the failed destination removed from the
            # input list.
            if node_guid is not None not in self._guid_to_url_map:
                self._guid_to_url_map.update({node_guid: storage_url})

            storage_client = self._sdk.storage.using(storage_url).securitytools
            min_timestamp = None

            if cursor is None:
                cursor = self._handlers.get_starting_cursor_position(plan_uid)
                if cursor is None:
                    min_timestamp = self._min_timestamp

            def callback(response):
                self.handle_security_event_response(response, user)

            storage_client.get_security_detection_events(plan_uid, cursor=cursor,
                                                         include_files=True,
                                                         min_timestamp=min_timestamp,
                                                         then=callback,
                                                         catch=lambda(ex):
                                                         self.locate_storage_client(remaining_locations, user))
        except Exception as e:
            message = "An error occurred in SecurityEventFetcher while getting security events"
            raise Exception(message + ", caused by: " + e.message)

    def handle_security_event_response(self, response, callback_user):
        try:
            if response.content:
                self._handlers.process_security_event_response(response, callback_user)
                response_cursor = util.get_obj_from_response(response, "cursor")
                if response_cursor:
                    parsed_url = urlparse(response.request.url)
                    storage_url = parsed_url.scheme + "://" + parsed_url.netloc
                    plan_uid = parse_qs(parsed_url.query).get("planUid", None)
                    self._handlers.record_cursor_position(plan_uid, callback_user, response_cursor)
                    self.get_security_events(storage_url, plan_uid, callback_user, cursor=response_cursor)
        except Exception as e:
            message = "An error occurred in SecurityEventFetcher while handling security event responses"
            raise Exception(message + ", caused by: " + e.message)
