from py42._internal.auth_handling import (
    AuthHandler,
    CompositeModifier,
    CookieModifier,
    HeaderModifier,
)
from py42._internal.login_providers import (
    BasicAuthProvider,
    C42ApiV1TokenProvider,
    C42ApiV3TokenProvider,
)
from py42._internal.session import Py42Session


class SessionFactory(object):
    def __init__(self, session_impl, session_modifier_factory, auth_handler_factory):
        self._session_impl = session_impl
        self._session_modifier_factory = session_modifier_factory
        self._auth_handler_factory = auth_handler_factory

    def create_basic_auth_session(self, host_address, username, password):
        provider = BasicAuthProvider(host_address, username, password)
        header_modifier = self._session_modifier_factory.create_header_modifier(u"Basic {0}")
        return self._create_session(self._session_impl, provider, header_modifier)

    def create_v1_session(self, parent_session):
        provider = C42ApiV1TokenProvider(parent_session)
        header_modifier = self._session_modifier_factory.create_header_modifier(u"token {0}")
        return self._create_session(self._session_impl, provider, header_modifier)

    def create_jwt_session(self, parent_session):
        provider = C42ApiV3TokenProvider(parent_session)
        header_modifier = self._session_modifier_factory.create_v3_session_modifier()
        return self._create_session(self._session_impl, provider, header_modifier)

    def create_storage_session(self, c42_api_login_provider):
        header_modifier = self._session_modifier_factory.create_header_modifier(u"login_token {0}")
        tmp = self._create_session(self._session_impl, c42_api_login_provider, header_modifier)
        return self.create_v1_session(tmp)

    def create_jwt_session_from_provider(self, login_provider):
        header_modifier = self._session_modifier_factory.create_v3_session_modifier()
        return self._create_session(self._session_impl, login_provider, header_modifier)

    def create_key_value_store_session(self, key_value_store_login_provider):
        return self._create_session(self._session_impl, key_value_store_login_provider)

    def _create_session(self, session_impl, login_provider, modifier=None):
        handler = None
        host_address = login_provider.get_target_host_address()
        if modifier:
            handler = self._auth_handler_factory.create_auth_handler(login_provider, modifier)
        return Py42Session(session_impl(), host_address, auth_handler=handler)


class SessionModifierFactory(object):
    @staticmethod
    def create_header_modifier(value_format):
        return HeaderModifier(value_format=value_format)

    def create_v3_session_modifier(self):
        header_modifier = self.create_header_modifier(u"v3_user_token {0}")
        cookie_modifier = CookieModifier(u"C42_JWT_API_TOKEN")
        return CompositeModifier([header_modifier, cookie_modifier])


class AuthHandlerFactory(object):
    @staticmethod
    def create_auth_handler(login_provider, modifier=None):
        return AuthHandler(login_provider, modifier)
