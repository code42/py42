import json

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
from py42._internal.login_provider_factories import ArchiveLocatorFactory
from py42._internal.clients.alerts import AlertClient
from py42._internal.session_factory import SessionFactory
from py42._internal.storage_session_manager import StorageSessionManager


class AuthorityClientFactory(object):
    def __init__(self, session):
        self.session = session

    def create_administration_client(self):
        return administration.AdministrationClient(self.session)

    def create_user_client(self):
        return users.UserClient(self.session)

    def create_device_client(self):
        return devices.DeviceClient(self.session)

    def create_org_client(self):
        return orgs.OrgClient(self.session)

    def create_legal_hold_client(self):
        return legal_hold.LegalHoldClient(self.session)

    def create_archive_client(self):
        return archive.ArchiveClient(self.session)

    def create_security_client(self):
        return security.SecurityClient(self.session)


class StorageClientFactory(object):
    def __init__(self, storage_session_manager, login_provider_factory):
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


class MicroserviceClientFactory(object):
    def __init__(self, authority_url, root_session, session_factory, user_context):
        self._authority_url = authority_url
        self._session_factory = session_factory
        self._user_context = user_context
        self._root_session = root_session
        self._key_value_store_client = None
        self._alerts_client = None
        self._departing_employee_client = None
        self._file_event_client = None

    def get_alerts_client(self):
        if not self._alerts_client:
            url = self._key_value_store_client.get_stored_value(u"AlertService-API_URL")
            session = self._session_factory.create_jwt_session(url, self._root_session)
            self._alerts_client = AlertClient(session, self._user_context)
        return self._alerts_client

    def get_departing_employee_client(self):
        if not self._departing_employee_client:
            url = self._key_value_store_client.get_stored_value(u"employeecasemanagement-API_URL")
            session = self._session_factory.create_jwt_session(url, self._root_session)
            self._departing_employee_client = DepartingEmployeeClient(session, self._user_context)
        return self._departing_employee_client

    def get_file_event_client(self):
        if not self._file_event_client:
            config_session = self._session_factory.create_anonymous_session(self._authority_url)
            url = _hacky_get_microservice_url(config_session, u"forensicsearch")
            session = self._session_factory.create_jwt_session(url, self._root_session)
            self._file_event_client = FileEventClient(session)
        return self._file_event_client

    def _get_stored_value(self, key):
        if not self._key_value_store_client:
            config_session = self._session_factory.create_anonymous_session(self._authority_url)
            url = _hacky_get_microservice_url(config_session, u"simple-key-value-store")
            session = self._session_factory.create_anonymous_session(url)
            self._key_value_store_client = KeyValueStoreClient(session)
        return self._key_value_store_client.get_stored_value(key)


def _hacky_get_microservice_url(session, microservice_base_name):
    sts_url = _get_sts_base_url(session)
    return sts_url.replace(u"sts", microservice_base_name)


def _get_sts_base_url(session):
    uri = u"/api/ServerEnv"
    try:
        response = session.get(uri)
    except Exception as ex:
        message = (
            u"An error occurred while requesting server environment information, caused by {0}"
        )
        message = message.format(ex)
        raise Exception(message)

    sts_base_url = None
    if response.text:
        response_json = json.loads(response.text)
        if u"stsBaseUrl" in response_json:
            sts_base_url = response_json[u"stsBaseUrl"]
    if not sts_base_url:
        raise Exception(u"stsBaseUrl not found.")
    return sts_base_url
