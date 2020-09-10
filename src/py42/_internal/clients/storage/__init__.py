from py42._internal.clients.storage.archive import StorageArchiveClient
from py42._internal.clients.storage.securitydata import StorageSecurityClient
from py42.clients import BaseClient


class StorageClient(BaseClient):
    def __init__(self, session):
        super(StorageClient, self).__init__(session)
        self._archive_client = StorageArchiveClient(session)
        self._security_client = StorageSecurityClient(session)

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
        session = self._storage_session_manager.get_storage_session(token_provider)
        return StorageClient(session)

    def from_plan_info(self, plan_uid, destination_guid):
        token_provider = self._token_provider_factory.create_security_archive_locator(
            plan_uid, destination_guid
        )
        session = self._storage_session_manager.get_storage_session(token_provider)
        return StorageClient(session)
