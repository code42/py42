from py42._internal.base_classes import BaseClient
from py42._internal.clients.storage.archive import StorageArchiveClient
from py42._internal.clients.storage.security import StorageSecurityClient


class StorageClient(BaseClient):
    def __init__(self, session):
        super(StorageClient, self).__init__(session)
        self._archive_client = StorageArchiveClient(session)
        self._security_client = StorageSecurityClient(session)

    @property
    def archive(self):
        return self._archive_client

    @property
    def security(self):
        return self._security_client
