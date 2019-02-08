from .api import StorageAPIClient
from .api.handlers.http import util, threadutils

STORAGE_CLIENTS_LIST_LOCK = "scll"


class StorageClientManager(object):
    def __init__(self, storage_logon_client, is_async):
        self._storage_logon_client = storage_logon_client
        self._is_async = is_async
        self._client_list = {}
        self._lock = threadutils.ScopedLock()

    def using(self, storage_url):
        return self._client_list.get(storage_url, None)

    def _fetch_client(self, storage_url, force_replace, factory_func, **kwargs):
        storage_client = self._client_list.get(storage_url, None)
        if storage_client is None or force_replace:
            try:
                created = False
                self._lock.acquire(storage_url)
                new_storage_client = self._client_list.get(storage_url, None)
                if new_storage_client is None:
                    created = True
                    new_storage_client = factory_func(**kwargs)
                storage_client = new_storage_client
                if created:
                    self._lock.acquire(STORAGE_CLIENTS_LIST_LOCK)
                    self._client_list.update({storage_url: storage_client})
                    self._lock.release(STORAGE_CLIENTS_LIST_LOCK)
            except Exception as e:
                message = "Failed to add storage client to SDK API list."
                raise Exception(message + ", caused by: " + e.message)
            finally:
                self._lock.release(storage_url)

        return storage_client

    def fetch_client_via_plan_info(self, init_plan_uid, init_destination_guid, force_replace=False):
        response = self._storage_logon_client.storage_auth_token(init_plan_uid, init_destination_guid)
        storage_logon_info = util.get_obj_from_response(response, "data")
        storage_url = storage_logon_info["serverUrl"]
        return self._fetch_client(storage_url, force_replace, StorageAPIClient.create_v1_token_client,
                                  authority_api=self._storage_logon_client,
                                  init_plan_uid=init_plan_uid,
                                  init_destination_guid=init_destination_guid,
                                  storage_logon_info=storage_logon_info,
                                  is_async=self._is_async)

    def wait_all(self):
        self._lock.acquire(STORAGE_CLIENTS_LIST_LOCK)
        for key in self._client_list:
            self._client_list[key].wait()
        self._lock.release(STORAGE_CLIENTS_LIST_LOCK)
