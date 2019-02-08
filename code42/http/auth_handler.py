import base64


class AuthHandler(object):

    def handle_unauthorized(self, session):
        pass

    @staticmethod
    def response_indicates_unauthorized(response):
        return response.status_code == 401


class MissingHeaderHandler(AuthHandler):

    def __init__(self, auth_session=None, header_name="Authorization"):
        self._auth_session = auth_session
        self._header_name = header_name

    def _fetch_header_value(self):
        pass

    def handle_unauthorized(self, session):
        try:
            token_string = self._fetch_header_value()
            if token_string is not None:
                session.headers.update({self._header_name: token_string})
        except Exception as e:
            message = "Failed to apply header to request to " + session.host_address
            raise Exception(message + ", caused by: " + e.message)


class BasicAuthHandler(MissingHeaderHandler):
    def __init__(self, username, password):
        super(BasicAuthHandler, self).__init__()
        self._username = username
        self._password = password

    def _fetch_header_value(self):
        return "Basic " + base64.encodestring("%s:%s" % (self._username, self._password)).replace('\n', '')
