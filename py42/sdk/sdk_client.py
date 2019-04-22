from requests import Session

import py42._internal.session_factory as session_factory
from py42._internal.dependency_containers import SDKDependencies


class SDK(object):

    def __init__(self, sdk_dependencies, is_async=False):
        # type: (SDKDependencies, bool) -> None
        self._is_async = is_async
        self._sdk_dependencies = sdk_dependencies
        self._authority_dependencies = sdk_dependencies.authority_dependencies
        self._storage_dependencies = sdk_dependencies.storage_dependencies

    @classmethod
    def create_using_local_account(cls, host_address, username, password, is_async=False):
        session_impl = Session
        basic_auth_session = session_factory.create_basic_auth_session(session_impl, host_address, username, password)
        sdk_dependencies = SDKDependencies.create_c42_api_dependencies(session_impl, basic_auth_session,
                                                                       is_async=is_async)
        return cls(sdk_dependencies, is_async=is_async)

    def wait(self):
        if self._is_async:
            self._authority_dependencies.default_session.wait()
            self._authority_dependencies.v3_required_session.wait()
            self._authority_dependencies.storage_session_manager.wait_all()

    @property
    def storage(self):
        return self._storage_dependencies.storage_client_factory

    @property
    def administration(self):
        return self._authority_dependencies.administration_client

    @property
    def archive(self):
        return self._sdk_dependencies.archive_module

    @property
    def users(self):
        return self._authority_dependencies.user_client

    @property
    def devices(self):
        return self._authority_dependencies.device_client

    @property
    def orgs(self):
        return self._authority_dependencies.org_client

    @property
    def legal_hold(self):
        return self._authority_dependencies.legal_hold_client

    @property
    def security(self):
        return self._sdk_dependencies.security_module
