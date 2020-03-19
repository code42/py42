from py42.exceptions import Py42RequestError


class LoginProvider(object):
    def get_secret_value(self, force_refresh=False):
        pass


class AuthHandler(object):
    def __init__(self, login_provider, session_modifier):
        self._login_provider = login_provider
        self._session_modifier = session_modifier

    def renew_authentication(self, session, use_cache=False):
        try:
            secret = self._login_provider.get_secret_value(force_refresh=not use_cache)
            self._session_modifier.modify_session(session, secret)
        except Exception as ex:
            raise Py42RequestError(
                "An error occurred while trying to apply cookies to the session", ex
            )

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
    def __init__(self, header_name=u"Authorization", value_format=u"{0}"):
        self._header_name = header_name
        self._value_format = value_format

    def modify_session(self, session, value):
        session.headers.update({self._header_name: self._value_format.format(value)})


class CookieModifier(SessionModifier):
    def __init__(self, cookie_name, value_format=u"{0}"):
        self._cookie_name = cookie_name
        self._value_format = value_format

    def modify_session(self, session, value):
        session.cookies.set(self._cookie_name, self._value_format.format(value))
