from threading import Lock

from py42._internal.base_classes import BaseAuthStrategy
from py42._internal.session import Py42Session


class StorageSessionManager(object):
    def __init__(self, auth_strategy, is_async=False):
        # type: (BaseAuthStrategy, bool) -> None
        self._auth_strategy = auth_strategy
        self._is_async = is_async
        self._session_list = {}
        self._guid_to_url_map = {}
        self._list_update_lock = Lock()

    def using(self, storage_url):
        # type: (str) -> Py42Session
        return self._session_list.get(storage_url.lower())

    def get_storage_session(self, archive_locator, force_replace=False):
        storage_session = None
        node_guid = archive_locator.node_guid
        if node_guid is not None:
            storage_url = self._guid_to_url_map.get(node_guid)
            storage_session = self.using(storage_url or "")

        if storage_session is None:
            storage_url = archive_locator.get_target_host_address()
            try:
                self._list_update_lock.acquire()
                storage_session = self.using(storage_url)
                update = storage_session is None or force_replace
                if update:
                    storage_session = self._auth_strategy.create_storage_session(archive_locator)
                    self._session_list.update({storage_url.lower(): storage_session})
                    self._guid_to_url_map.update({node_guid: storage_url.lower()})
                self._list_update_lock.release()
            except Exception as e:
                message = "Failed to create or retrieve storage session, caused by: {0}".format(e.message)
                raise Exception(message)

        return storage_session

    def wait_all(self):
        self._list_update_lock.acquire()
        for key in self._session_list:
            self._session_list[key].wait()
        self._list_update_lock.release()
