from py42._internal.clients.security import SecurityClient, get_normalized_security_event_plan_info
from py42._internal.clients.devices import DeviceClient
from py42._internal.login_providers import C42APIStorageAuthTokenProvider, C42APILoginTokenProvider
from py42._internal.base_classes import BaseArchiveLocatorFactory
import py42.util as util


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

    def create_backup_archive_locator(self, device_guid, user_id=None, destination_guid=None, *args, **kwargs):
        if user_id is None or destination_guid is None:
            response = self._device_client.get_device_by_guid(device_guid, include_backup_usage=True, force_sync=True)
            if destination_guid is None:
                # take the first destination guid we find
                destination_list = util.get_obj_from_response(response, "backupUsage")
                destination_guid = destination_list[0]["targetComputerGuid"]
            if user_id is None:
                # use the userId that we found to be the owner of the device
                user_id = util.get_obj_from_response(response, "userId")

        return C42APILoginTokenProvider(self._auth_session, user_id, device_guid, destination_guid)
