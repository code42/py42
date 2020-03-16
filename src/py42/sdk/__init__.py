from requests import Session

from py42._internal.initialization import SDKDependencies
from py42._internal.session_factory import (
    AuthHandlerFactory,
    SessionFactory,
    SessionModifierFactory,
)


def from_local_account(host_address, username, password):
    return SDKClient.from_local_account(host_address, username, password)


class SDKClient(object):
    def __init__(self, sdk_dependencies):
        self._sdk_dependencies = sdk_dependencies

    @classmethod
    def from_local_account(cls, host_address, username, password):
        session_impl = Session
        session_factory = SessionFactory(
            session_impl, SessionModifierFactory(), AuthHandlerFactory()
        )
        basic_auth_session = session_factory.create_basic_auth_session(
            host_address, username, password
        )
        sdk_dependencies = SDKDependencies(host_address, session_factory, basic_auth_session)
        return cls(sdk_dependencies)

    @property
    def storageaccess(self):
        return self._sdk_dependencies.storage_client_factory

    @property
    def serveradmin(self):
        return self._sdk_dependencies.administration_client

    @property
    def archive(self):
        return self._sdk_dependencies.archive_module

    @property
    def users(self):
        return self._sdk_dependencies.user_client

    @property
    def devices(self):
        return self._sdk_dependencies.device_client

    @property
    def orgs(self):
        return self._sdk_dependencies.org_client

    @property
    def legalhold(self):
        return self._sdk_dependencies.legal_hold_client

    @property
    def usercontext(self):
        return self._sdk_dependencies.user_context

    @property
    def securitydata(self):
        return self._sdk_dependencies.security_module

    @property
    def detectionlists(self):
        return self._sdk_dependencies.detection_lists_module
