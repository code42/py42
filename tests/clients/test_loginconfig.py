import pytest
from requests.sessions import Session

from pycpg.clients.loginconfig import LoginConfigurationClient
from pycpg.services._connection import Connection

HOST_ADDRESS = "example.com"


class TestLoginConfiguration:
    @pytest.fixture
    def mock_session(self, mocker):
        mock_session = mocker.MagicMock(spec=Session)
        mock_session.headers = {}
        return mock_session

    def test_get_for_user_calls_session_get_with_expected_uri_and_params(
        self, mock_session
    ):
        connection = Connection.from_host_address(HOST_ADDRESS, session=mock_session)
        loginconfig = LoginConfigurationClient(connection)
        loginconfig.get_for_user("test@example.com")
        expected_uri = f"https://{HOST_ADDRESS}/api/v3/LoginConfiguration"
        expected_params = {"username": "test@example.com"}
        mock_session.get.assert_called_once_with(expected_uri, params=expected_params)

    def test_get_for_user_does_not_use_pycpg_connection_get_method(
        self, mocker, mock_session
    ):
        """Because the loginConfiguration endpoint is unauthenticated, we want to make
        sure we don't force the Connection's CPGRenewableAuth object to make any
        authentication requests before making the loginConfig request.
        """
        mock_get = mocker.patch("pycpg.services._connection.Connection.get")
        connection = Connection.from_host_address(HOST_ADDRESS, session=mock_session)
        loginconfig = LoginConfigurationClient(connection)
        loginconfig.get_for_user("test@example.com")
        assert mock_get.call_count == 0
        assert mock_session.get.call_count == 1
