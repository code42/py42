from py42.services import BaseService
from py42.services.storage._auth import FileArchiveTmpAuth, SecurityArchiveTmpAuth
from py42.services.storage import StorageArchiveService, StorageSecurityDataService


class StorageClient(BaseService):
    def __init__(self, connection):
        super(StorageClient, self).__init__(connection)
        self._archive_client = StorageArchiveService(connection)
        self._security_client = StorageSecurityDataService(connection)

    @property
    def archive(self):
        return self._archive_client

    @property
    def securitydata(self):
        return self._security_client


class StorageClientFactory(object):
    def __init__(self, connection, device_client, connection_manager):
        self._connection = connection
        self._device_client = device_client
        self._connection_manager = connection_manager

    def from_device_guid(self, device_guid, destination_guid=None):
        if destination_guid is None:
            destination_guid = self._auto_select_destination_guid(device_guid)

        auth = FileArchiveTmpAuth(self._connection, u"my", device_guid, destination_guid)
        connection = self._connection_manager.get_storage_connection(auth)
        return StorageClient(connection)

    def from_plan_info(self, plan_uid, destination_guid):
        auth = SecurityArchiveTmpAuth(self._connection, plan_uid, destination_guid)
        connection = self._connection_manager.get_storage_connection(auth)
        return StorageClient(connection)

    def _auto_select_destination_guid(self, device_guid):
        response = self._device_client.get_by_guid(
            device_guid, include_backup_usage=True
        )
        # take the first destination guid we find
        destination_list = response["backupUsage"]
        if not destination_list:
            raise Exception(
                u"No destinations found for device guid: {}".format(device_guid)
            )
        return destination_list[0][u"targetComputerGuid"]
