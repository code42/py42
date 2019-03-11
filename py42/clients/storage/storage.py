from py42.clients.storage.security import SecurityClient
from py42.clients.storage.restore import RestoreClient
from py42.clients.storage.archive import ArchiveClient
from py42.clients.storage.storage_base import StorageTargetedClient


class StorageClient(StorageTargetedClient):

    def __init__(self, session):
        super(StorageClient, self).__init__(session)
        self._security_client = SecurityClient(session)
        self._restore_client = RestoreClient(session)
        self._archive_client = ArchiveClient(session)

    @property
    def security(self):
        return self._security_client

    @property
    def restore(self):
        return self._restore_client

    @property
    def archive(self):
        return self._archive_client
