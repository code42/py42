from threading import Lock

from py42.clients.storage import StorageClient
from py42.clients.storage.storage_base import StorageTargetedClient


class StorageClientManager(object):
    def __init__(self, storage_logon_info_requester, is_async=False):
        self._storage_logon_info_requester = storage_logon_info_requester
        self._is_async = is_async
        self._client_list = {}
        self._list_update_lock = Lock()

    def using(self, storage_url):
        # type: (str) -> StorageClient
        return self._client_list.get(storage_url.lower(), None)

    def _fetch_client(self, storage_url, factory_func, force_replace=False, is_async=False):
        try:
            token_requester = factory_func()
            self._list_update_lock.acquire()
            storage_client = self.using(storage_url)
            update = storage_client is None or force_replace
            if update:
                storage_client = StorageClient.create_with_v1_token_auth(storage_url, token_requester,
                                                                         is_async=is_async)
                self._client_list.update({storage_url.lower(): storage_client})
            self._list_update_lock.release()
        except Exception as e:
            message = "Failed to add storage client to SDK API list, caused by: {0}".format(e.message)
            raise Exception(message)

        return storage_client

    def fetch_client_using_plan_info(self, init_plan_uid, init_destination_guid, force_replace=False, is_async=False):

        logon_info = self._storage_logon_info_requester.get_storage_logon_info_using_plan_info(init_plan_uid,
                                                                                               init_destination_guid)
        storage_url = logon_info["serverUrl"]
        existing_storage_client = self.using(storage_url)

        if existing_storage_client is not None:
            return existing_storage_client

        def get_storage_logon_info(force_refresh=False):
            if not force_refresh:
                return logon_info["loginToken"]

            refreshed_logon_info = self._storage_logon_info_requester.get_storage_logon_info_using_plan_info(
                init_plan_uid,
                init_destination_guid)

            return refreshed_logon_info["loginToken"]

        def factory_method():
            return StorageTargetedClient.create_using_tmp_storage_token_requester(storage_url,
                                                                                  get_storage_logon_info)

        storage_client = self._fetch_client(storage_url,
                                            factory_method,
                                            force_replace=force_replace,
                                            is_async=self._is_async or is_async)

        return storage_client

    def wait_all(self):
        self._list_update_lock.acquire()
        for key in self._client_list:
            self._client_list[key].wait()
        self._list_update_lock.release()
