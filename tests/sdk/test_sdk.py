import pytest

from py42.clients.alerts import AlertsClient
from py42.clients.archive import ArchiveClient
from py42.clients.auditlogs import AuditLogsClient
from py42.clients.cases import CasesClient
from py42.clients.detectionlists import DetectionListsClient
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
