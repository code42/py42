from py42._internal.base_classes import BaseAuthorityClient
import py42.util as util


def get_normalized_security_event_plan_info(security_client, user_uid, **kwargs):
    # Raises HTTPError if no plans are found.
    # Normally we would just be able to call the SecurityEventLocations endpoint and use what comes back,
    # but due to this endpoint having its format completely change across C42 versions, we need to perform
    # transformations on the response in order to standardize.
    # TODO: once we have proper types this should be refactored to not use so many magical strings
    response = security_client.get_security_event_locations(user_uid, force_sync=True, **kwargs)
    if response is not None:
        # Prior to Code42 6.7, the SecurityEventLocation api returned data back in a different format,
        # complete with an array of destinationGuids incorrectly labeled as "storageNodeGuids."
        destination_list = util.get_obj_from_response(response, "storageNodeGuids")
        if destination_list:
            plan_uid = util.get_obj_from_response(response, "planUid")
            plan_dict = {plan_uid: [{"destinationGuid": destination}] for destination in destination_list}
        else:
            location_list = util.get_obj_from_response(response, "securityPlanLocationsByDestination")
            plan_dict = {z: [{"destinationGuid": x["destinationGuid"], "nodeGuid": y["nodeGuid"]}]
                         for x in location_list
                         for y in x["securityPlanLocationsByNode"]
                         for z in y["securityPlanUids"]}

        return plan_dict
    return {}


class SecurityClient(BaseAuthorityClient):

    def get_security_event_locations(self, user_uid, **kwargs):
        uri = "/c42api/v3/SecurityEventsLocation"
        params = {"userUid": user_uid}

        return self._v3_required_session.get(uri, params=params, **kwargs)
