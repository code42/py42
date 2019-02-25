import json
from ...http.genericclient import GenericClient
from ... import sessionfactory


class AuthenticationClient(GenericClient):

    @classmethod
    def create_with_v1_token_auth(cls, storage_address, token_requester, is_async=False):
        session = sessionfactory.create_v1_token_session(storage_address, token_requester, is_async=is_async)
        return cls(session)

    def get_v1_token(self):
        uri = "/api/AuthToken"
        return self.post(uri)

    def get_v1_token_value(self):
        response = self.get_v1_token()
        response_data = json.loads(response.content)["data"]
        token = str(response_data[0]) + "-" + str(response_data[1])
        return token
