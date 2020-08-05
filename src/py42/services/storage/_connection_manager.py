from threading import Lock

from requests import HTTPError

from py42._compat import str
from py42.exceptions import Py42StorageSessionInitializationError


class ConnectionManager(object):
    def __init__(self, session_cache=None):
        self._session_cache = session_cache or {}
        self._list_update_lock = Lock()

    def get_saved_connection_for_url(self, url):
        return self._session_cache.get(url.lower())

    def get_storage_connection(self, token_provider):
        try:
            url = token_provider.get_login_info()[u"serverUrl"]
            connection = self.get_saved_connection_for_url(url)
            if connection is None:
                with self._list_update_lock:
                    connection = self.get_saved_connection_for_url(url)
                    if connection is None:
                        connection = self.create_storage_connection(url, token_provider)
                        self._session_cache.update({url.lower(): connection})
        except HTTPError as ex:
            message = u"Failed to create or retrieve connection, caused by: {}".format(
                str(ex)
            )
            raise Py42StorageSessionInitializationError(message)
        return connection

    def create_storage_connection(self, url, token_provider):
        return self._session_factory.create_storage_connection(url, token_provider)
