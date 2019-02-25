from ..lib.authority import AuthorityClient, AuthorityTargetedClient
from .storageclientmanager import StorageClientManager


class SDKClient(object):

    def __init__(self, authority_api_client, storage_manager):
        # type: (AuthorityClient, StorageClientManager) -> None
        self._authority_api_client = authority_api_client
        self._storage_manager = storage_manager

    @classmethod
    def create_from_local_logon(cls, host_address, username, password, is_async=False):
        authority_client = AuthorityClient.create_from_local_logon(host_address, username, password, is_async=is_async)
        storage_location_requester = AuthorityTargetedClient.create_from_local_logon(host_address, username, password)
        storage_manager = StorageClientManager(storage_location_requester, is_async=is_async)
        return cls(authority_client, storage_manager)

    @property
    def authority(self):
        # type: () -> AuthorityClient
        return self._authority_api_client

    @property
    def storage(self):
        # type: () -> StorageClientManager
        return self._storage_manager
