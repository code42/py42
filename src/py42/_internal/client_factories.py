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


class MicroserviceClientFactory(object):
    def __init__(self, session_factory, key_value_store_client, user_context):
        self._session_factory = session_factory
        self._key_value_store_client = key_value_store_client
        self._user_context = user_context

    def create_alerts_client(self):
        url = self._key_value_store_client.get_stored_value(u"AlertService-API_URL")
        session = self._session_factory.create_jwt_session(url)
        return AlertClient(session, self._user_context)

    def create_departing_employee_client(self):
        url = self._key_value_store_client.get_stored_value(u"employeecasemanagement-API_URL")
        session = self._session_factory.create_jwt_session(url)
        return DepartingEmployeeClient(session, self._user_context)

    def create_file_event_client(self, authority_url):
        config_session = self._session_factory.create_anonymous_session(authority_url)
        url = hacky_get_microservice_url(config_session, u"forensicsearch")
        session = self._session_factory.create_jwt_session(url)
        return FileEventClient(session)


def hacky_get_microservice_url(session, microservice_base_name):
    sts_url = _get_sts_base_url(session)
    return str(sts_url).replace(u"sts", microservice_base_name)


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
