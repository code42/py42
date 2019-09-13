import py42.util as util
from py42._internal.clients.devices import DeviceClient
from py42._internal.clients.security import SecurityClient
from py42._internal.login_providers import C42APILoginTokenProvider, C42APIStorageAuthTokenProvider, \
    FileEventLoginProvider


class ArchiveLocatorFactory(object):

    def __init__(self, auth_session, security_client, device_client):
        # type: (object, SecurityClient, DeviceClient) -> ArchiveLocatorFactory
        self._auth_session = auth_session
        self._security_client = security_client
        self._device_client = device_client

    def create_security_archive_locator(self, plan_uid, destination_guid):
        return C42APIStorageAuthTokenProvider(self._auth_session, plan_uid, destination_guid)

    def create_backup_archive_locator(self, device_guid, destination_guid=None):
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


class FileEventLoginProviderFactory(object):

    def __init__(self, auth_session):
        self._auth_session = auth_session

    def create_file_event_login_provider(self):
        return FileEventLoginProvider(self._auth_session)
