from .authority_api import AuthorityAPIClient
from .handlers import V1AuthHandler, V3AuthHandler
from .handlers.http import Session, BasicAuthHandler
from code42.sdk.sdkutil import create_session


def build_credentials_based_authority_client(host_address, username, password, proxies, is_async):
    basic_session = Session(host_address, auth_handler=BasicAuthHandler(username, password))
    available_handlers = [V3AuthHandler(auth_session=basic_session),
                          V1AuthHandler(auth_session=basic_session)]

    for handler in available_handlers:
        try:
            session = Session(host_address, auth_handler=handler, proxies=proxies)
            client = AuthorityAPIClient(session)
            response = client.get_current_user()
            if 200 <= response.status_code < 300:
                if is_async:
                    session = create_session(host_address, handler, proxies, True)

                if isinstance(handler, V1AuthHandler):
                    v3_handler = available_handlers[0]
                    v3_session = Session(host_address, auth_handler=v3_handler, proxies=proxies)
                    if is_async:
                        v3_session = create_session(host_address, v3_handler, proxies, True)
                    client = AuthorityAPIClient(session, v3_session)
                else:
                    client = AuthorityAPIClient(session)

                return client
        except Exception as e:
            pass
    raise Exception("Invalid credentials or host address. Check that the username and password are correct, that the" +
                    " host is available and reachable, and that you have supplied the full scheme, domain, and port " +
                    "(e.g. https://myhost.code42.com:4285).")
