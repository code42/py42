import json
from .. import sessionfactory as sessionfactory
from ..shared.authentication import AuthenticationClient

V3_AUTH = "v3_user_token"
V3_COOKIE_NAME = "C42_JWT_API_TOKEN"


class AuthorityTargetedClient(AuthenticationClient):
    def __init__(self, default_session, v3_required=None):
        super(AuthorityTargetedClient, self).__init__(default_session)
        self._v3_required_session = v3_required or default_session

    @classmethod
    def create_from_local_logon(cls, host_address, username, password, is_async=False):
        token_requester = cls.create_with_basic_auth(host_address, username, password)
        authority_client = cls.create_with_token_auth(host_address, token_requester, is_async=is_async)
        return authority_client

    @classmethod
    def create_with_token_auth(cls, authority_address, token_requester, is_async=False):
        methods = [{"name": "V3", "func": sessionfactory.create_jwt_token_session},
                   {"name": "V1", "func": sessionfactory.create_v1_token_session}]
        for method in methods:
            try:
                session = method["func"](authority_address, token_requester)
                response = session.get("/api/User/my")
                v3_session = None
                if 200 <= response.status_code < 300:
                    if method["name"] != "V3":
                        v3_session = methods[0]["func"](authority_address, token_requester, is_async=is_async)
                    if is_async:
                        session = method["func"](authority_address, token_requester, is_async=is_async)
                    return cls(session, v3_session)
            except Exception as e:
                print e

        raise Exception(
            "Invalid credentials or host address. Check that the username and password are correct, that the" +
            " host is available and reachable, and that you have supplied the full scheme, domain, and port " +
            "(e.g. https://myhost.code42.com:4285).")

    def get_v3_user_token(self, use_body=True):
        uri = "/c42api/v3/auth/jwt"
        params = {"useBody": use_body}
        return self.get(uri, params=params)

    def get_storage_auth_token(self, plan_uid, destination_guid, **kwargs):
        uri = "/api/StorageAuthToken"
        data = {"planUid": plan_uid, "destinationGuid": destination_guid}

        return self.post(uri, data=json.dumps(data), **kwargs)

    def get_jwt_token_value(self):
        response = self.get_v3_user_token()
        if response.content:
            response_data = json.loads(response.content)["data"]
            token = str(response_data[V3_AUTH])
        else:
            # some older versions only return the v3 token in a cookie instead of a response header.
            token = self.session.cookies.get_dict().get(V3_COOKIE_NAME, None)

        return token

    def get_storage_logon_info(self, plan_uid, destination_guid):
        response = self.get_storage_auth_token(plan_uid, destination_guid)
        logon_info = json.loads(response.content)["data"]
        return logon_info

    def wait(self):
        super(AuthorityTargetedClient, self).wait()
        if "wait" in dir(self._v3_required_session):
            self._v3_required_session.wait()
