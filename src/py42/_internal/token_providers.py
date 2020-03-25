import base64
import json

from py42._internal.auth_handling import TokenProvider

V3_AUTH = u"v3_user_token"


class BasicAuthProvider(TokenProvider):
    def __init__(self, username, password):
        super(BasicAuthProvider, self).__init__()
        cred_bytes = base64.b64encode(u"{0}:{1}".format(username, password).encode(u"utf-8"))
        self._base64_credentials = cred_bytes.decode(u"utf-8")

    def get_secret_value(self, force_refresh=False):
        return self._base64_credentials


class C42ApiV3TokenProvider(TokenProvider):
    def __init__(self, auth_session):
        super(C42ApiV3TokenProvider, self).__init__()
        self._auth_session = auth_session

    def get_secret_value(self, force_refresh=False):
        uri = u"/c42api/v3/auth/jwt"
        params = {u"useBody": True}
        response = self._auth_session.get(uri, params=params)
        return response[V3_AUTH]


class C42ApiV1TokenProvider(TokenProvider):
    def __init__(self, auth_session):
        super(C42ApiV1TokenProvider, self).__init__()
        self._auth_session = auth_session

    def get_secret_value(self, force_refresh=False):
        uri = u"/api/AuthToken"
        response = self._auth_session.post(uri, data=None)
        return u"{0}-{1}".format(response[0], response[1])


class C42APITmpAuthProvider(TokenProvider):
    def __init__(self):
        super(C42APITmpAuthProvider, self).__init__()
        self._cached_info = None

    def get_login_info(self):
        if self._cached_info is None:
            response = self.get_tmp_auth_token()  # pylint: disable=assignment-from-no-return
            self._cached_info = response
        return self._cached_info

    def get_tmp_auth_token(self):
        pass

    def get_secret_value(self, force_refresh=False):
        if force_refresh or self._cached_info is None:
            self.get_login_info()
        return self._cached_info[u"loginToken"]


class C42APILoginTokenProvider(C42APITmpAuthProvider):
    def __init__(self, auth_session, user_id, device_guid, destination_guid):
        super(C42APILoginTokenProvider, self).__init__()
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


class C42APIStorageAuthTokenProvider(C42APITmpAuthProvider):
    def __init__(self, auth_session, plan_uid, destination_guid):
        super(C42APIStorageAuthTokenProvider, self).__init__()
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
        return C42APIStorageAuthTokenProvider(self._auth_session, plan_uid, destination_guid)

    def create_backup_archive_locator(self, device_guid, destination_guid=None):
        if destination_guid is None:
            response = self._device_client.get_by_guid(device_guid, include_backup_usage=True)
            if destination_guid is None:
                # take the first destination guid we find
                destination_list = response["backupUsage"]
                if not destination_list:
                    raise Exception(
                        u"No destinations found for device guid: {0}".format(device_guid)
                    )
                destination_guid = destination_list[0][u"targetComputerGuid"]

        return C42APILoginTokenProvider(self._auth_session, u"my", device_guid, destination_guid)
