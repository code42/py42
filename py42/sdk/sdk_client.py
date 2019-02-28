from py42.clients.authority import AuthorityClient
from py42.clients.authority.authority_base import AuthorityTargetedClient
from py42.sdk.storage_client_manager import StorageClientManager


class SDK(object):

    def __init__(self, authority_api_client, storage_manager):
        # type: (AuthorityClient, StorageClientManager) -> None
        self._authority_api_client = authority_api_client
        self._storage_manager = storage_manager

    @classmethod
    def create_using_local_account(cls, host_address, username, password, is_async=False):
        authority_client = AuthorityClient.create_using_local_account(host_address, username, password,
                                                                      is_async=is_async)
        storage_location_requester = AuthorityTargetedClient.create_using_local_account(host_address, username,
                                                                                        password)
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
