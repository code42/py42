import base64


class AuthHandler(object):
    def __init__(self, secret_fetcher, secret_applier):
        self._secret_fetcher = secret_fetcher
        self._secret_applier = secret_applier

    def handle_unauthorized(self, session):
        secret = self._secret_fetcher.get_secret()
        self._secret_applier.apply_secret(session, secret)

    @staticmethod
    def response_indicates_unauthorized(response):
        return response.status_code == 401


class SecretProvider(object):
    def get_secret(self):
        pass


class SecretApplier(object):
    def apply_secret(self, session, secret):
        pass


class CompositeApplier(SecretApplier):
    def __init__(self, secret_applier_list):
        self.secret_applier_list = secret_applier_list

    def apply_secret(self, session, secret):
        for handler in self.secret_applier_list:
            handler.apply_secret(session, secret)


class HeaderApplier(SecretApplier):

    def __init__(self, header_name="Authorization", value_format="{}"):
        self._header_name = header_name
        self._value_format = value_format

    def apply_secret(self, session, secret):
        session.headers.update({self._header_name: self._value_format.format(secret)})


class CookieApplier(SecretApplier):

    def __init__(self, cookie_name, value_format="{}"):
        self._cookie_name = cookie_name
        self._value_format = value_format

    def apply_secret(self, session, secret):
        session.cookies.set(self._cookie_name, self._value_format.format(secret))


class BasicAuthProvider(SecretProvider):
    def __init__(self, username, password):
        self._username = username
        self._password = password
        self._secret_value = None

    def get_secret(self, renew=True):
        return base64.encodestring("%s:%s" % (self._username, self._password)).replace('\n', '')