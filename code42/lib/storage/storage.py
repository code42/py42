from .storagebase import StorageTargetedClient
from .securitytools import SecurityToolsClient


class StorageClient(StorageTargetedClient):

    def __init__(self, session):
        super(StorageClient, self).__init__(session)
        self._securitytools = SecurityToolsClient(session)

    @property
    def securitytools(self):
        return self._securitytools
