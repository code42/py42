from threading import Lock

from requests.auth import AuthBase


class C42RenewableAuth(AuthBase):
    def __init__(self):
        self._auth_lock = Lock()
        self._credentials = None

    def __call__(self, r):
        r.headers["Authorization"] = self.get_credentials()
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


class BearerAuth(C42RenewableAuth):
    def __init__(self, auth_connection, totp=None):
        super().__init__()
        self._auth_connection = auth_connection
        self._totp = totp if callable(totp) else lambda: totp

    def _get_credentials(self):
        uri = "/api/v3/auth/jwt"
        params = {"useBody": True}
        current_token = self._totp()
        headers = {"totp-auth": str(current_token)} if current_token else None
        response = self._auth_connection.get(uri, params=params, headers=headers)
        return f"Bearer {response['v3_user_token']}"


class ApiClientAuth(C42RenewableAuth):
    def __init__(self, auth_connnection):
        super().__init__()
        self._auth_connection = auth_connnection

    def _get_credentials(self):
        uri = "/api/v3/oauth/token"
        params = {"grant_type": "client_credentials"}
        response = self._auth_connection.post(uri, params=params)
        return f"Bearer {response['access_token']}"


class CustomJWTAuth(C42RenewableAuth):
    def __init__(self, jwt_provider):
        super().__init__()
        self._jwt_provider = jwt_provider

    def _get_credentials(self):
        return f"Bearer {self._jwt_provider()}"
