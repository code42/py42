import py42.util as util
from py42._internal.base_classes import BaseArchiveLocatorFactory
from py42._internal.clients.devices import DeviceClient
from py42._internal.clients.security import SecurityClient, get_normalized_security_event_plan_info
from py42._internal.login_providers import C42APILoginTokenProvider, C42APIStorageAuthTokenProvider


class C42AuthorityArchiveLocatorFactory(BaseArchiveLocatorFactory):

    def __init__(self, auth_session, security_client, device_client):
        # type: (object, SecurityClient, DeviceClient) -> C42AuthorityArchiveLocatorFactory
        self._auth_session = auth_session
        self._security_client = security_client
        self._device_client = device_client

    def create_security_archive_locators(self, user_uid, *args, **kwargs):
        plan_dict = get_normalized_security_event_plan_info(self._security_client, user_uid, **kwargs)
        locator_list = []
        for plan, destination_list in plan_dict.items():
            for destination in destination_list:
                locator_list.append(C42APIStorageAuthTokenProvider(self._auth_session, plan,
                                                                   destination["destinationGuid"],
                                                                   node_guid=destination.get("nodeGuid")))
        return locator_list

    def create_backup_archive_locator(self, device_guid, destination_guid=None, *args, **kwargs):
        try:
            if destination_guid is None:
                response = self._device_client.get_device_by_guid(device_guid, include_backup_usage=True, force_sync=True)
                if destination_guid is None:
                    # take the first destination guid we find
                    destination_list = util.get_obj_from_response(response, "backupUsage")
                    if not destination_list:
                        raise Exception("No destinations found for device guid: {0}".format(device_guid))
                    destination_guid = destination_list[0]["targetComputerGuid"]
        except Exception as e:
            message = "An error occurred while trying to determine a destination for device guid: {0}," \
                      " caused by: {1}".format(device_guid, e.message)
            raise Exception(message)

        return C42APILoginTokenProvider(self._auth_session, "my", device_guid, destination_guid)
