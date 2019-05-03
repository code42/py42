from threading import Lock

from py42._internal.base_classes import BaseSessionFactory
from py42._internal.session import Py42Session
from py42._internal.login_providers import FileEventLoginProvider


class SessionManager(object):
    def __init__(self, session_factory, is_async=False):
        # type: (BaseSessionFactory, bool) -> None
        self._session_factory = session_factory
        self._is_async = is_async
        self._session_list = {}
        self._node_guid_to_storage_url_map = {}
        self._list_update_lock = Lock()

    def using(self, storage_url):
        # type: (str) -> Py42Session
        return self._session_list.get(storage_url.lower())

    def get_storage_session(self, login_provider, force_replace=False):
        storage_session = None
        node_guid = login_provider.node_guid
        if node_guid is not None:
            storage_url = self._node_guid_to_storage_url_map.get(node_guid)
            storage_session = self.using(storage_url or "")

        if storage_session is None:
            storage_url = login_provider.get_target_host_address()
            try:
                self._list_update_lock.acquire()
                storage_session = self.using(storage_url)
                update = storage_session is None or force_replace
                if update:
                    storage_session = self._session_factory.create_storage_session(login_provider)
                    self._session_list.update({storage_url.lower(): storage_session})
                    self._node_guid_to_storage_url_map.update({node_guid: storage_url.lower()})
                self._list_update_lock.release()
            except Exception as e:
                message = "Failed to create or retrieve storage session, caused by: {0}".format(e.message)
                raise Exception(message)

        return storage_session

    def get_file_event_session(self, login_provider):
        # type: (FileEventLoginProvider) -> Py42Session
        file_event_service_url = login_provider.get_target_host_address()
        file_event_session = self.using(file_event_service_url)
        if not file_event_session:
            try:
                self._list_update_lock.acquire()
                file_event_session = self.using(file_event_service_url)
                if not file_event_session:
                    file_event_session = self._session_factory.create_file_event_session(login_provider)
                    self._session_list.update({file_event_service_url.lower(): file_event_session})
                self._list_update_lock.release()
            except Exception as e:
                message = "Failed to create or retrieve file event session, caused by: {0}".format(e.message)
                raise Exception(message)
        return file_event_session

    def wait_all(self):
        self._list_update_lock.acquire()
        for key in self._session_list:
            self._session_list[key].wait()
        self._list_update_lock.release()
