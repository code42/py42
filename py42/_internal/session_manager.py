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
        self._cache_key_to_storage_url_map = {}
        self._cache_update_lock = Lock()

    def get_url_for_cache_key(self, cache_key):
        return self._cache_key_to_storage_url_map.get(cache_key)

    def get_session(self, login_provider, force_replace=False):
        storage_session, needs_cache_key_update = self._get_session_from_cache(login_provider, force_replace)
        if storage_session and needs_cache_key_update:
            self._add_cache_key_url_mapping(login_provider, storage_session)

        return storage_session

    def _add_cache_key_url_mapping(self, login_provider, storage_session):
        with self._cache_update_lock:
            self._cache_key_to_storage_url_map.update({login_provider.session_cache_key: storage_session.host_address})

    def _get_session_from_cache(self, login_provider, force_replace):
        storage_session = None
        needs_cache_key_update = False

        if login_provider.session_cache_key is not None and not force_replace:
            storage_url = self.get_url_for_cache_key(login_provider.session_cache_key)
            if storage_url is not None:
                storage_session = self.get_saved_session_for_url(storage_url)
            else:
                needs_cache_key_update = True

        if storage_session is None or force_replace:
            storage_session = super(StorageSessionManager, self).get_session(login_provider, force_replace)
        return storage_session, needs_cache_key_update

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
