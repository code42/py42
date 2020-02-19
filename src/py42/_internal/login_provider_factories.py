import py42.util as util
from py42._internal.clients.devices import DeviceClient
from py42._internal.clients.security import SecurityClient
from py42._internal.compat import str
from py42._internal.login_providers import (
    C42APILoginTokenProvider,
    C42APIStorageAuthTokenProvider,
    FileEventLoginProvider,
    KeyValueStoreLoginProvider,
    AlertLoginProvider,
    EmployeeCaseManagementLoginProvider,
)


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
                response = self._device_client.get_device_by_guid(
                    device_guid, include_backup_usage=True
                )
                if destination_guid is None:
                    # take the first destination guid we find
                    destination_list = util.get_obj_from_response(response, u"backupUsage")
                    if not destination_list:
                        raise Exception(
                            u"No destinations found for device guid: {0}".format(device_guid)
                        )
                    destination_guid = destination_list[0][u"targetComputerGuid"]
        except Exception as ex:
            message = (
                u"An error occurred while trying to determine a destination for device guid: {0},"
                u" caused by: {1}".format(device_guid, str(ex))
            )
            raise Exception(message)

        return C42APILoginTokenProvider(self._auth_session, u"my", device_guid, destination_guid)


class FileEventLoginProviderFactory(object):
    def __init__(self, auth_session):
        self._auth_session = auth_session

    def create_file_event_login_provider(self):
        return FileEventLoginProvider(self._auth_session)


class KeyValueStoreLocatorFactory(object):
    def __init__(self, auth_session):
        self._auth_session = auth_session

    def create_key_value_store_locator(self):
        return KeyValueStoreLoginProvider(self._auth_session)


class AlertLoginProviderFactory(object):
    def __init__(self, auth_session, key_value_store_client_factory):
        self._auth_session = auth_session
        self._key_value_store_client_factory = key_value_store_client_factory

    def create_alert_login_provider(self):
        key_value_store_client = self._key_value_store_client_factory.get_key_value_store_client()
        return AlertLoginProvider(self._auth_session, key_value_store_client)


class EmployeeCaseManagementLoginProviderFactory(object):
    def __init__(self, auth_session, key_value_store_client_factory):
        self._auth_session = auth_session
        self._key_value_store_client_factory = key_value_store_client_factory

    def create_ecm_login_provider(self):
        key_value_store_client = self._key_value_store_client_factory.get_key_value_store_client()
        return EmployeeCaseManagementLoginProvider(self._auth_session, key_value_store_client)
