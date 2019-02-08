from storage_client_manager import StorageClientManager
from client_factory import build_credentials_based_authority_client


class SDKClient(object):

    def __init__(self, authority_api_client, storage_manager):
        self._authority_api_client = authority_api_client
        self._storage_manager = storage_manager

    @classmethod
    def create_via_credentials(cls, host_address, username, password, proxies=None, is_async=False):
        client = build_credentials_based_authority_client(host_address, username, password, proxies, is_async)
        storage_logon_client = build_credentials_based_authority_client(host_address, username,
                                                                        password, proxies, False)
        storage_manager = StorageClientManager(storage_logon_client, is_async)
        return cls(client, storage_manager)

    @property
    def authority_api(self):
        return self._authority_api_client

    @property
    def storage_api(self):
        return self._storage_manager

