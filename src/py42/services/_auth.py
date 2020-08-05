from threading import Lock

from requests.auth import AuthBase


class C42RenewableAuth(AuthBase):
    def __init__(self):
        self._auth_lock = Lock()
        self._credentials = None

    def __call__(self, r):
        with self._auth_lock:
            self._credentials = self._credentials or self._get_credentials()
            r.headers[u"Authorization"] = self._credentials
        return r

    def clear_credentials(self):
        # Do not clear credentials while they are being retrieved
        with self._auth_lock:
            self._credentials = None

    def _get_credentials(self):
        raise NotImplementedError()


class V3Auth(C42RenewableAuth):
    def __init__(self, auth_connection):
        super(V3Auth, self).__init__()
        self._auth_connection = auth_connection

    def _get_credentials(self):
        uri = u"/c42api/v3/auth/jwt"
        params = {u"useBody": True}
        response = self._auth_connection.get(uri, params=params)
        return u"{} {}".format("v3_user_token", response["v3_user_token"])


class V1Auth(C42RenewableAuth):
    def __init__(self, storage_tmp_session):
        super(V1Auth, self).__init__()
        self._auth_session = storage_tmp_session

    def _get_credentials(self):
        uri = u"/api/AuthToken"
        response = self._auth_session.post(uri, data=None)
        return u"{} {}-{}".format(u"token", response[0], response[1])


