from .http.authhandling import HeaderApplier, CookieApplier, CompositeApplier, AuthHandler
from .secretproviders import JWTTokenProvider, V1TokenProvider, TmpStorageTokenProvider
from .http import sessionfactory


def create_jwt_token_session(host_address, jwt_token_requester, is_async=False):
    secret_fetcher = JWTTokenProvider(jwt_token_requester)
    header_applier = HeaderApplier(value_format="v3_user_token {}")
    cookie_applier = CookieApplier("C42_JWT_API_TOKEN")
    composite_applier = CompositeApplier([header_applier, cookie_applier])
    handler = AuthHandler(secret_fetcher, composite_applier)
    session = sessionfactory.create_session(host_address, handler=handler, is_async=is_async)
    return session


def create_v1_token_session(host_address, v1_token_requester, is_async=False):
    secret_fetcher = V1TokenProvider(v1_token_requester)
    header_applier = HeaderApplier(value_format="token {}")
    handler = AuthHandler(secret_fetcher, header_applier)
    session = sessionfactory.create_session(host_address, handler=handler, is_async=is_async)
    return session


def create_tmp_login_session_from_plan_info(storage_location_requester, plan_uid, destination_guid, is_async=False):
    secret_fetcher = TmpStorageTokenProvider(storage_location_requester, plan_uid, destination_guid)
    header_applier = HeaderApplier(value_format="login_Token {}")
    handler = AuthHandler(secret_fetcher, header_applier)
    storage_url = secret_fetcher.get_storage_logon_info().get("serverUrl")
    session = sessionfactory.create_session(storage_url, handler=handler, is_async=is_async)
    return session
