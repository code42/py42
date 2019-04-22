from threading import Lock


class LoginProvider(object):
    def get_target_host_address(self):
        pass

    def get_secret_value(self, force_refresh=False):
        pass


class AuthHandler(object):
    def __init__(self, login_provider, session_modifier):
        self._login_provider = login_provider
        self._session_modifier = session_modifier
        self._auth_is_valid = False
        self._auth_lock = Lock()
        self._initial_auth = True

    def try_authorize(self, session, response=None):
        # returns whether or not re-authorization was needed
        if self._response_indicates_unauthorized(response):
            self._auth_is_valid = False
            with self._auth_lock:
                if not self._auth_is_valid:
                    self._handle_unauthorized(session)
            # if multiple threads needed re-auth, return true for all of them even though
            # only one of them actually did the work of re-authing.
            return True
        return False

    def _handle_unauthorized(self, session):
        try:
            secret = self._login_provider.get_secret_value(force_refresh=not self._initial_auth)
            if self._initial_auth:
                self._initial_auth = False
            self._session_modifier.modify_session(session, secret)
            self._auth_is_valid = True
        except Exception as e:
            message = "An error occurred while trying to handle an unauthorized request, caused by: {0}"
            message = message.format(e.message)
            raise Exception(message)

    def _response_indicates_unauthorized(self, response):
        return self._initial_auth or (response is not None and response.status_code == 401)


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
