import json

from requests import HTTPError

from py42._internal.clients import archive
from py42._internal.clients import key_value_store
from py42._internal.clients import securitydata
from py42.clients import administration, alerts, devices, legalhold, orgs, users
from py42.clients.detectionlists.departing_employee import DepartingEmployeeClient
from py42.clients.detectionlists.high_risk_employee import HighRiskEmployeeClient
from py42._internal.clients.detection_list_user import DetectionListUserClient
from py42.clients.file_event import FileEventClient
from py42.exceptions import Py42FeatureUnavailableError, Py42SessionInitializationError


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
        return legalhold.LegalHoldClient(self.session)

    def create_archive_client(self):
        return archive.ArchiveClient(self.session)

    def create_security_client(self):
        return securitydata.SecurityClient(self.session)


class MicroserviceClientFactory(object):
    def __init__(
        self,
        authority_url,
        root_session,
        session_factory,
        user_context,
        key_value_store_client=None,
    ):
        self._authority_url = authority_url
        self._root_session = root_session
        self._session_factory = session_factory
        self._user_context = user_context
        self._key_value_store_client = key_value_store_client
        self._alerts_client = None
        self._departing_employee_client = None
        self._file_event_client = None
        self._high_risk_employee_client = None
        self._detection_list_user_client = None

    def get_alerts_client(self):
        if not self._alerts_client:
            session = self._get_jwt_session(u"AlertService-API_URL")
            self._alerts_client = alerts.AlertClient(session, self._user_context)
        return self._alerts_client

    def get_departing_employee_client(self):
        if not self._departing_employee_client:
            session = self._get_jwt_session(u"employeecasemanagement-API_URL")
            self._departing_employee_client = DepartingEmployeeClient(session, self._user_context)
        return self._departing_employee_client

    def get_file_event_client(self):
        if not self._file_event_client:
            session = self._get_jwt_session(u"FORENSIC_SEARCH-API_URL")
            self._file_event_client = FileEventClient(session)
        return self._file_event_client

    def _get_jwt_session(self, key):
        url = self._get_stored_value(key)
        return self._session_factory.create_jwt_session(url, self._root_session)

    def _get_stored_value(self, key):
        if not self._key_value_store_client:
            url = _hacky_get_microservice_url(self._root_session, u"simple-key-value-store")
            session = self._session_factory.create_anonymous_session(url)
            self._key_value_store_client = key_value_store.KeyValueStoreClient(session)
        return self._key_value_store_client.get_stored_value(key).text

    def get_high_risk_employee_client(self, user_client):
        if not self._high_risk_employee_client:
            session = self._get_jwt_session(u"employeecasemanagement-API_URL")
            self._high_risk_employee_client = HighRiskEmployeeClient(
                session, self._user_context, self.get_detection_list_user_client(), user_client
            )
        return self._high_risk_employee_client

    def get_detection_list_user_client(self):
        if not self._detection_list_user_client:
            session = self._get_jwt_session(u"employeecasemanagement-API_URL")
            self._detection_list_user_client = DetectionListUserClient(session, self._user_context)
        return self._detection_list_user_client


def _hacky_get_microservice_url(session, microservice_base_name):
    sts_url = _get_sts_base_url(session)
    return sts_url.replace(u"sts", microservice_base_name)


def _get_sts_base_url(session):
    uri = u"/api/ServerEnv"
    try:
        response = session.get(uri)
    except HTTPError as ex:
        raise Py42SessionInitializationError(ex)

    sts_base_url = None
    if response.text:
        response_json = json.loads(response.text)
        sts_base_url = response_json.get(u"stsBaseUrl")
    if not sts_base_url:
        raise Py42FeatureUnavailableError()
    return sts_base_url
