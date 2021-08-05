from py42.response import Py42Response


class LoginConfigurationClient:
    def __init__(self, connection):
        self._connection = connection

    def get_for_user(self, username):
        uri = "{}/c42api/v3/LoginConfiguration".format(self._connection.host_address)
        response = self._connection._session.get(uri, params={"username": username})
        return Py42Response(response)
