from code42.http import Session, MissingHeaderHandler
from code42.util.constants import *
import json


class V1AuthHandler(MissingHeaderHandler):

    def _fetch_header_value(self):
        try:
            response = self._auth_session.post("/api/AuthToken")
            response_data = json.loads(response.content)["data"]
            token = str(response_data[0]) + "-" + str(response_data[1])
            return V1_AUTH + " " + token

        except Exception as e:
            message = "Failed to retrieve v1 token from authority: " + self._auth_session.host_address
            raise Exception(message + ", caused by: " + e.message)


class V1StorageNodeAuthHandler(MissingHeaderHandler):

    def __init__(self, authority_api, plan_uid, destination_guid, initial_logon_info=None):
        super(V1StorageNodeAuthHandler, self).__init__(auth_session=authority_api)
        self._plan_uid = plan_uid
        self._destination_guid = destination_guid
        self._storage_auth_session = None
        self._initial_logon_info = initial_logon_info
        self._is_initial_logon = True

    def _get_perm_token_from_tmp_login(self, server_url, tmp_login_token):
        try:
            if self._storage_auth_session is None:
                self._storage_auth_session = Session(server_url, proxies=self._auth_session.proxies)

            response = self._storage_auth_session.post("/api/AuthToken",
                                                       headers={"Authorization": "login_Token %s" % tmp_login_token})

            response_data = json.loads(response.content)["data"]
            token = str(response_data[0]) + "-" + str(response_data[1])

            return token
        except Exception as e:
            message = "Failed to retrieve permanent v1 login token from storage node: " + server_url
            raise Exception(message + ", caused by: " + e.message)

    def _fetch_header_value(self):
        try:
            if self._is_initial_logon:
                logon_info = self._initial_logon_info
                self._is_initial_logon = False
            else:
                response = self._auth_session.storage_auth_token(self._plan_uid, self._destination_guid)
                logon_info = json.loads(response.content)["data"]

            tmp_token = logon_info["loginToken"]
            server_url = logon_info["serverUrl"]

            header_value = V1_AUTH + " " + self._get_perm_token_from_tmp_login(server_url, tmp_token)

            return header_value

        except Exception as e:
            message = "Failed to renew v1 auth token for planUid: " + self._plan_uid + "," \
                      "destinationGuid: " + self._destination_guid
            raise Exception(message + ", caused by: " + e.message)


class V3AuthHandler(MissingHeaderHandler):

    def _fetch_header_value(self):
        try:
            response = self._auth_session.get("/c42api/v3/auth/jwt?useBody=true")
            if response.content:
                response_data = json.loads(response.content)["data"]
                token = str(response_data[V3_AUTH])
            else:
                # some older versions only return the v3 token in a cookie instead of a response header.
                token = self._auth_session.cookies.get_dict().get("C42_JWT_API_TOKEN", None)

            return V3_AUTH + " " + token
        except Exception as e:
            message = "Failed to retrieve v3 user token from authority: " + self._auth_session.host_address
            raise Exception(message + ", caused by: " + e.message)

    def handle_unauthorized(self, session):
        super(V3AuthHandler, self).handle_unauthorized(session)
        auth_string = session.headers.get(self._header_name)
        if auth_string is not None:
            # some older versions need the token to be sent in a cookie instead of a request header.
            token = auth_string.split(V3_AUTH + " ")[1]
            session.cookies.set("C42_JWT_API_TOKEN", token)
