from py42._internal.base_classes import BaseArchiveLocatorFactory
from py42._internal.clients import administration, archive, devices, legal_hold, orgs, security, users
from py42._internal.clients.fileevent.file_event import FileEventClient
from py42._internal.clients.storage.storage import StorageClient
from py42._internal.login_provider_factories import FileEventLoginProviderFactory
from py42._internal.session_manager import SessionsManager


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
    def __init__(self, session_manager, login_provider_factory):
        # type: (SessionsManager, BaseArchiveLocatorFactory) -> None
        self._session_manager = session_manager
        self._login_provider_factory = login_provider_factory

    def create_backup_client(self, *args, **kwargs):
        login_provider = self._login_provider_factory.create_backup_archive_locator(*args, **kwargs)
        session = self._session_manager.get_storage_session(login_provider)
        return StorageClient(session)

    def create_security_plan_clients(self, *args, **kwargs):
        login_providers = self._login_provider_factory.create_security_archive_locators(*args, **kwargs)
        sessions = [self._session_manager.get_storage_session(provider) for provider in login_providers]
        clients = [StorageClient(session) for session in sessions]
        return clients


class FileEventClientFactory(object):
    def __init__(self, session_manager, login_provider_factory):
        # type: (SessionsManager, FileEventLoginProviderFactory) -> None
        self._session_manager = session_manager
        self._login_provider_factory = login_provider_factory

    def create_file_event_client(self):
        login_provider = self._login_provider_factory.create_file_event_login_provider()
        session = self._session_manager.get_file_event_session(login_provider)
        return FileEventClient(session)
