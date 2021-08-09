from py42.services._auth import C42RenewableAuth
from py42.services._connection import Connection


class StorageAuth(C42RenewableAuth):
    def __init__(self):
        super().__init__()
        self._storage_url = None
        self._storage_connection = None

    def get_storage_url(self):
        self.get_credentials()
        return self._storage_url

    def get_tmp_auth(self):
        raise NotImplementedError()

    def _get_auth_token(self, login_token):
        uri = "api/AuthToken"
        response = self._storage_connection.post(
            uri, headers={"Authorization": f"login_token {login_token}"}
        )
        token1, token2 = response.data
        return f"token {token1}-{token2}"

    def _get_credentials(self):
        storage_url, login_token = self.get_tmp_auth()
        self._storage_url = storage_url
        self._storage_connection = (
            self._storage_connection or _get_new_storage_connection(self._storage_url)
        )
        return self._get_auth_token(login_token)


class FileArchiveAuth(StorageAuth):
    def __init__(self, connection, user_id, device_guid, destination_guid):
        super().__init__()
        self._connection = connection
        self._user_id = user_id
        self._device_guid = device_guid
        self._destination_guid = destination_guid

    def get_tmp_auth(self):
        uri = "/api/LoginToken"
        data = {
            "userId": self._user_id,
            "sourceGuid": self._device_guid,
            "destinationGuid": self._destination_guid,
        }
        response = self._connection.post(uri, json=data)
        storage_url = response["serverUrl"]
        login_token = response["loginToken"]
        return storage_url, login_token


def _get_new_storage_connection(storage_url):
    return Connection.from_host_address(storage_url)
