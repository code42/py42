import json
from threading import Lock

from py42._internal.client_factories import (
    FileEventClientFactory,
    StorageClientFactory,
    AlertClientFactory,
)
from py42._internal.clients.security import SecurityClient
import py42.util as util


class SecurityModule(object):
    def __init__(
        self,
        security_client,
        storage_client_factory,
        file_event_client_factory,
        alert_client_factory,
    ):
        # type: (SecurityClient, StorageClientFactory, FileEventClientFactory, AlertClientFactory) -> None
        self._security_client = security_client
        self._storage_client_factory = storage_client_factory
        self._file_event_client_factory = file_event_client_factory
        self._alert_client_factory = alert_client_factory
        self._file_event_client = None
        self._alert_client = None
        self._client_cache = {}
        self._client_cache_lock = Lock()

    @property
    def alerts(self):
        if self._alert_client is None:
            self._alert_client = self._alert_client_factory.get_alert_client()
        return self._alert_client

    def get_security_plan_storage_info_list(self, user_uid):
        locations = None
        try:
            response = self._security_client.get_security_event_locations(user_uid)
            locations = util.get_obj_from_response(response, u"securityPlanLocationsByDestination")
        except Exception:
            # TODO: only pass if the exception is caused by a 404
            pass

        if locations:
            plan_destination_map = _get_plan_destination_map(locations)
            selected_plan_infos = self._get_plan_storage_infos(plan_destination_map)
            if not selected_plan_infos:
                raise Exception(
                    u"Could not establish a connection to retrieve security events for user {0}".format(
                        user_uid
                    )
                )

            return selected_plan_infos

    def get_plan_security_events(
        self,
        plan_storage_info,
        cursor=None,
        include_files=True,
        event_types=None,
        min_timestamp=None,
        max_timestamp=None,
    ):
        return self._get_security_detection_events(
            plan_storage_info, cursor, include_files, event_types, min_timestamp, max_timestamp
        )

    def get_user_security_events(
        self,
        user_uid,
        cursor=None,
        include_files=True,
        event_types=None,
        min_timestamp=None,
        max_timestamp=None,
    ):
        security_plan_storage_infos = self.get_security_plan_storage_info_list(user_uid)
        return self._get_security_detection_events(
            security_plan_storage_infos,
            cursor,
            include_files,
            event_types,
            min_timestamp,
            max_timestamp,
        )

    def search_file_events(self, query):
        """Searches for file events

        Args:
            query: raw JSON query or FileEventQuery object. See https://support.code42.com/Administrator/Cloud/Monitoring_and_managing/Forensic_File_Search_API

        Returns:
            list of file events as JSON
        """
        if self._file_event_client is None:
            self._file_event_client = self._file_event_client_factory.get_file_event_client()
        return self._file_event_client.search_file_events(query)

    def _get_plan_storage_infos(self, plan_destination_map):
        plan_infos = []
        for plan_uid in plan_destination_map:
            destinations = plan_destination_map[plan_uid]
            storage_info = self._get_storage_info_for_plan(plan_uid, destinations)
            if storage_info:
                plan_infos.append(storage_info)

        return plan_infos

    def _get_storage_info_for_plan(self, plan_uid, destinations):
        for destination in destinations:
            # try to connect to every storage node for this plan until one works
            plan_storage_info = self._get_storage_info_for_plan_destination(plan_uid, destination)
            if plan_storage_info:
                return plan_storage_info

    def _get_storage_info_for_plan_destination(self, plan_uid, destination):
        try:
            destination_guid = destination[u"destinationGuid"]
            node_guid = destination[u"nodeGuid"]
            plan_storage_info = PlanStorageInfo(plan_uid, destination_guid, node_guid)
            self._try_get_security_detection_event_client(plan_storage_info)
            return plan_storage_info
        except Exception:
            pass

    def _try_get_security_detection_event_client(self, plan_storage_info):
        # check if we have already created and stored this client
        client = self._client_cache.get(plan_storage_info.node_guid)

        # otherwise, create it
        if client is None:
            client = self._storage_client_factory.get_storage_client_from_plan_uid(
                plan_storage_info.plan_uid, plan_storage_info.destination_guid
            ).security

            # store this client via its guid so that we don't have to call StorageAuthToken
            # just to determine what storage client to use
            with self._client_cache_lock:
                self._client_cache.update({plan_storage_info.node_guid: client})

        return client

    def _get_security_detection_events(
        self, plan_storage_infos, cursor, include_files, event_types, min_timestamp, max_timestamp
    ):
        if type(plan_storage_infos) is not list:
            plan_storage_infos = [plan_storage_infos]

        # get the storage node client for each plan
        for plan_storage_info in plan_storage_infos:
            client = self._try_get_security_detection_event_client(plan_storage_info)
            started = False

            # get all pages of events for this plan
            while cursor or not started:
                started = True
                response = client.get_security_detection_events_for_plan(
                    plan_storage_info.plan_uid,
                    cursor=cursor,
                    include_files=include_files,
                    event_types=event_types,
                    min_timestamp=min_timestamp,
                    max_timestamp=max_timestamp,
                )

                if response.text:
                    cursor = json.loads(response.text)[u"data"].get(u"cursor")
                    # if there are no results, we don't get a cursor and have reached the end
                    if cursor:
                        yield response, cursor


def _get_plan_destination_map(locations_list):
    plan_destination_map = {}
    for plans in _get_destinations_in_locations_list(locations_list):
        for plan_uid in plans:
            plan_destination_map[plan_uid] = plans[plan_uid]
    return plan_destination_map


def _get_destinations_in_locations_list(locations_list):
    for destination in locations_list:
        for node in destination[u"securityPlanLocationsByNode"]:
            yield _get_plans_in_node(destination, node)


def _get_plans_in_node(destination, node):
    return {
        plan_uid: [
            {u"destinationGuid": destination[u"destinationGuid"], u"nodeGuid": node[u"nodeGuid"]}
        ]
        for plan_uid in node[u"securityPlanUids"]
    }


class PlanStorageInfo(object):
    def __init__(self, plan_uid, destination_guid, node_guid):
        self._plan_uid = plan_uid
        self._destination_uid = destination_guid
        self._node_guid = node_guid

    @property
    def plan_uid(self):
        return self._plan_uid

    @property
    def destination_guid(self):
        return self._destination_uid

    @property
    def node_guid(self):
        return self._node_guid
