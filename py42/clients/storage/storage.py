from py42.clients.storage.security import SecurityClient
from py42.clients.storage.storage_base import StorageTargetedClient


class StorageClient(StorageTargetedClient):

    def __init__(self, session):
        super(StorageClient, self).__init__(session)
        self._security_client = SecurityClient(session)

    @property
    def security(self):
        return self._security_client
