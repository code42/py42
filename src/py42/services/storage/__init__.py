from py42.services import BaseClient
from py42.services.storage.archive import StorageArchiveClient
from py42.services.storage.securitydata import StorageSecurityClient


class StorageClient(BaseClient):
    def __init__(self, connection):
        super(StorageClient, self).__init__(connection)
        self._archive_client = StorageArchiveClient(connection)
        self._security_client = StorageSecurityClient(connection)

    @property
    def archive(self):
        return self._archive_client

    @property
    def securitydata(self):
        return self._security_client


class StorageClientFactory(object):
    def __init__(self, storage_session_manager, token_provider_factory):
        self._storage_session_manager = storage_session_manager
        self._token_provider_factory = token_provider_factory

    def from_device_guid(self, device_guid, destination_guid=None):
        token_provider = self._token_provider_factory.create_backup_archive_locator(
            device_guid, destination_guid
        )
        connection = self._storage_session_manager.get_storage_session(token_provider)
        return StorageClient(connection)

    def from_plan_info(self, plan_uid, destination_guid):
        token_provider = self._token_provider_factory.create_security_archive_locator(
            plan_uid, destination_guid
        )
        connection = self._storage_session_manager.get_storage_session(token_provider)
        return StorageClient(connection)
