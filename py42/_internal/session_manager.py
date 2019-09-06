from threading import Lock

from py42._internal.session import Py42Session
from py42._internal.base_classes import BaseSessionFactory
from py42._internal.login_providers import LoginProvider


class SessionManager(object):
    def __init__(self):
        # override this in subclasses
        self._session_factory_method = None

        self._session_list = {}
        self._list_update_lock = Lock()

    def using(self, url):
        # type: (str) -> Py42Session
        return self._session_list.get(url.lower())

    def get_session(self, login_provider, force_replace=False):
        # type: (LoginProvider, bool) -> Py42Session
        if self._session_factory_method is not None:
            url = login_provider.get_target_host_address()
            session = self.using(url)
            if session is None or force_replace:
                try:
                    with self._list_update_lock:
                        session = self.using(url)
                        if session is None or force_replace:
                            session = self._session_factory_method(login_provider)
                            self._session_list.update({url.lower(): session})
                except Exception as e:
                    message = "Failed to create or retrieve session, caused by: {0}".format(e.message)
                    raise Exception(message)
            return session
        else:
            raise Exception("SessionManager is not meant to be instantiated directly, use a subclass.")

    def wait_all(self):
        with self._list_update_lock:
            for key in self._session_list:
                self._session_list[key].wait()


class StorageSessionManager(SessionManager):
    def __init__(self, session_factory):
        # type: (BaseSessionFactory) -> None
        super(StorageSessionManager, self).__init__()
        self._session_factory_method = session_factory.create_storage_session


class FileEventSessionManager(SessionManager):
    def __init__(self, session_factory):
        # type: (BaseSessionFactory) -> None
        super(FileEventSessionManager, self).__init__()
        self._session_factory_method = session_factory.create_file_event_session


class SessionsManager(object):
    def __init__(self, storage_session_manager, file_event_session_manager):
        # type: (StorageSessionManager, FileEventSessionManager) -> None
        self._storage_session_manager = storage_session_manager
        self._file_event_session_manager = file_event_session_manager
        self._node_guid_to_storage_url_map = {}

    def get_storage_session(self, login_provider, force_replace=False, node_guid=None):
        # type: (LoginProvider, bool, any) -> Py42Session
        storage_session = None
        if node_guid is not None:
            storage_url = self._node_guid_to_storage_url_map.get(node_guid)
            storage_session = self._storage_session_manager.using(storage_url or "")

        if storage_session is None:
            storage_session = self._storage_session_manager.get_session(login_provider,
                                                                        force_replace=force_replace)
        return storage_session

    def get_file_event_session(self, login_provider, force_replace=False):
        # type: (LoginProvider, bool) -> Py42Session
        return self._file_event_session_manager.get_session(login_provider, force_replace=force_replace)

    def wait_all(self):
        # TODO: INTEG-235 describes in detail a bug that needs to be addressed here.
        # currently the order in which we wait for sessions to complete must be the same as the order
        # in which they made their requests -- we need to make this more bulletproof.
        self._file_event_session_manager.wait_all()
        self._storage_session_manager.wait_all()
