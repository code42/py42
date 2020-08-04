import json
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


class StorageTmpAuth(C42RenewableAuth):
    def __init__(self):
        super(StorageTmpAuth, self).__init__()
        self._cached_info = None

    def get_login_info(self):
        if self._cached_info is None:
            response = self.get_tmp_auth_token()
            self._cached_info = response
        return self._cached_info

    def get_tmp_auth_token(self):
        raise NotImplementedError()

    def _get_credentials(self):
        if self._cached_info is None:
            self.get_login_info()
        login_token = self._cached_info[u"loginToken"]
        return u"{} {}".format(u"login_token", login_token)


class FileArchiveTmpAuth(StorageTmpAuth):
    def __init__(self, auth_session, user_id, device_guid, destination_guid):
        super(FileArchiveTmpAuth, self).__init__()
        self._auth_session = auth_session
        self._user_id = user_id
        self._device_guid = device_guid
        self._destination_guid = destination_guid

    def get_tmp_auth_token(self):
        uri = u"/api/LoginToken"
        data = {
            u"userId": self._user_id,
            u"sourceGuid": self._device_guid,
            u"destinationGuid": self._destination_guid,
        }
        response = self._auth_session.post(uri, data=json.dumps(data))
        return response


class SecurityArchiveTmpAuth(StorageTmpAuth):
    def __init__(self, auth_session, plan_uid, destination_guid):
        super(SecurityArchiveTmpAuth, self).__init__()
        self._auth_session = auth_session
        self._plan_uid = plan_uid
        self._destination_guid = destination_guid

    def get_tmp_auth_token(self):
        uri = u"/api/StorageAuthToken"
        data = {u"planUid": self._plan_uid, u"destinationGuid": self._destination_guid}
        response = self._auth_session.post(uri, data=json.dumps(data))
        return response


class StorageTokenProviderFactory(object):
    def __init__(self, auth_session, security_client, device_client):
        self._auth_session = auth_session
        self._security_client = security_client
        self._device_client = device_client

    def create_security_archive_locator(self, plan_uid, destination_guid):
        return SecurityArchiveTmpAuth(self._auth_session, plan_uid, destination_guid)

    def create_backup_archive_locator(self, device_guid, destination_guid=None):
        if destination_guid is None:
            response = self._device_client.get_by_guid(
                device_guid, include_backup_usage=True
            )
            if destination_guid is None:
                # take the first destination guid we find
                destination_list = response["backupUsage"]
                if not destination_list:
                    raise Exception(
                        u"No destinations found for device guid: {}".format(device_guid)
                    )
                destination_guid = destination_list[0][u"targetComputerGuid"]

        return FileArchiveTmpAuth(
            self._auth_session, u"my", device_guid, destination_guid
        )
