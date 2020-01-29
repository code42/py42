import py42.util as util
from py42._internal.base_classes import BaseAuthorityClient


def get_normalized_security_event_plan_info(security_client, user_uid):
    """Returns a dictionary of plan UIDs to their locations.

    Raises:
        HTTPError if no plans are found.

    Note: The data model changed with Code42 6.7.

    Example return value (6.7 and later):

        {"111111111111111111": [{"destinationGuid": "4", "nodeGuid": "41"},
                                {"destinationGuid": "5", "nodeGuid": "51"}],
         "222222222222222222": [{"destinationGuid": "4", "nodeGuid": "41"},
                                {"destinationGuid": "5", "nodeGuid": "51"}]}

    Pre Code42 6.7:

        {"111111111111111111": [{"destinationGuid": "4"},
                                {"destinationGuid": "5"}]}
    """
    # Normally we would just be able to call the SecurityEventLocations endpoint and use what comes back,
    # but due to this endpoint having its format completely change across C42 versions, we need to perform
    # transformations on the response in order to standardize.
    # TODO: once we have proper types this should be refactored to not use so many magical strings
    archive_locations_by_plan = {}
    response = security_client.get_security_event_locations(user_uid)
    if response is not None:
        # Prior to Code42 6.7, the SecurityEventLocation api returned data back in a different format,
        # complete with an array of destinationGuids incorrectly labeled as "storageNodeGuids."
        destination_list = util.get_obj_from_response(response, u"storageNodeGuids")
        if destination_list:
            plan_uid = util.get_obj_from_response(response, u"planUid")
            archive_locations_by_plan = {
                plan_uid: [{u"destinationGuid": destination}] for destination in destination_list
            }
        else:
            destinations = util.get_obj_from_response(
                response, u"securityPlanLocationsByDestination"
            )
            for destination in destinations:
                for node in destination[u"securityPlanLocationsByNode"]:
                    for plan_uid in node[u"securityPlanUids"]:
                        plan_locations = archive_locations_by_plan.get(plan_uid)
                        if plan_locations is None:
                            archive_locations_by_plan[plan_uid] = []
                            plan_locations = archive_locations_by_plan.get(plan_uid)
                        plan_locations.append(
                            {
                                u"destinationGuid": destination[u"destinationGuid"],
                                u"nodeGuid": node[u"nodeGuid"],
                            }
                        )
    return archive_locations_by_plan


class SecurityClient(BaseAuthorityClient):
    def get_security_event_locations(self, user_uid):
        uri = u"/c42api/v3/SecurityEventsLocation"
        params = {u"userUid": user_uid}

        return self._v3_required_session.get(uri, params=params)
