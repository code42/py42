class AuthHandler(object):
    def __init__(self, secret_provider_func, secret_applier):
        self._secret_provider_func = secret_provider_func
        self._secret_applier = secret_applier
        self._initial_auth = True

    def handle_unauthorized(self, session):
        try:
            secret = self._secret_provider_func(force_refresh=not self._initial_auth)
            if self._initial_auth:
                self._initial_auth = False
            self._secret_applier.apply_secret(session, secret)
        except Exception as e:
            message = "An error occurred while trying to handle an unauthorized request, caused by: {0}"
            message = message.format(e.message)
            raise Exception(message)

    @staticmethod
    def response_indicates_unauthorized(response):
        return response.status_code == 401


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

    def __init__(self, header_name="Authorization", value_format="{0}"):
        self._header_name = header_name
        self._value_format = value_format

    def apply_secret(self, session, secret):
        try:
            session.headers.update({self._header_name: self._value_format.format(secret)})
        except Exception as e:
            message = "An error occurred while trying to apply a {0} header to the session, caused by: {1}"
            message = message.format(self._header_name, e.message)
            raise Exception(message)


class CookieApplier(SecretApplier):

    def __init__(self, cookie_name, value_format="{0}"):
        self._cookie_name = cookie_name
        self._value_format = value_format

    def apply_secret(self, session, secret):
        try:
            session.cookies.set(self._cookie_name, self._value_format.format(secret))
        except Exception as e:
            message = "An error occurred while trying to apply cookies to the session, caused by: {0}"
            message = message.format(e.message)
            raise Exception(message)
