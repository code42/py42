import base64
import json

from py42._internal.auth_handling import LoginProvider
from py42._internal.compat import str

V3_AUTH = u"v3_user_token"
V3_COOKIE_NAME = u"C42_JWT_API_TOKEN"


class BasicAuthProvider(LoginProvider):
    def __init__(self, host_address, username, password):
        super(BasicAuthProvider, self).__init__()
        self._host_address = host_address
        cred_bytes = base64.b64encode(u"{0}:{1}".format(username, password).encode(u"utf-8"))
        self._base64_credentials = cred_bytes.decode(u"utf-8")

    def get_target_host_address(self):
        return self._host_address

    def get_secret_value(self, force_refresh=False):
        return self._base64_credentials


class C42ApiV3TokenProvider(LoginProvider):
    def __init__(self, auth_session):
        super(C42ApiV3TokenProvider, self).__init__()
        self._auth_session = auth_session

    def get_target_host_address(self):
        return self._auth_session.host_address

    def get_secret_value(self, force_refresh=False):
        uri = u"/c42api/v3/auth/jwt"
        params = {u"useBody": True}
        try:
            response = self._auth_session.get(uri, params=params)
            if response.text:
                response_data = json.loads(response.text)[u"data"]
                token = str(response_data[V3_AUTH])
            else:
                # some older versions only return the v3 token in a cookie.
                token = self._auth_session.cookies.get_dict().get(V3_COOKIE_NAME)

            return token
        except Exception as ex:
            message = u"An error occurred while trying to retrieve a jwt token, caused by {0}"
            message = message.format(str(ex))
            raise Exception(message)


class C42ApiV1TokenProvider(LoginProvider):
    def __init__(self, auth_session):
        super(C42ApiV1TokenProvider, self).__init__()
        self._auth_session = auth_session

    def get_target_host_address(self):
        return self._auth_session.host_address

    def get_secret_value(self, force_refresh=False):
        uri = u"/api/AuthToken"
        try:
            response = self._auth_session.post(uri, data=None)
            response_data = json.loads(response.text)[u"data"]
            token = u"{0}-{1}".format(response_data[0], response_data[1])
            return token
        except Exception as ex:
            message = u"An error occurred while trying to retrieve a V1 auth token, caused by {0}"
            message = message.format(str(ex))
            raise Exception(message)


class C42APITmpAuthProvider(LoginProvider):
    def __init__(self):
        super(C42APITmpAuthProvider, self).__init__()
        self._cached_info = None

    def get_target_host_address(self):
        if self._cached_info is not None:
            return self._cached_info[u"serverUrl"]

        return self.get_login_info()[u"serverUrl"]

    def get_login_info(self):
        try:
            response = self.get_tmp_auth_token()  # pylint: disable=assignment-from-no-return
            logon_info = json.loads(response.text)[u"data"]
            self._cached_info = logon_info
            return logon_info
        except Exception as ex:
            message = (
                u"An error occurred while trying to retrieve storage logon info, caused by {0}"
            )
            message = message.format(str(ex))
            raise Exception(message)

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
        try:
            uri = u"/api/LoginToken"
            data = {
                u"userId": self._user_id,
                u"sourceGuid": self._device_guid,
                u"destinationGuid": self._destination_guid,
            }
            response = self._auth_session.post(uri, data=json.dumps(data))
            return response
        except Exception as ex:
            message = u"An error occurred while requesting a LoginToken, caused by {0}"
            message = message.format(str(ex))
            raise Exception(message)


class C42APIStorageAuthTokenProvider(C42APITmpAuthProvider):
    def __init__(self, auth_session, plan_uid, destination_guid):
        super(C42APIStorageAuthTokenProvider, self).__init__()
        self._auth_session = auth_session
        self._plan_uid = plan_uid
        self._destination_guid = destination_guid

    def get_tmp_auth_token(self):
        try:
            uri = u"/api/StorageAuthToken"
            data = {u"planUid": self._plan_uid, u"destinationGuid": self._destination_guid}
            response = self._auth_session.post(uri, data=json.dumps(data))
            return response
        except Exception as ex:
            message = u"An error occurred while requesting a StorageAuthToken, caused by {0}"
            message = message.format(str(ex))
            raise Exception(message)


class FileEventLoginProvider(C42ApiV3TokenProvider):
    def __init__(self, auth_session):
        super(FileEventLoginProvider, self).__init__(auth_session)
        self._forensic_search_url = None

    def get_target_host_address(self):
        # HACK: The forensic search base URL can be derived from the STS base URL, which is
        # available from the /api/ServerEnv resource.
        if self._forensic_search_url is None:
            sts_base_url = _get_sts_base_url(self._auth_session)
            self._forensic_search_url = str(sts_base_url).replace(u"sts", u"forensicsearch")
        return self._forensic_search_url


class KeyValueStoreLoginProvider(LoginProvider):
    def __init__(self, auth_session):
        super(KeyValueStoreLoginProvider, self).__init__()
        self._auth_session = auth_session
        self._key_value_store_url = None

    def get_target_host_address(self):
        # HACK: The simple-key-value-store base URL can be derived from the STS base URL, which is
        # available from the /api/ServerEnv resource.
        if self._key_value_store_url is None:
            sts_base_url = _get_sts_base_url(self._auth_session)
            self._key_value_store_url = str(sts_base_url).replace(u"sts", u"simple-key-value-store")
        return self._key_value_store_url


class AlertLoginProvider(C42ApiV3TokenProvider):
    def __init__(self, auth_session, key_value_store_client):
        super(AlertLoginProvider, self).__init__(auth_session)
        self._key_value_store_client = key_value_store_client

    def get_target_host_address(self):
        return _get_url_from_key_value_store(self._key_value_store_client, u"AlertService-API_URL")


class EmployeeCaseManagementLoginProvider(C42ApiV3TokenProvider):
    def __init__(self, auth_session, key_value_store_client):
        super(EmployeeCaseManagementLoginProvider, self).__init__(auth_session)
        self._key_value_store_client = key_value_store_client

    def get_target_host_address(self):
        return _get_url_from_key_value_store(
            self._key_value_store_client, u"employeecasemanagement-API_URL"
        )


def _get_sts_base_url(session):
    uri = u"/api/ServerEnv"
    try:
        response = session.get(uri)
    except Exception as ex:
        message = (
            u"An error occurred while requesting server environment information, caused by {0}"
        )
        message = message.format(ex)
        raise Exception(message)

    sts_base_url = None
    if response.text:
        response_json = json.loads(response.text)
        if u"stsBaseUrl" in response_json:
            sts_base_url = response_json[u"stsBaseUrl"]
    if not sts_base_url:
        raise Exception(u"stsBaseUrl not found.")
    return sts_base_url


def _get_url_from_key_value_store(key_value_store, url_key):
    try:
        response = key_value_store.get_stored_value(url_key)
    except Exception as ex:
        message = u"An error occurred while requesting a URL from simple key value store"
        message = u"{0}, caused by {1}".format(message, ex)
        raise Exception(message)

    return response.text
