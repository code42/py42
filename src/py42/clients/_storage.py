from py42.services import BaseService
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
    def __init__(self, storage_session_manager, storage_auth_factory):
        self._storage_session_manager = storage_session_manager
        self._storage_auth_factory = storage_auth_factory

    def from_device_guid(self, device_guid, destination_guid=None):
        auth = self._storage_auth_factory.create_backup_archive_locator(
            device_guid, destination_guid
        )
        connection = self._storage_session_manager.get_storage_connection(auth)
        return StorageClient(connection)

    def from_plan_info(self, plan_uid, destination_guid):
        auth = self._storage_auth_factory.create_security_archive_locator(
            plan_uid, destination_guid
        )
        connection = self._storage_session_manager.get_storage_connection(auth)
        return StorageClient(connection)
