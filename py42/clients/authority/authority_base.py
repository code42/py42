import json

from py42._internal import session_factory
from py42.clients.shared.authentication import AuthenticationClient

V3_AUTH = "v3_user_token"
V3_COOKIE_NAME = "C42_JWT_API_TOKEN"


class AuthorityTargetedClient(AuthenticationClient):
    def __init__(self, default_session, v3_required=None):
        super(AuthorityTargetedClient, self).__init__(default_session)
        self._v3_required_session = v3_required or default_session

    @classmethod
    def create_using_local_account(cls, host_address, username, password, is_async=False):
        token_requester = cls.create_with_basic_auth(host_address, username, password)
        authority_client = cls.create_using_token_requester(host_address, token_requester, is_async=is_async)
        return authority_client

    @classmethod
    def create_using_token_requester(cls, authority_address, token_requester, is_async=False):
        methods = [{"name": "V3", "func": session_factory.create_jwt_token_session,
                    "retriever": token_requester.get_jwt_token_value},
                   {"name": "V1", "func": session_factory.create_v1_token_session,
                    "retriever": token_requester.get_v1_token_value}]
        for method in methods:
            try:
                session = method["func"](authority_address, method["retriever"])
                response = session.get("/api/User/my")
                v3_session = None
                if 200 <= response.status_code < 300:
                    if method["name"] != "V3":
                        v3_session = methods[0]["func"](authority_address, methods[0]["retriever"], is_async=is_async)
                    if is_async:
                        session = method["func"](authority_address, method["retriever"], is_async=is_async)
                    return cls(session, v3_session)
            except:
                pass

        message = "Invalid credentials or host address. Check that the username and password are correct, that the " \
                  "host is available and reachable, and that you have supplied the full scheme, domain, and port " \
                  "(e.g. https://myhost.code42.com:4285). If you are using a self-signed ssl certificate, try setting" \
                  "py42.http.settings.verify_ssl_certs to false (or using a cert from a legitimate certificate" \
                  " authority)."
        raise Exception(message)

    def get_v3_user_token(self, use_body=True):
        uri = "/c42api/v3/auth/jwt"
        params = {"useBody": use_body}
        return self.get(uri, params=params)

    def get_storage_auth_token_using_plan_info(self, plan_uid, destination_guid, **kwargs):
        uri = "/api/StorageAuthToken"
        data = {"planUid": plan_uid, "destinationGuid": destination_guid}

        return self.post(uri, data=json.dumps(data), **kwargs)

    def get_jwt_token_value(self, **kwargs):
        try:
            response = self.get_v3_user_token()
            if response.content:
                response_data = json.loads(response.content)["data"]
                token = str(response_data[V3_AUTH])
            else:
                # some older versions only return the v3 token in a cookie instead of a response header.
                token = self.cookies.get_dict().get(V3_COOKIE_NAME, None)

            return token
        except Exception as e:
            message = "An error occurred while trying to retrieve a jwt token, caused by {0}"
            message = message.format(e.message)
            raise Exception(message)

    def get_storage_logon_info_using_plan_info(self, plan_uid, destination_guid):
        try:
            response = self.get_storage_auth_token_using_plan_info(plan_uid, destination_guid)
            logon_info = json.loads(response.content)["data"]
            return logon_info
        except Exception as e:
            message = "An error occurred while trying to retrieve storage logon info, caused by {0}"
            message = message.format(e.message)
            raise Exception(message)

    def wait(self):
        super(AuthorityTargetedClient, self).wait()
        if "wait" in dir(self._v3_required_session):
            self._v3_required_session.wait()
