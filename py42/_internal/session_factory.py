from .http import generic_session_factory
from .http.handling import AuthHandler, CompositeApplier, CookieApplier, HeaderApplier


def create_jwt_token_session(host_address, jwt_token_provider_func, is_async=False):
    header_applier = HeaderApplier(value_format="v3_user_token {0}")
    cookie_applier = CookieApplier("C42_JWT_API_TOKEN")
    composite_applier = CompositeApplier([header_applier, cookie_applier])
    handler = AuthHandler(jwt_token_provider_func, composite_applier)
    session = generic_session_factory.create_session(host_address, handler=handler, is_async=is_async)
    return session


def create_v1_token_session(host_address, v1_token_provider_func, is_async=False):
    header_applier = HeaderApplier(value_format="token {0}")
    handler = AuthHandler(v1_token_provider_func, header_applier)
    session = generic_session_factory.create_session(host_address, handler=handler, is_async=is_async)
    return session


def create_tmp_storage_login_token_session(host_address, tmp_storage_login_token_provider_func, is_async=False):
    header_applier = HeaderApplier(value_format="login_Token {0}")
    handler = AuthHandler(tmp_storage_login_token_provider_func, header_applier)
    session = generic_session_factory.create_session(host_address, handler=handler, is_async=is_async)
    return session
