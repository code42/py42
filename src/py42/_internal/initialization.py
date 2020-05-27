from py42._internal.archive_access import ArchiveAccessorManager
from py42._internal.client_factories import AuthorityClientFactory, MicroserviceClientFactory
from py42._internal.clients.storage import StorageClientFactory
from py42._internal.storage_session_manager import StorageSessionManager
from py42._internal.token_providers import StorageTokenProviderFactory
from py42.modules import (
    alerts,
    archive as archive_module,
    detectionlists,
    securitydata as sec_module,
)
from py42.usercontext import UserContext


def _get_storage_client_factory(session_factory, archive_locator_factory):
    storage_session_manager = StorageSessionManager(session_factory)
    return StorageClientFactory(storage_session_manager, archive_locator_factory)


class SDKDependencies(object):
    def __init__(self, host_address, session_factory, root_session):
        self._set_v3_session(host_address, session_factory, root_session)

        # authority clients
        authority_client_factory = AuthorityClientFactory(self.session)
        self.administration_client = authority_client_factory.create_administration_client()
        self.user_client = authority_client_factory.create_user_client()
        self.device_client = authority_client_factory.create_device_client()
        self.org_client = authority_client_factory.create_org_client()
        self.legal_hold_client = authority_client_factory.create_legal_hold_client()
        self.archive_client = authority_client_factory.create_archive_client()
        self.security_client = authority_client_factory.create_security_client()
        self.user_context = UserContext(self.administration_client)

        archive_locator_factory = StorageTokenProviderFactory(
            self.session, self.security_client, self.device_client
        )

        self.storage_client_factory = _get_storage_client_factory(
            session_factory, archive_locator_factory
        )

        archive_accessor_manager = ArchiveAccessorManager(
            self.archive_client, self.storage_client_factory
        )

        microservice_client_factory = MicroserviceClientFactory(
            host_address, root_session, session_factory, self.user_context, self.user_client
        )

        # modules (feature sets that combine info from multiple clients)
        self.archive_module = archive_module.ArchiveModule(
            archive_accessor_manager, self.archive_client
        )
        self.security_module = sec_module.SecurityModule(
            self.security_client, self.storage_client_factory, microservice_client_factory
        )
        self.detection_lists_module = detectionlists.DetectionListsModule(
            microservice_client_factory
        )

        self.alerts_module = alerts.AlertsModule(microservice_client_factory)

    def _set_v3_session(self, host_address, session_factory, root_session):
        self.root_session = root_session
        self.session = session_factory.create_jwt_session(host_address, root_session)
        self._test_session(self.session, u"/api/User/my")

    @staticmethod
    def _test_session(session, test_uri):
        response = session.get(test_uri)
        return 200 <= response.status_code < 300
