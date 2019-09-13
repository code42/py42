from threading import Lock

from py42._internal.base_classes import BaseSessionFactory
from py42._internal.login_providers import LoginProvider
from py42._internal.session import Py42Session


class SessionManager(object):
    def __init__(self, session_cache=None):
        self._session_cache = session_cache or {}
        self._list_update_lock = Lock()

    def get_saved_session_for_url(self, url):
        return self._session_cache.get(url.lower())

    def get_session(self, login_provider, force_replace=False):
        # type: (LoginProvider, bool) -> Py42Session
        url = login_provider.get_target_host_address()
        session = self.get_saved_session_for_url(url)
        if session is None or force_replace:
            try:
                with self._list_update_lock:
                    session = self.get_saved_session_for_url(url)
                    if session is None or force_replace:
                        session = self.create_session(login_provider)
                        self._session_cache.update({url.lower(): session})
            except Exception as e:
                message = "Failed to create or retrieve session, caused by: {0}".format(e.message)
                raise Exception(message)
        return session

    def create_session(self, login_provider, force_replace=False):
        pass

    def wait_all(self):
        with self._list_update_lock:
            for key in self._session_cache:
                self._session_cache[key].wait()


class StorageSessionManager(SessionManager):
    def __init__(self, session_factory):
        # type: (BaseSessionFactory) -> None
        super(StorageSessionManager, self).__init__()
        self._session_factory = session_factory

    def create_session(self, login_provider, force_replace=False):
        return self._session_factory.create_storage_session(login_provider)


class FileEventSessionManager(SessionManager):
    def __init__(self, session_factory):
        # type: (BaseSessionFactory) -> None
        super(FileEventSessionManager, self).__init__()
        self._session_factory = session_factory

    def create_session(self, login_provider, force_replace=False):
        return self._session_factory.create_file_event_session(login_provider)


class SessionsManager(object):
    def __init__(self, storage_session_manager, file_event_session_manager):
        # type: (StorageSessionManager, FileEventSessionManager) -> None
        self._storage_session_manager = storage_session_manager
        self._file_event_session_manager = file_event_session_manager

    def get_storage_session(self, login_provider, force_replace=False):
        # type: (LoginProvider, bool) -> Py42Session
        return self._storage_session_manager.get_session(login_provider, force_replace=force_replace)

    def get_file_event_session(self, login_provider, force_replace=False):
        # type: (LoginProvider, bool) -> Py42Session
        return self._file_event_session_manager.get_session(login_provider, force_replace=force_replace)

    def wait_all(self):
        # TODO: INTEG-235 describes in detail a bug that needs to be addressed here.
        # currently the order in which we wait for sessions to complete must be the same as the order
        # in which they made their requests -- we need to make this more bulletproof.
        self._file_event_session_manager.wait_all()
        self._storage_session_manager.wait_all()
