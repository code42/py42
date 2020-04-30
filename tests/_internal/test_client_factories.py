import pytest

from py42._internal.client_factories import AuthorityClientFactory, MicroserviceClientFactory
from py42._internal.clients import key_value_store, archive, alerts
from py42._internal.clients import securitydata
from py42._internal.clients.storage import StorageClientFactory, StorageClient
from py42._internal.session_factory import SessionFactory
from py42._internal.storage_session_manager import StorageSessionManager
from py42._internal.token_providers import StorageTokenProviderFactory
from py42.clients import administration, devices, file_event, legalhold, orgs
from py42.clients import detectionlists, users
from py42.clients.detectionlists import departing_employee
from py42.usercontext import UserContext
from py42.clients.users import UserClient


_USER_UID = "user-uid"
TEST_ROOT_URL = "https://example.com"
ALERTS_URL = "alerts.example.com"
FILE_EVENTS_URL = "fileevents.example.com"
DEPARTING_EMPLOYEE_URL = "departing.example.com"


@pytest.fixture
def token_provider_factory(mocker):
    return mocker.MagicMock(spec=StorageTokenProviderFactory)


@pytest.fixture
def storage_session_manager(mocker):
    return mocker.MagicMock(spec=StorageSessionManager)


@pytest.fixture
def session_factory(mocker, mock_session):
    mock_factory = mocker.MagicMock(spec=SessionFactory)
    mock_env_response = '{"stsBaseUrl": "sts-"}'
    mock_session.get.return_value.text = mock_env_response
    mock_factory.create_anonymous_session.return_value = mock_session
    return mock_factory


@pytest.fixture
def user_context(mocker):
    return mocker.MagicMock(spec=UserContext)


@pytest.fixture
def user_client(mocker):
    return mocker.MagicMock(spec=UserClient)


@pytest.fixture
def key_value_store_client(mocker):
    return mocker.MagicMock(spec=key_value_store.KeyValueStoreClient)


class TestAuthorityClientFactory(object):
    def test_create_adminstration_client(self, mock_session):
        factory = AuthorityClientFactory(mock_session)
        client = factory.create_administration_client()
        assert type(client) == administration.AdministrationClient

    def test_create_archive_client(self, mock_session):
        factory = AuthorityClientFactory(mock_session)
        client = factory.create_archive_client()
        assert type(client) == archive.ArchiveClient

    def test_create_device_client(self, mock_session):
        factory = AuthorityClientFactory(mock_session)
        client = factory.create_device_client()
        assert type(client) == devices.DeviceClient

    def test_create_legal_hold_client(self, mock_session):
        factory = AuthorityClientFactory(mock_session)
        client = factory.create_legal_hold_client()
        assert type(client) == legalhold.LegalHoldClient

    def test_create_org_client(self, mock_session):
        factory = AuthorityClientFactory(mock_session)
        client = factory.create_org_client()
        assert type(client) == orgs.OrgClient

    def test_create_security_client(self, mock_session):
        factory = AuthorityClientFactory(mock_session)
        client = factory.create_security_client()
        assert type(client) == securitydata.SecurityClient

    def test_create_user_client(self, mock_session):
        factory = AuthorityClientFactory(mock_session)
        client = factory.create_user_client()
        assert type(client) == users.UserClient


class TestStorageClientFactory(object):
    def test_from_device_guid(self, token_provider_factory, storage_session_manager):
        factory = StorageClientFactory(storage_session_manager, token_provider_factory)
        client = factory.from_device_guid("test-device-guid")
        assert type(client) == StorageClient

    def test_from_plan_info(self, token_provider_factory, storage_session_manager):
        factory = StorageClientFactory(storage_session_manager, token_provider_factory)
        client = factory.from_plan_info("test-plan-uid", "test-dest-guid")
        assert type(client) == StorageClient


class TestMicroserviceClientFactory(object):
    def test_get_alerts_client(self, mock_session, session_factory, user_context, user_client):
        factory = MicroserviceClientFactory(
            TEST_ROOT_URL, mock_session, session_factory, user_context, user_client
        )
        client = factory.get_alerts_client()
        assert type(client) == alerts.AlertClient

    def test_get_alerts_client_calls_get_stored_value_with_expected_key(
        self, mock_session, session_factory, user_context, user_client, key_value_store_client
    ):
        factory = MicroserviceClientFactory(
            TEST_ROOT_URL,
            mock_session,
            session_factory,
            user_context,
            user_client,
            key_value_store_client,
        )
        factory.get_alerts_client()
        key_value_store_client.get_stored_value.assert_called_once_with("AlertService-API_URL")

    def test_get_alerts_client_creates_client_with_expected_url(
        self, mock_session, session_factory, user_context, user_client, key_value_store_client
    ):
        key_value_store_client.get_stored_value.return_value.text = ALERTS_URL
        factory = MicroserviceClientFactory(
            TEST_ROOT_URL,
            mock_session,
            session_factory,
            user_context,
            user_client,
            key_value_store_client,
        )
        factory.get_alerts_client()
        session_factory.create_jwt_session.assert_called_once_with(ALERTS_URL, mock_session)

    def test_get_alerts_client_returns_same_intance_on_multiple_calls(
        self, mock_session, session_factory, user_context, user_client
    ):
        factory = MicroserviceClientFactory(
            TEST_ROOT_URL, mock_session, session_factory, user_context, user_client
        )
        client1 = factory.get_alerts_client()
        client2 = factory.get_alerts_client()

        assert client1 is client2

    def test_get_departing_employee_client(
        self, mock_session, session_factory, user_context, user_client
    ):
        factory = MicroserviceClientFactory(
            TEST_ROOT_URL, mock_session, session_factory, user_context, user_client
        )
        client = factory.get_departing_employee_client()
        assert type(client) == detectionlists.departing_employee.DepartingEmployeeClient

    def test_get_departing_employee_client_calls_get_stored_value_with_expected_key(
        self, mock_session, session_factory, user_context, user_client, key_value_store_client
    ):
        factory = MicroserviceClientFactory(
            TEST_ROOT_URL,
            mock_session,
            session_factory,
            user_context,
            user_client,
            key_value_store_client,
        )
        factory.get_departing_employee_client()

        key_value_store_client.get_stored_value.assert_called_with("employeecasemanagement-API_URL")
        assert key_value_store_client.get_stored_value.call_count == 1

    def test_get_departing_employee_client_creates_client_with_expected_url(
        self, mock_session, session_factory, user_context, user_client, key_value_store_client
    ):
        key_value_store_client.get_stored_value.return_value.text = DEPARTING_EMPLOYEE_URL
        factory = MicroserviceClientFactory(
            TEST_ROOT_URL,
            mock_session,
            session_factory,
            user_context,
            user_client,
            key_value_store_client,
        )
        factory.get_departing_employee_client()
        session_factory.create_jwt_session.assert_called_with(DEPARTING_EMPLOYEE_URL, mock_session)
        assert session_factory.create_jwt_session.call_count == 1

    def test_get_departing_employee_client_returns_same_intance_on_multiple_calls(
        self, mock_session, session_factory, user_context, user_client
    ):
        factory = MicroserviceClientFactory(
            TEST_ROOT_URL, mock_session, session_factory, user_context, user_client
        )
        client1 = factory.get_departing_employee_client()
        client2 = factory.get_departing_employee_client()

        assert client1 is client2

    def test_get_file_event_client(self, mock_session, session_factory, user_context, user_client):
        factory = MicroserviceClientFactory(
            TEST_ROOT_URL, mock_session, session_factory, user_context, user_client
        )
        client = factory.get_file_event_client()
        assert type(client) == file_event.FileEventClient

    def test_get_file_event_client_calls_get_stored_value_with_expected_key(
        self, mock_session, session_factory, user_context, user_client, key_value_store_client
    ):
        factory = MicroserviceClientFactory(
            TEST_ROOT_URL,
            mock_session,
            session_factory,
            user_context,
            user_client,
            key_value_store_client,
        )
        factory.get_file_event_client()
        key_value_store_client.get_stored_value.assert_called_once_with("FORENSIC_SEARCH-API_URL")

    def test_get_file_event_client_calls_creates_client_with_expected_url(
        self, mock_session, session_factory, user_context, user_client, key_value_store_client
    ):
        key_value_store_client.get_stored_value.return_value.text = FILE_EVENTS_URL
        factory = MicroserviceClientFactory(
            TEST_ROOT_URL,
            mock_session,
            session_factory,
            user_context,
            user_client,
            key_value_store_client,
        )
        factory.get_file_event_client()
        session_factory.create_jwt_session.assert_called_once_with(FILE_EVENTS_URL, mock_session)

    def test_get_file_event_client_returns_same_intance_on_multiple_calls(
        self, mock_session, session_factory, user_context, user_client
    ):
        factory = MicroserviceClientFactory(
            TEST_ROOT_URL, mock_session, session_factory, user_context, user_client
        )
        client1 = factory.get_file_event_client()
        client2 = factory.get_file_event_client()

        assert client1 is client2
