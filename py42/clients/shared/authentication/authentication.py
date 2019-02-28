import json

from py42._internal.http.generic_client import GenericClient
from py42._internal import session_factory


class AuthenticationClient(GenericClient):

    @classmethod
    def create_with_v1_token_auth(cls, storage_address, token_requester, is_async=False):
        session = session_factory.create_v1_token_session(storage_address, token_requester.get_v1_token_value,
                                                          is_async=is_async)
        return cls(session)

    def get_v1_token(self):
        uri = "/api/AuthToken"
        return self.post(uri)

    def get_v1_token_value(self, **kwargs):
        try:
            response = self.get_v1_token()
            response_data = json.loads(response.content)["data"]
            token = "{0}-{1}".format(response_data[0], response_data[1])
            return token
        except Exception as e:
            message = "An error occurred while trying to retrieve a V1 auth token, caused by {0}"
            message = message.format(e.message)
            raise Exception(message)
