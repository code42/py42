from py42._internal.auth_handling import AuthHandler, HeaderModifier
from py42._internal.session import Py42Session
from py42._internal.token_providers import (
    BasicAuthProvider,
    C42ApiV1TokenProvider,
    C42ApiV3TokenProvider,
)


class SessionFactory(object):
    def __init__(self, session_impl, session_modifier_factory, auth_handler_factory):
        self._session_impl = session_impl
        self._session_modifier_factory = session_modifier_factory
        self._auth_handler_factory = auth_handler_factory

    def create_basic_auth_session(self, host_address, username, password):
        provider = BasicAuthProvider(username, password)
        header_modifier = self._session_modifier_factory.create_header_modifier(u"Basic {0}")
        return self._create_session(self._session_impl, host_address, provider, header_modifier)

    def create_v1_session(self, host_address, parent_session):
        provider = C42ApiV1TokenProvider(parent_session)
        header_modifier = self._session_modifier_factory.create_header_modifier(u"token {0}")
        return self._create_session(self._session_impl, host_address, provider, header_modifier)

    def create_jwt_session(self, host_address, parent_session):
        provider = C42ApiV3TokenProvider(parent_session)
        header_modifier = self._session_modifier_factory.create_header_modifier(
            u"v3_user_token {0}"
        )
        return self._create_session(self._session_impl, host_address, provider, header_modifier)

    def create_storage_session(self, host_address, c42_api_token_provider):
        header_modifier = self._session_modifier_factory.create_header_modifier(u"login_token {0}")
        tmp = self._create_session(
            self._session_impl, host_address, c42_api_token_provider, header_modifier
        )
        return self.create_v1_session(host_address, tmp)

    def create_anonymous_session(self, host_address):
        return self._create_session(self._session_impl, host_address)

    def _create_session(self, session_impl, host_address, token_provider=None, modifier=None):
        handler = None
        if modifier:
            handler = self._auth_handler_factory.create_auth_handler(token_provider, modifier)
        return Py42Session(session_impl(), host_address, auth_handler=handler)


class SessionModifierFactory(object):
    @staticmethod
    def create_header_modifier(value_format):
        return HeaderModifier(value_format=value_format)


class AuthHandlerFactory(object):
    @staticmethod
    def create_auth_handler(token_provider, modifier=None):
        return AuthHandler(token_provider, modifier)
