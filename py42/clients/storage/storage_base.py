from py42._internal import session_factory
from py42.clients.shared.authentication import AuthenticationClient


class StorageTargetedClient(AuthenticationClient):
    @classmethod
    def create_using_tmp_storage_token_requester(cls, host_address, tmp_storage_token_requester_func, is_async=False):
        session = session_factory.create_tmp_storage_login_token_session(host_address, tmp_storage_token_requester_func,
                                                                         is_async=is_async)
        return cls(session)
