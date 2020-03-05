import base64
import json

from py42._internal.auth_handling import LoginProvider
from py42._internal.compat import str

V3_AUTH = u"v3_user_token"
V3_COOKIE_NAME = u"C42_JWT_API_TOKEN"


class BasicAuthProvider(LoginProvider):
    def __init__(self, username, password):
        super(BasicAuthProvider, self).__init__()
        cred_bytes = base64.b64encode(u"{0}:{1}".format(username, password).encode(u"utf-8"))
        self._base64_credentials = cred_bytes.decode(u"utf-8")

    def get_secret_value(self, force_refresh=False):
        return self._base64_credentials


class C42ApiV3TokenProvider(LoginProvider):
    def __init__(self, auth_session):
        super(C42ApiV3TokenProvider, self).__init__()
        self._auth_session = auth_session

    def get_secret_value(self, force_refresh=False):
        uri = u"/c42api/v3/auth/jwt"
        params = {u"useBody": True}
        response = self._auth_session.get(uri, params=params)
        if response.text:
            response_data = json.loads(response.text)[u"data"]
            token = str(response_data[V3_AUTH])
        else:
            # some older versions only return the v3 token in a cookie.
            token = self._auth_session.cookies.get_dict().get(V3_COOKIE_NAME)

        return token


class C42ApiV1TokenProvider(LoginProvider):
    def __init__(self, auth_session):
        super(C42ApiV1TokenProvider, self).__init__()
        self._auth_session = auth_session

    def get_secret_value(self, force_refresh=False):
        uri = u"/api/AuthToken"
        response = self._auth_session.post(uri, data=None)
        response_data = json.loads(response.text)[u"data"]
        token = u"{0}-{1}".format(response_data[0], response_data[1])
        return token


class C42APITmpAuthProvider(LoginProvider):
    def __init__(self):
        super(C42APITmpAuthProvider, self).__init__()
        self._cached_info = None

    def get_login_info(self):
        if self._cached_info is None:
            response = self.get_tmp_auth_token()  # pylint: disable=assignment-from-no-return
            logon_info = json.loads(response.text)[u"data"]
            self._cached_info = logon_info
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
