import pytest
from requests import Session
from tests.conftest import create_mock_response

from py42.clients.alerts import AlertsClient
from py42.clients.archive import ArchiveClient
from py42.clients.auditlogs import AuditLogsClient
from py42.clients.cases import CasesClient
from py42.clients.detectionlists import DetectionListsClient
from py42.exceptions import Py42UnauthorizedError
from py42.sdk import from_local_account
from py42.sdk import SDKClient
from py42.services import administration
from py42.services import devices
from py42.services import legalhold
from py42.services import orgs
from py42.services import users
from py42.services._auth import C42RenewableAuth
from py42.services._connection import Connection
from py42.usercontext import UserContext


HOST_ADDRESS = "https://example.com"
TEST_USERNAME = "test-username"
TEST_PASSWORD = "test-password"


class TestSDK:
    @pytest.fixture
    def py42_connection(self, mocker, successful_response):
        mock_connection = mocker.MagicMock(spec=Connection)
        mock_connection.get.return_value = successful_response
        return mock_connection

    @pytest.fixture
    def mock_auth(self, mocker):
        return mocker.MagicMock(spec=C42RenewableAuth)

    @pytest.fixture
    def mock_session(self, mocker):
        mock_session = mocker.MagicMock(spec=Session)
        mock_session.headers = {}
        return mock_session

    def test_has_administration_service_set(self, py42_connection, mock_auth):
        client = SDKClient(py42_connection, mock_auth)
        assert type(client.serveradmin) == administration.AdministrationService

    def test_has_archive_service_set(self, py42_connection, mock_auth):
        client = SDKClient(py42_connection, mock_auth)
        assert type(client.archive) == ArchiveClient

    def test_has_device_service_set(self, py42_connection, mock_auth):
        client = SDKClient(py42_connection, mock_auth)
        assert type(client.devices) == devices.DeviceService

    def test_has_alert_service_set(self, py42_connection, mock_auth):
        client = SDKClient(py42_connection, mock_auth)
        assert type(client.alerts) == AlertsClient

    def test_has_detection_lists_service_set(self, py42_connection, mock_auth):
        client = SDKClient(py42_connection, mock_auth)
        assert type(client.detectionlists) == DetectionListsClient

    def test_has_legal_hold_service_set(self, py42_connection, mock_auth):
        client = SDKClient(py42_connection, mock_auth)
        assert type(client.legalhold) == legalhold.LegalHoldService

    def test_has_org_service_set(self, py42_connection, mock_auth):
        client = SDKClient(py42_connection, mock_auth)
        assert type(client.orgs) == orgs.OrgService

    def test_has_user_service_set(self, py42_connection, mock_auth):
        client = SDKClient(py42_connection, mock_auth)
        assert type(client.users) == users.UserService

    def test_has_user_context_set(self, py42_connection, mock_auth):
        client = SDKClient(py42_connection, mock_auth)
        assert type(client.usercontext) == UserContext

    def test_has_auditlog_service_set(self, py42_connection, mock_auth):
        client = SDKClient(py42_connection, mock_auth)
        assert type(client.auditlogs) == AuditLogsClient

    def test_has_cases_service_set(self, py42_connection, mock_auth):
        client = SDKClient(py42_connection, mock_auth)
        assert type(client.cases) == CasesClient

    def test_from_local_account_when_unauthorized_calls_loginConfig_and_returns_config_value_on_raised_exception_text(
        self, mocker, mock_session, mock_auth, unauthorized_response
    ):
        login_type = "LOCAL_2FA"
        mock_session.send.return_value = unauthorized_response
        mock_session.get.return_value = create_mock_response(
            mocker, f'{{"loginType": "{login_type}"}}'
        )
        connection = Connection.from_host_address(HOST_ADDRESS, session=mock_session)
        client = SDKClient(connection, mock_auth)
        mocker.patch("py42.sdk.SDKClient.from_local_account", return_value=client)

        with pytest.raises(Py42UnauthorizedError) as err:
            from_local_account(HOST_ADDRESS, TEST_USERNAME, TEST_PASSWORD)

        assert f"User LoginConfig: {login_type}" in str(err)
