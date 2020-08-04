from threading import Lock

from requests import HTTPError

from py42._compat import str
from py42.exceptions import Py42StorageSessionInitializationError


class ConnectionManager(object):
    def __init__(self, session_cache=None):
        self._session_cache = session_cache or {}
        self._list_update_lock = Lock()

    def get_saved_session_for_url(self, url):
        return self._session_cache.get(url.lower())

    def get_storage_session(self, token_provider):
        try:
            url = token_provider.get_login_info()[u"serverUrl"]
            cnxn = self.get_saved_session_for_url(url)
            if cnxn is None:
                with self._list_update_lock:
                    cnxn = self.get_saved_session_for_url(url)
                    if cnxn is None:
                        cnxn = self.create_storage_session(url, token_provider)
                        self._session_cache.update({url.lower(): cnxn})
        except HTTPError as ex:
            message = u"Failed to create or retrieve cnxn, caused by: {}".format(
                str(ex)
            )
            raise Py42StorageSessionInitializationError(message)
        return cnxn

    def create_storage_session(self, url, token_provider):
        return self._session_factory.create_storage_session(url, token_provider)
