import pytest
from services._connection import Connection

from py42._internal.initialization import SDKDependencies
from py42._internal.session_factory import SessionFactory
from py42.clients import alerts
from py42.clients import archive as arch_mod
from py42.clients import detectionlists
from py42.clients import securitydata as sec_mod
from py42.sdk import SDKClient
from py42.services import administration
from py42.services import devices
from py42.services import legalhold
from py42.services import orgs
from py42.services import users
from py42.usercontext import UserContext

HOST_ADDRESS = "https://example.com"
TEST_USERNAME = "test-username"
TEST_PASSWORD = "test-password"


class TestSDK(object):
    @pytest.fixture
    def py42_session(self, mocker, successful_response):
        mock_session = mocker.MagicMock(spec=Connection)
        mock_session.get.return_value = successful_response
        return mock_session

    @pytest.fixture
    def mock_session_factory(self, mocker, py42_session):
        mock_session_factory = mocker.MagicMock(spec=SessionFactory)
        mock_session_factory.create_jwt_session.return_value = py42_session
        return mock_session_factory

    def test_has_administation_client_set(
        self, mock_session_factory, success_requests_session
    ):
        deps = SDKDependencies(
            HOST_ADDRESS, mock_session_factory, success_requests_session
        )
        sdk = SDKClient(deps)
        assert type(sdk.serveradmin) == administration.AdministrationService

    def test_has_archive_module_set(
        self, mock_session_factory, success_requests_session
    ):
        deps = SDKDependencies(
            HOST_ADDRESS, mock_session_factory, success_requests_session
        )
        sdk = SDKClient(deps)
        assert type(sdk.archive) == arch_mod.ArchiveClient

    def test_has_device_client_set(
        self, mock_session_factory, success_requests_session
    ):
        deps = SDKDependencies(
            HOST_ADDRESS, mock_session_factory, success_requests_session
        )
        sdk = SDKClient(deps)
        assert type(sdk.devices) == devices.DeviceService

    def test_has_alert_module_set(self, mock_session_factory, success_requests_session):
        deps = SDKDependencies(
            HOST_ADDRESS, mock_session_factory, success_requests_session
        )
        sdk = SDKClient(deps)
        assert type(sdk.alerts) == alerts.AlertsClient

    def test_has_detection_lists_module_set(
        self, mock_session_factory, success_requests_session
    ):
        deps = SDKDependencies(
            HOST_ADDRESS, mock_session_factory, success_requests_session
        )
        sdk = SDKClient(deps)
        assert type(sdk.detectionlists) == detectionlists.DetectionListsClient

    def test_has_legal_hold_client_set(
        self, mock_session_factory, success_requests_session
    ):
        deps = SDKDependencies(
            HOST_ADDRESS, mock_session_factory, success_requests_session
        )
        sdk = SDKClient(deps)
        assert type(sdk.legalhold) == legalhold.LegalHoldService

    def test_has_org_client_set(self, mock_session_factory, success_requests_session):
        deps = SDKDependencies(
            HOST_ADDRESS, mock_session_factory, success_requests_session
        )
        sdk = SDKClient(deps)
        assert type(sdk.orgs) == orgs.OrgService

    def test_has_security_module_set(
        self, mock_session_factory, success_requests_session
    ):
        deps = SDKDependencies(
            HOST_ADDRESS, mock_session_factory, success_requests_session
        )
        sdk = SDKClient(deps)
        assert type(sdk.securitydata) == sec_mod.SecurityDataClient

    def test_has_user_client_set(self, mock_session_factory, success_requests_session):
        deps = SDKDependencies(
            HOST_ADDRESS, mock_session_factory, success_requests_session
        )
        sdk = SDKClient(deps)
        assert type(sdk.users) == users.UserService

    def test_has_user_context_set(self, mock_session_factory, success_requests_session):
        deps = SDKDependencies(
            HOST_ADDRESS, mock_session_factory, success_requests_session
        )
        sdk = SDKClient(deps)
        assert type(sdk.usercontext) == UserContext
