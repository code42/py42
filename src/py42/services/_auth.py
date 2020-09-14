from threading import Lock

from requests.auth import AuthBase


class C42RenewableAuth(AuthBase):
    def __init__(self):
        self._auth_lock = Lock()
        self._credentials = None

    def __call__(self, r):
        r.headers[u"Authorization"] = self.get_credentials()
        return r

    def clear_credentials(self):
        # Do not clear credentials while they are being retrieved
        with self._auth_lock:
            self._credentials = None

    def get_credentials(self):
        if not self._credentials:
            with self._auth_lock:
                if not self._credentials:
                    self._credentials = self._credentials or self._get_credentials()
        return self._credentials

    def _get_credentials(self):
        raise NotImplementedError()


class V3Auth(C42RenewableAuth):
    def __init__(self, auth_connection, totp=None):
        super(V3Auth, self).__init__()
        self._auth_connection = auth_connection
        self._totp = totp if callable(totp) else lambda: totp

    def _get_credentials(self):
        uri = u"/c42api/v3/auth/jwt"
        params = {u"useBody": True}
        currentToken = self._totp()
        headers = {"totp-auth": str(currentToken)} if currentToken else None
        response = self._auth_connection.get(uri, params=params, headers=headers)
        return u"v3_user_token {}".format(response["v3_user_token"])
