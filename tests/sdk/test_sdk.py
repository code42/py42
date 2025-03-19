import pytest
from requests import Session
from tests.conftest import create_mock_response

from pycpg.clients.archive import ArchiveClient
from pycpg.clients.auditlogs import AuditLogsClient
from pycpg.exceptions import PycpgUnauthorizedError
from pycpg.sdk import from_local_account
from pycpg.sdk import SDKClient
from pycpg.services import administration
from pycpg.services import devices
from pycpg.services import legalhold
from pycpg.services import legalholdapiclient
from pycpg.services import orgs
from pycpg.services import users
from pycpg.services._auth import CPGRenewableAuth
from pycpg.services._connection import Connection
from pycpg.usercontext import UserContext


HOST_ADDRESS = "https://example.com"
TEST_USERNAME = "test-username"
TEST_PASSWORD = "test-password"


class TestSDK:
    @pytest.fixture
    def pycpg_connection(self, mocker, successful_response):
        mock_connection = mocker.MagicMock(spec=Connection)
        mock_connection.get.return_value = successful_response
        return mock_connection

    @pytest.fixture
    def mock_auth(self, mocker):
        return mocker.MagicMock(spec=CPGRenewableAuth)

    @pytest.fixture
    def mock_session(self, mocker):
        mock_session = mocker.MagicMock(spec=Session)
        mock_session.headers = {}
        return mock_session

    def test_has_administration_service_set(self, pycpg_connection, mock_auth):
        client = SDKClient(pycpg_connection, mock_auth)
        assert type(client.serveradmin) == administration.AdministrationService

    def test_has_archive_service_set(self, pycpg_connection, mock_auth):
        client = SDKClient(pycpg_connection, mock_auth)
        assert type(client.archive) == ArchiveClient

    def test_has_device_service_set(self, pycpg_connection, mock_auth):
        client = SDKClient(pycpg_connection, mock_auth)
        assert type(client.devices) == devices.DeviceService


    def test_has_legal_hold_service_set(self, pycpg_connection, mock_auth):
        client = SDKClient(pycpg_connection, mock_auth)
        assert type(client.legalhold) == legalhold.LegalHoldService

    def test_has_api_client_legal_hold_service_set_if_initialized_with_api_client_flag(
        self, pycpg_connection, mock_auth
    ):
        client = SDKClient(pycpg_connection, mock_auth, auth_flag=1)
        assert type(client.legalhold) == legalholdapiclient.LegalHoldApiClientService

    def test_has_org_service_set(self, pycpg_connection, mock_auth):
        client = SDKClient(pycpg_connection, mock_auth)
        assert type(client.orgs) == orgs.OrgService

    def test_has_user_service_set(self, pycpg_connection, mock_auth):
        client = SDKClient(pycpg_connection, mock_auth)
        assert type(client.users) == users.UserService

    def test_has_user_context_set(self, pycpg_connection, mock_auth):
        client = SDKClient(pycpg_connection, mock_auth)
        assert type(client.usercontext) == UserContext

    def test_has_auditlog_service_set(self, pycpg_connection, mock_auth):
        client = SDKClient(pycpg_connection, mock_auth)
        assert type(client.auditlogs) == AuditLogsClient

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
        mocker.patch("pycpg.sdk.SDKClient.from_local_account", return_value=client)

        with pytest.raises(PycpgUnauthorizedError) as err:
            from_local_account(HOST_ADDRESS, TEST_USERNAME, TEST_PASSWORD)

        assert f"User LoginConfig: {login_type}" in str(err)
