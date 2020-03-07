from threading import Lock

from py42._internal.compat import str


class StorageSessionManager(object):
    def __init__(self, session_factory, session_cache=None):
        self._session_factory = session_factory
        self._session_cache = session_cache or {}
        self._list_update_lock = Lock()

    def get_saved_session_for_url(self, url):
        return self._session_cache.get(url.lower())

    def get_storage_session(self, token_provider):
        try:
            url = token_provider.get_login_info()[u"serverUrl"]
            session = self.get_saved_session_for_url(url)
            if session is None:
                with self._list_update_lock:
                    session = self.get_saved_session_for_url(url)
                    if session is None:
                        session = self.create_storage_session(url, token_provider)
                        self._session_cache.update({url.lower(): session})
        except Exception as ex:
            message = u"Failed to create or retrieve session, caused by: {0}".format(str(ex))
            raise Exception(message)
        return session

    def create_storage_session(self, url, token_provider):
        return self._session_factory.create_storage_session(url, token_provider)
