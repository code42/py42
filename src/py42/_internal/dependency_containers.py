from py42._internal.archive_access import ArchiveAccessorManager
from py42._internal.client_factories import (
    AuthorityClientFactory,
    FileEventClientFactory,
    StorageClientFactory,
    KeyValueStoreClientFactory,
    AlertClientFactory,
    EmployeeCaseManagementClientFactory,
)
from py42._internal.login_provider_factories import (
    ArchiveLocatorFactory,
    FileEventLoginProviderFactory,
    AlertLoginProviderFactory,
    KeyValueStoreLocatorFactory,
    EmployeeCaseManagementLoginProviderFactory,
)
from py42._internal.modules import (
    archive as archive_module,
    security as sec_module,
    employee_case_management as ecm_module,
)
from py42._internal.user_context import UserContext
from py42._internal.session import Py42Session
from py42._internal.session_factory import SessionFactory
from py42._internal.storage_session_manager import StorageSessionManager


class AuthorityDependencies(object):
    def __init__(self, session_factory, root_session):
        # type: (SessionFactory, Py42Session) -> None
        self._set_sessions(session_factory, root_session)
        default_session = self.default_session
        v3_required_session = self.v3_required_session

        # authority clients
        authority_client_factory = AuthorityClientFactory(default_session, v3_required_session)
        self.session_factory = session_factory
        self.administration_client = authority_client_factory.create_administration_client()
        self.user_client = authority_client_factory.create_user_client()
        self.device_client = authority_client_factory.create_device_client()
        self.org_client = authority_client_factory.create_org_client()
        self.legal_hold_client = authority_client_factory.create_legal_hold_client()
        self.archive_client = authority_client_factory.create_archive_client()
        self.security_client = authority_client_factory.create_security_client()
        self.user_context = UserContext(self.administration_client)

    def _set_sessions(self, session_factory, root_session):
        # type: (SessionFactory, Py42Session) -> None
        self.root_session = root_session
        v3_session = session_factory.create_jwt_session(root_session)
        v1_session = session_factory.create_v1_session(root_session)
        sessions = [v3_session, v1_session]
        selected_session_idx = self._select_first_valid_session_idx(sessions, u"/api/User/my")

        selected_session = sessions[selected_session_idx]

        # some older versions of C42 Server have v3 APIs that support JWT tokens while the V1 api does not.
        if selected_session is not v3_session:
            v3_required_session = v3_session
        else:
            v3_required_session = selected_session

        self.default_session = selected_session
        self.v3_required_session = v3_required_session
        self.storage_sessions_manager = StorageSessionManager(session_factory)

    @staticmethod
    def verify_session_supported(session, test_uri):
        try:
            response = session.get(test_uri)
            return 200 <= response.status_code < 300
        except Exception:
            return False

    @staticmethod
    def _select_first_valid_session_idx(session_list, test_uri):
        host_address = None
        for idx, session in enumerate(session_list):
            host_address = session.host_address
            if AuthorityDependencies.verify_session_supported(session, test_uri):
                return idx

        message = (
            u"Invalid credentials or host address ({0}). Check that the username and password are correct, that the "
            u"host is available and reachable, and that you have supplied the full scheme, domain, and port "
            u"(e.g. https://myhost.code42.com:4285). If you are using a self-signed ssl certificate, try setting "
            u"py42.settings.verify_ssl_certs to false (or using a cert from a legitimate certificate "
            u"authority).".format(host_address)
        )
        raise Exception(message)


class StorageDependencies(object):
    def __init__(self, authority_dependencies, archive_locator_factory):
        # type: (AuthorityDependencies, ArchiveLocatorFactory) -> None
        self.storage_client_factory = StorageClientFactory(
            authority_dependencies.storage_sessions_manager, archive_locator_factory
        )


class FileEventDependencies(object):
    def __init__(self, authority_dependencies):
        # type: (AuthorityDependencies) -> None
        file_event_login_provider_factory = FileEventLoginProviderFactory(
            authority_dependencies.root_session
        )
        self.file_event_client_factory = FileEventClientFactory(
            authority_dependencies.session_factory, file_event_login_provider_factory
        )


class AlertDependencies(object):
    def __init__(self, authority_dependencies, key_value_store_client_factory):
        # type: (AuthorityDependencies, KeyValueStoreClientFactory) -> None
        alert_login_provider_factory = AlertLoginProviderFactory(
            authority_dependencies.root_session, key_value_store_client_factory
        )
        self.alert_client_factory = AlertClientFactory(
            authority_dependencies.session_factory,
            alert_login_provider_factory,
            authority_dependencies.user_context,
        )


class KeyValueStoreDependencies(object):
    def __init__(self, authority_dependencies):
        # type: (AuthorityDependencies) -> None
        key_value_store_login_provider_factory = KeyValueStoreLocatorFactory(
            authority_dependencies.root_session
        )
        self.key_value_store_client_factory = KeyValueStoreClientFactory(
            authority_dependencies.session_factory, key_value_store_login_provider_factory
        )


class EmployeeCaseManagementDependencies(object):
    def __init__(self, authority_dependencies, key_value_store_client_factory):
        # type: (AuthorityDependencies, KeyValueStoreClientFactory) -> None
        ecm_login_provider_factory = EmployeeCaseManagementLoginProviderFactory(
            authority_dependencies.root_session, key_value_store_client_factory
        )
        self.employee_case_management_client_factory = EmployeeCaseManagementClientFactory(
            authority_dependencies.session_factory,
            ecm_login_provider_factory,
            authority_dependencies.user_context,
        )


class SDKDependencies(object):
    def __init__(
        self,
        authority_dependencies,
        storage_dependencies,
        file_event_dependencies,
        employee_case_management_dependencies,
        alert_dependencies,
        key_value_store_dependencies,
    ):
        # type: (AuthorityDependencies, StorageDependencies, FileEventDependencies, EmployeeCaseManagementDependencies, AlertDependencies, KeyValueStoreDependencies) -> None
        archive_client = authority_dependencies.archive_client
        security_client = authority_dependencies.security_client
        storage_client_factory = storage_dependencies.storage_client_factory
        file_event_client_factory = file_event_dependencies.file_event_client_factory

        self.authority_dependencies = authority_dependencies
        self.storage_dependencies = storage_dependencies
        self.file_event_dependencies = file_event_dependencies
        self.ecm_dependencies = employee_case_management_dependencies
        self.alert_dependencies = alert_dependencies

        archive_accessor_manager = ArchiveAccessorManager(archive_client, storage_client_factory)

        # modules (feature sets that combine info from multiple clients)
        self.archive_module = archive_module.ArchiveModule(archive_accessor_manager, archive_client)
        self.security_module = sec_module.SecurityModule(
            security_client,
            storage_client_factory,
            file_event_client_factory,
            alert_dependencies.alert_client_factory,
        )
        self.employee_case_management_module = ecm_module.EmployeeCaseManagementModule(
            self.ecm_dependencies.employee_case_management_client_factory
        )

    @classmethod
    def create_c42_api_dependencies(cls, session_factory, root_session):
        # type: (type, SessionFactory, Py42Session) -> SDKDependencies
        # this configuration is for using c42-hosted endpoints to get v3 or v1 authentication tokens.
        authority_dependencies = AuthorityDependencies(session_factory, root_session)
        default_session = authority_dependencies.default_session
        security_client = authority_dependencies.security_client
        device_client = authority_dependencies.device_client
        key_value_store_dependencies = KeyValueStoreDependencies(authority_dependencies)
        archive_locator_factory = ArchiveLocatorFactory(
            default_session, security_client, device_client
        )
        key_value_store_client_factory = key_value_store_dependencies.key_value_store_client_factory
        ecm_dependencies = EmployeeCaseManagementDependencies(
            authority_dependencies, key_value_store_client_factory
        )
        alert_dependencies = AlertDependencies(
            authority_dependencies, key_value_store_client_factory
        )
        storage_dependencies = StorageDependencies(authority_dependencies, archive_locator_factory)
        file_event_dependencies = FileEventDependencies(authority_dependencies)
        key_value_store_dependencies = KeyValueStoreDependencies(authority_dependencies)

        return cls(
            authority_dependencies,
            storage_dependencies,
            file_event_dependencies,
            ecm_dependencies,
            alert_dependencies,
            key_value_store_dependencies,
        )
