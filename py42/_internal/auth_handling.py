
class LoginProvider(object):
    def get_target_host_address(self):
        pass

    def get_secret_value(self, force_refresh=False):
        pass


class AuthHandler(object):
    def __init__(self, login_provider, session_modifier):
        self._login_provider = login_provider
        self._session_modifier = session_modifier

    def renew_authentication(self, session, use_credential_cache=False):
        try:
            secret = self._login_provider.get_secret_value(force_refresh=not use_credential_cache)
            self._session_modifier.modify_session(session, secret)
        except Exception as e:
            message = "An error occurred while trying to handle an unauthorized request, caused by: {0}"
            message = message.format(e.message)
            raise Exception(message)

    @staticmethod
    def response_indicates_unauthorized(response):
        return response.status_code == 401


class SessionModifier(object):
    def modify_session(self, session, value):
        pass


class CompositeModifier(SessionModifier):
    def __init__(self, session_modifier_list):
        self._session_modifier_list = session_modifier_list

    def modify_session(self, session, value):
        for handler in self._session_modifier_list:
            handler.modify_session(session, value)


class HeaderModifier(SessionModifier):

    def __init__(self, header_name="Authorization", value_format="{0}"):
        self._header_name = header_name
        self._value_format = value_format

    def modify_session(self, session, value):
        try:
            session.headers.update({self._header_name: self._value_format.format(value)})
        except Exception as e:
            message = "An error occurred while trying to apply a {0} header to the session, caused by: {1}"
            message = message.format(self._header_name, e.message)
            raise Exception(message)


class CookieModifier(SessionModifier):

    def __init__(self, cookie_name, value_format="{0}"):
        self._cookie_name = cookie_name
        self._value_format = value_format

    def modify_session(self, session, value):
        try:
            session.cookies.set(self._cookie_name, self._value_format.format(value))
        except Exception as e:
            message = "An error occurred while trying to apply cookies to the session, caused by: {0}"
            message = message.format(e.message)
            raise Exception(message)
