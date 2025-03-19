import pytest
from requests import Request
from tests.conftest import create_mock_response

from pycpg.services._auth import ApiClientAuth
from pycpg.services._auth import BearerAuth
from pycpg.services._auth import CustomJWTAuth


@pytest.fixture
def mock_request(mocker):
    mock = mocker.MagicMock(spec=Request)
    mock.headers = {}
    return mock


@pytest.fixture
def mock_v3_conn(mock_connection, mocker):
    response = create_mock_response(mocker, '{"v3_user_token": "TEST_TOKEN_VALUE"}')
    mock_connection.get.return_value = response
    return mock_connection


@pytest.fixture
def mock_api_client_conn(mock_connection, mocker):
    t = '{"access_token": "API_CLIENT_VAL", "token_type": "bearer", "expires_in": 900}'
    response = create_mock_response(mocker, t)
    mock_connection.post.return_value = response
    return mock_connection


@pytest.fixture
def mock_custom_auth_function():
    def custom_function():
        return "token-string"

    return custom_function


class TestV3Auth:
    def test_call_returns_request_with_expected_header(
        self, mock_v3_conn, mock_request
    ):
        auth = BearerAuth(mock_v3_conn)
        request = auth(mock_request)
        assert request.headers["Authorization"] == "Bearer TEST_TOKEN_VALUE"

    def test_call_only_calls_auth_api_first_time(self, mock_v3_conn, mock_request):
        auth = BearerAuth(mock_v3_conn)
        auth(mock_request)
        assert mock_v3_conn.get.call_count == 1
        auth(mock_request)
        assert mock_v3_conn.get.call_count == 1

    def test_call_calls_auth_api_with_expected_url(self, mock_v3_conn, mock_request):
        auth = BearerAuth(mock_v3_conn)
        auth(mock_request)
        params = {"useBody": True}
        headers = None
        mock_v3_conn.get.assert_called_once_with(
            "/api/v3/auth/jwt", params=params, headers=headers
        )

    @pytest.mark.parametrize(
        "totp,expected",
        [("123456", "123456"), (lambda: "654321", "654321"), (999999, "999999")],
    )
    def test_call_calls_auth_api_with_totp_header(
        self, mock_v3_conn, mock_request, totp, expected
    ):
        auth = BearerAuth(mock_v3_conn, totp)
        auth(mock_request)
        params = {"useBody": True}
        headers = {"totp-auth": expected}
        mock_v3_conn.get.assert_called_once_with(
            "/api/v3/auth/jwt", params=params, headers=headers
        )

    def test_clear_credentials_causes_auth_api_to_be_called_on_subsequent_calls(
        self, mock_v3_conn, mock_request
    ):
        auth = BearerAuth(mock_v3_conn)
        auth(mock_request)
        assert mock_v3_conn.get.call_count == 1
        auth.clear_credentials()
        auth(mock_request)
        assert mock_v3_conn.get.call_count == 2


class TestCustomJWTAuth:
    def test_get_credentials_returns_jwt_string(self, mock_custom_auth_function):
        auth = CustomJWTAuth(mock_custom_auth_function)
        jwt_string = auth.get_credentials()
        assert jwt_string == "Bearer token-string"


class TestApiClientAuth:
    def test_call_returns_request_with_expected_header(
        self, mock_api_client_conn, mock_request
    ):
        auth = ApiClientAuth(mock_api_client_conn)
        request = auth(mock_request)
        assert request.headers["Authorization"] == "Bearer API_CLIENT_VAL"

    def test_call_only_calls_auth_api_first_time(
        self, mock_api_client_conn, mock_request
    ):
        auth = ApiClientAuth(mock_api_client_conn)
        auth(mock_request)
        assert mock_api_client_conn.post.call_count == 1
        auth(mock_request)
        assert mock_api_client_conn.post.call_count == 1

    def test_call_calls_auth_api_with_expected_url(
        self, mock_api_client_conn, mock_request
    ):
        auth = ApiClientAuth(mock_api_client_conn)
        auth(mock_request)
        params = {"grant_type": "client_credentials"}
        mock_api_client_conn.post.assert_called_once_with(
            "/api/v3/oauth/token", params=params
        )

    def test_clear_credentials_causes_auth_api_to_be_called_on_subsequent_calls(
        self, mock_api_client_conn, mock_request
    ):
        auth = ApiClientAuth(mock_api_client_conn)
        auth(mock_request)
        assert mock_api_client_conn.post.call_count == 1
        auth.clear_credentials()
        auth(mock_request)
        assert mock_api_client_conn.post.call_count == 2
