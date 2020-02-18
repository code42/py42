from py42._internal.clients import (
    administration,
    archive,
    devices,
    legal_hold,
    orgs,
    security,
    users,
)
from py42._internal.user_context import UserContext
from py42._internal.clients.employee_case_management.departing_employee import (
    DepartingEmployeeClient,
)
from py42._internal.clients.fileevent.file_event import FileEventClient
from py42._internal.clients.key_value_store import KeyValueStoreClient
from py42._internal.clients.storage.storage import StorageClient
from py42._internal.login_provider_factories import (
    ArchiveLocatorFactory,
    FileEventLoginProviderFactory,
    EmployeeCaseManagementLoginProviderFactory,
    AlertLoginProviderFactory,
    KeyValueStoreLocatorFactory,
)
from py42._internal.clients.alerts import AlertClient
from py42._internal.session_factory import SessionFactory
from py42._internal.storage_session_manager import StorageSessionManager


class AuthorityClientFactory(object):
    def __init__(self, default_session, v3_required_session):
        self.default_session = default_session
        self.v3_required_session = v3_required_session

    def create_administration_client(self):
        return administration.AdministrationClient(self.default_session, self.v3_required_session)

    def create_user_client(self):
        return users.UserClient(self.default_session, self.v3_required_session)

    def create_device_client(self):
        return devices.DeviceClient(self.default_session, self.v3_required_session)

    def create_org_client(self):
        return orgs.OrgClient(self.default_session, self.v3_required_session)

    def create_legal_hold_client(self):
        return legal_hold.LegalHoldClient(self.default_session, self.v3_required_session)

    def create_archive_client(self):
        return archive.ArchiveClient(self.default_session, self.v3_required_session)

    def create_security_client(self):
        return security.SecurityClient(self.default_session, self.v3_required_session)


class StorageClientFactory(object):
    def __init__(self, storage_session_manager, login_provider_factory):
        # type: (StorageSessionManager, ArchiveLocatorFactory) -> None
        self._storage_session_manager = storage_session_manager
        self._login_provider_factory = login_provider_factory

    def get_storage_client_from_device_guid(self, device_guid, destination_guid=None):
        login_provider = self._login_provider_factory.create_backup_archive_locator(
            device_guid, destination_guid
        )
        session = self._storage_session_manager.get_storage_session(login_provider)
        return StorageClient(session)

    def get_storage_client_from_plan_uid(self, plan_uid, destination_guid):
        login_provider = self._login_provider_factory.create_security_archive_locator(
            plan_uid, destination_guid
        )
        session = self._storage_session_manager.get_storage_session(login_provider)
        return StorageClient(session)


class FileEventClientFactory(object):
    def __init__(self, session_factory, login_provider_factory):
        # type: (SessionFactory, FileEventLoginProviderFactory) -> None
        self._session_factory = session_factory
        self._login_provider_factory = login_provider_factory

    def get_file_event_client(self):
        login_provider = self._login_provider_factory.create_file_event_login_provider()
        session = self._session_factory.create_jwt_session_from_provider(login_provider)
        return FileEventClient(session)


class KeyValueStoreClientFactory(object):
    def __init__(self, session_factory, login_provider_factory):
        # type: (SessionFactory, KeyValueStoreLocatorFactory) -> None
        self._session_factory = session_factory
        self._login_provider_factory = login_provider_factory

    def get_key_value_store_client(self):
        login_provider = self._login_provider_factory.create_key_value_store_locator()
        session = self._session_factory.create_key_value_store_session(login_provider)
        return KeyValueStoreClient(session)


class EmployeeCaseManagementClientFactory(object):
    def __init__(self, session_factory, login_provider_factory, user_context):
        # type: (SessionFactory, EmployeeCaseManagementLoginProviderFactory, UserContext) -> None
        self._session_factory = session_factory
        self._login_provider_factory = login_provider_factory
        self._user_context = user_context

    def get_departing_employee_client(self):
        login_provider = self._login_provider_factory.create_ecm_login_provider()
        session = self._session_factory.create_jwt_session_from_provider(login_provider)
        return DepartingEmployeeClient(session, self._user_context)


class AlertClientFactory(object):
    def __init__(self, session_factory, login_provider_factory, user_context):
        # type: (SessionFactory, AlertLoginProviderFactory, UserContext) -> None
        self._session_factory = session_factory
        self._login_provider_factory = login_provider_factory
        self._user_context = user_context

    def get_alert_client(self):
        login_provider = self._login_provider_factory.create_alert_login_provider()
        session = self._session_factory.create_jwt_session_from_provider(login_provider)
        return AlertClient(session, self._user_context)
