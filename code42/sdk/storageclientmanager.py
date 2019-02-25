from threading import Lock
import json
from ..lib.storage import StorageClient
from ..lib.storage.storagebase import StorageTargetedClient


class StorageClientManager(object):
    def __init__(self, storage_location_requester, is_async=False):
        self._storage_location_requester = storage_location_requester
        self._is_async = is_async
        self._client_list = {}
        self._list_update_lock = Lock()

    def using(self, storage_url):
        # type: (str) -> StorageClient
        return self._client_list.get(storage_url, None)

    def _fetch_client(self, storage_url, factory_func, force_replace=False, is_async=False):
        try:
            tmp_login_client = factory_func()
            self._list_update_lock.acquire()
            storage_client = self.using(storage_url)
            update = storage_client is None or force_replace
            if update:
                storage_client = StorageClient.create_with_v1_token_auth(storage_url, tmp_login_client,
                                                                         is_async=is_async)
                self._client_list.update({storage_url: storage_client})
            self._list_update_lock.release()
        except Exception as e:
            message = "Failed to add storage client to SDK API list."
            raise Exception(message + ", caused by: " + e.message)

        return storage_client

    def fetch_client_via_plan_info(self, init_plan_uid, init_destination_guid, force_replace=False, is_async=False):

        response = self._storage_location_requester.get_storage_auth_token(init_plan_uid, init_destination_guid)
        logon_info = json.loads(response.content)["data"]
        storage_url = logon_info["serverUrl"]
        existing_storage_client = self.using(storage_url)

        if existing_storage_client is not None:
            return existing_storage_client

        def factory_method():
            return StorageTargetedClient.create_with_tmp_auth_from_plan_info(self._storage_location_requester,
                                                                             init_plan_uid, init_destination_guid)
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
