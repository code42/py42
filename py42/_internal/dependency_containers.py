from py42._internal.archive_locator_factories import C42AuthorityArchiveLocatorFactory
from py42._internal.auth_strategies import C42AuthorityAuthStrategy
from py42._internal.base_classes import BaseArchiveLocatorFactory, BaseAuthStrategy
from py42._internal.clients import administration, archive, devices, legal_hold, orgs, restore, security, users
from py42._internal.generic_session import Session
from py42._internal.modules import restore as restore_module, security as sec_module
from py42._internal.modules.restore import FileDownloader
from py42._internal.storage_client_factory import StorageClientFactory
from py42._internal.storage_session_manager import StorageSessionManager


class AuthorityDependencies(object):

    def __init__(self, auth_strategy, root_session, is_async=False):
        # type: (BaseAuthStrategy, Session, bool) -> None
        self._set_sessions(auth_strategy, root_session, is_async=is_async)
        default_session = self.default_session
        v3_required_session = self.v3_required_session

        # authority clients
        self.administration_client = administration.AdministrationClient(default_session, v3_required_session)
        self.user_client = users.UserClient(default_session, v3_required_session)
        self.device_client = devices.DeviceClient(default_session, v3_required_session)
        self.org_client = orgs.OrgClient(default_session, v3_required_session)
        self.legal_hold_client = legal_hold.LegalHoldClient(default_session, v3_required_session)
        self.archive_client = archive.ArchiveClient(default_session, v3_required_session)
        self.restore_client = restore.RestoreClient(default_session, v3_required_session)
        self.security_client = security.SecurityClient(default_session, v3_required_session)

    def _set_sessions(self, auth_strategy, root_session, is_async=False):
        # type: (BaseAuthStrategy, Session, bool) -> None

        v3_session = auth_strategy.create_jwt_session(root_session)
        v1_session = auth_strategy.create_v1_session(root_session)
        sessions = [v3_session, v1_session]
        selected_session_idx = self._select_first_valid_session_idx(sessions, "/api/User/my")

        selected_session = sessions[selected_session_idx]

        # some older versions of C42 Server have v3 APIs that support JWT tokens while the V1 api does not.
        if selected_session is not v3_session:
            v3_required_session = v3_session
        else:
            v3_required_session = selected_session

        self.default_session = selected_session
        self.v3_required_session = v3_required_session
        self.storage_session_manager = StorageSessionManager(auth_strategy, is_async=is_async)

    @staticmethod
    def verify_session_supported(session, test_uri):
        try:
            response = session.get(test_uri, force_sync=True)
            return 200 <= response.status_code < 300
        except Exception:
            return False

    @staticmethod
    def _select_first_valid_session_idx(session_list, test_uri):
        for idx in range(len(session_list)):
            session = session_list[idx - 1]
            if AuthorityDependencies.verify_session_supported(session, test_uri):
                return idx

        message = "Invalid credentials or host address. Check that the username and password are correct, that the " \
                  "host is available and reachable, and that you have supplied the full scheme, domain, and port " \
                  "(e.g. https://myhost.code42.com:4285). If you are using a self-signed ssl certificate, try setting" \
                  "py42.settings.verify_ssl_certs to false (or using a cert from a legitimate certificate" \
                  " authority)."
        raise Exception(message)


class StorageDependencies(object):
    def __init__(self, authority_dependencies, archive_locator_factory):
        # type: (AuthorityDependencies, BaseArchiveLocatorFactory) -> None
        storage_session_manager = authority_dependencies.storage_session_manager
        self.storage_client_factory = StorageClientFactory(storage_session_manager, archive_locator_factory)


class SDKDependencies(object):

    def __init__(self, authority_dependencies, storage_dependencies):
        # type: (AuthorityDependencies, StorageDependencies) -> None
        archive_client = authority_dependencies.archive_client
        security_client = authority_dependencies.security_client
        storage_client_factory = storage_dependencies.storage_client_factory

        self.authority_dependencies = authority_dependencies
        self.storage_dependencies = storage_dependencies

        downloader = FileDownloader(archive_client, storage_client_factory)

        # modules (feature sets that combine info from multiple clients)
        self.security_module = sec_module.SecurityModule(security_client, storage_client_factory)
        self.restore_module = restore_module.RestoreModule(archive_client, storage_client_factory, downloader)

    @classmethod
    def create_c42_api_dependencies(cls, root_session, is_async=False):
        # type: (Session, bool) -> SDKDependencies
        # this configuration is for using c42-hosted endpoints to get v3 or v1 authentication tokens.
        auth_strategy = C42AuthorityAuthStrategy(is_async=is_async)
        authority_dependencies = AuthorityDependencies(auth_strategy, root_session)
        default_session = authority_dependencies.default_session
        security_client = authority_dependencies.security_client
        device_client = authority_dependencies.device_client

        archive_locator_factory = C42AuthorityArchiveLocatorFactory(default_session, security_client, device_client)

        storage_dependencies = StorageDependencies(authority_dependencies, archive_locator_factory)

        return cls(authority_dependencies, storage_dependencies)



