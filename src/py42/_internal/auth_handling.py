from py42._internal.compat import str


class TokenProvider(object):
    def get_secret_value(self, force_refresh=False):
        pass


class AuthHandler(object):
    def __init__(self, token_provider, session_modifier):
        self._token_provider = token_provider
        self._session_modifier = session_modifier

    def renew_authentication(self, session, use_cache=False):
        try:
            secret = self._token_provider.get_secret_value(force_refresh=not use_cache)
            self._session_modifier.modify_session(session, secret)
        except Exception as ex:
            message = (
                u"An error occurred while trying to handle an unauthorized request, caused by: {0}"
            )
            message = message.format(str(ex))
            raise Exception(message)

    @staticmethod
    def response_indicates_unauthorized(response):
        return response.status_code == 401


class HeaderModifier(object):
    def __init__(self, header_name=u"Authorization", value_format=u"{0}"):
        self._header_name = header_name
        self._value_format = value_format

    def modify_session(self, session, value):
        try:
            session.headers.update({self._header_name: self._value_format.format(value)})
        except Exception as ex:
            message = u"An error occurred while trying to apply a {0} header to the session, caused by: {1}"
            message = message.format(self._header_name, str(ex))
            raise Exception(message)
