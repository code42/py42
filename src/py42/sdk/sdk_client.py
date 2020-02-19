from requests import Session

from py42._internal.dependency_containers import SDKDependencies
from py42._internal.session_factory import (
    AuthHandlerFactory,
    SessionFactory,
    SessionModifierFactory,
)


class SDK(object):
    def __init__(self, sdk_dependencies):
        # type: (SDKDependencies) -> None
        self._sdk_dependencies = sdk_dependencies
        self._authority_dependencies = sdk_dependencies.authority_dependencies
        self._storage_dependencies = sdk_dependencies.storage_dependencies
        self._file_event_dependencies = sdk_dependencies.file_event_dependencies
        self._ecm_dependencies = sdk_dependencies.ecm_dependencies
        self._alert_dependencies = sdk_dependencies.alert_dependencies

    @classmethod
    def create_using_local_account(cls, host_address, username, password):
        session_impl = Session
        session_factory = SessionFactory(
            session_impl, SessionModifierFactory(), AuthHandlerFactory()
        )
        basic_auth_session = session_factory.create_basic_auth_session(
            host_address, username, password
        )
        sdk_dependencies = SDKDependencies.create_c42_api_dependencies(
            session_factory, basic_auth_session
        )
        return cls(sdk_dependencies)

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
    def user_context(self):
        return self._authority_dependencies.user_context

    @property
    def security(self):
        return self._sdk_dependencies.security_module

    @property
    def employee_case_management(self):
        return self._sdk_dependencies.employee_case_management_module
