from py42._internal.async_session import Py42AsyncSession
from py42._internal.auth_handling import AuthHandler, CompositeModifier, CookieModifier, HeaderModifier
from py42._internal.session import Py42Session
from py42._internal.login_providers import BasicAuthProvider


def create_auth_handling_session(session_impl, login_provider, modifier, is_async=False):
    session_type = Py42AsyncSession if is_async else Py42Session
    host_address = login_provider.get_target_host_address()
    handler = AuthHandler(login_provider, modifier)
    return session_type(session_impl(), host_address, auth_handler=handler)


def create_basic_auth_session(session_impl, host_address, username, password, is_async=False):
    provider = BasicAuthProvider(host_address, username, password)
    header_modifier = HeaderModifier(value_format="Basic {0}")
    return create_auth_handling_session(session_impl, provider, header_modifier, is_async=is_async)


def create_c42api_v1_session(session_impl, c42_api_login_provider, is_async=False):
    header_modifier = HeaderModifier(value_format="token {0}")
    return create_auth_handling_session(session_impl, c42_api_login_provider, header_modifier, is_async=is_async)


def create_c42api_v3_session(session_impl, c42_api_login_provider, is_async=False):
    header_modifier = HeaderModifier(value_format="v3_user_token {0}")
    cookie_modifier = CookieModifier("C42_JWT_API_TOKEN")
    composite_modifier = CompositeModifier([header_modifier, cookie_modifier])
    return create_auth_handling_session(session_impl, c42_api_login_provider, composite_modifier, is_async=is_async)


def create_c42api_tmp_storage_session(session_impl, c42_api_login_provider, is_async=False):
    header_modifier = HeaderModifier(value_format="login_token {0}")
    return create_auth_handling_session(session_impl, c42_api_login_provider, header_modifier, is_async=is_async)
