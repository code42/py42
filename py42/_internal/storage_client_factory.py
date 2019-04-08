from py42._internal.storage_session_manager import StorageSessionManager
from py42._internal.base_classes import BaseArchiveLocatorFactory
from py42._internal.clients.storage.storage import StorageClient


class StorageClientFactory(object):
    def __init__(self, storage_session_manager, login_provider_factory):
        # type: (StorageSessionManager, BaseArchiveLocatorFactory) -> StorageClientFactory
        self._storage_session_manager = storage_session_manager
        self._provider_factory = login_provider_factory

    def create_backup_client(self, *args, **kwargs):
        locator = self._provider_factory.create_backup_archive_locator(*args, **kwargs)
        session = self._storage_session_manager.get_storage_session(locator)
        return StorageClient(session)

    def create_security_plan_clients(self, *args, **kwargs):
        locators = self._provider_factory.create_security_archive_locators(*args, **kwargs)
        sessions = [self._storage_session_manager.get_storage_session(locator) for locator in locators]
        clients = [StorageClient(session) for session in sessions]
        return clients
