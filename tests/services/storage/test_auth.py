import pytest
from requests import Request
from tests.conftest import create_mock_response

from py42.services._connection import Connection
from py42.services.storage._auth import FileArchiveAuth
from py42.services.storage._auth import SecurityArchiveAuth

TEST_USER_ID = "0123456789"
TEST_DEVICE_GUID = "testdeviceguid"
TEST_DESTINATION_GUID = "testdestinationguid"
TEST_PLAN_UID = "testplanuid"


@pytest.fixture
def mock_request(mocker):
    mock = mocker.MagicMock(spec=Request)
    mock.headers = {}
    return mock


@pytest.fixture
def mock_tmp_auth_conn(mock_connection, mocker):
    response = create_mock_response(
        mocker, '{"serverUrl": "testhost.com", "loginToken": "TEST_TMP_TOKEN_VALUE"}'
    )
    mock_connection.post.return_value = response
    return mock_connection


@pytest.fixture
def mock_storage_auth_token_conn(mocker):
    mock_connection = mocker.MagicMock(spec=Connection)
    mock_connection.headers = {}
    mock_connection.post.return_value = create_mock_response(
        mocker, '["TEST_V1", "TOKEN_VALUE"]'
    )
    mocker.patch(
        "py42.services.storage._auth._get_new_storage_connection",
        return_value=mock_connection,
    )
    return mock_connection


class TestFileArchiveTmpAuth:
    def test_call_returns_request_with_expected_header(
        self, mock_tmp_auth_conn, mock_request, mock_storage_auth_token_conn
    ):
        auth = FileArchiveAuth(
            mock_tmp_auth_conn, TEST_USER_ID, TEST_DEVICE_GUID, TEST_DESTINATION_GUID
        )
        request = auth(mock_request)
        assert request.headers["Authorization"] == "token TEST_V1-TOKEN_VALUE"

    def test_call_only_calls_auth_apis_first_time(
        self, mock_tmp_auth_conn, mock_request, mock_storage_auth_token_conn
    ):
        auth = FileArchiveAuth(
            mock_tmp_auth_conn, TEST_USER_ID, TEST_DEVICE_GUID, TEST_DESTINATION_GUID
        )
        auth(mock_request)
        assert mock_tmp_auth_conn.post.call_count == 1
        assert mock_storage_auth_token_conn.post.call_count == 1
        auth(mock_request)
        assert mock_tmp_auth_conn.post.call_count == 1
        assert mock_storage_auth_token_conn.post.call_count == 1

    def test_call_calls_auth_apis_with_expected_urls(
        self, mock_tmp_auth_conn, mock_request, mock_storage_auth_token_conn
    ):
        auth = FileArchiveAuth(
            mock_tmp_auth_conn, TEST_USER_ID, TEST_DEVICE_GUID, TEST_DESTINATION_GUID
        )
        auth(mock_request)
        data = {
            "userId": TEST_USER_ID,
            "sourceGuid": TEST_DEVICE_GUID,
            "destinationGuid": TEST_DESTINATION_GUID,
        }
        mock_tmp_auth_conn.post.assert_called_once_with("/api/LoginToken", json=data)
        mock_storage_auth_token_conn.post.assert_called_once_with(
            "api/AuthToken",
            headers={"Authorization": "login_token TEST_TMP_TOKEN_VALUE"},
        )

    def test_clear_credentials_causes_auth_api_to_be_called_on_subsequent_calls(
        self, mock_tmp_auth_conn, mock_request, mock_storage_auth_token_conn
    ):
        auth = FileArchiveAuth(
            mock_tmp_auth_conn, TEST_USER_ID, TEST_DEVICE_GUID, TEST_DESTINATION_GUID
        )
        auth(mock_request)
        assert mock_tmp_auth_conn.post.call_count == 1
        assert mock_storage_auth_token_conn.post.call_count == 1
        auth.clear_credentials()
        auth(mock_request)
        assert mock_tmp_auth_conn.post.call_count == 2
        assert mock_storage_auth_token_conn.post.call_count == 2

    def test_get_storage_url_returns_expected_value(
        self, mock_tmp_auth_conn, mock_storage_auth_token_conn
    ):
        auth = FileArchiveAuth(
            mock_tmp_auth_conn, TEST_USER_ID, TEST_DEVICE_GUID, TEST_DESTINATION_GUID
        )
        assert auth.get_storage_url() == "testhost.com"

    def test_get_storage_url_only_calls_auth_api_first_time(
        self, mock_tmp_auth_conn, mock_storage_auth_token_conn
    ):
        auth = FileArchiveAuth(
            mock_tmp_auth_conn, TEST_USER_ID, TEST_DEVICE_GUID, TEST_DESTINATION_GUID
        )
        auth.get_storage_url()
        assert mock_tmp_auth_conn.post.call_count == 1
        assert mock_storage_auth_token_conn.post.call_count == 1
        auth.get_storage_url()
        assert mock_tmp_auth_conn.post.call_count == 1
        assert mock_storage_auth_token_conn.post.call_count == 1


class TestSecurityArchiveTmpAuth:
    def test_call_returns_request_with_expected_header(
        self, mock_tmp_auth_conn, mock_request, mock_storage_auth_token_conn
    ):
        auth = SecurityArchiveAuth(
            mock_tmp_auth_conn, TEST_PLAN_UID, TEST_DESTINATION_GUID
        )
        request = auth(mock_request)
        assert request.headers["Authorization"] == "token TEST_V1-TOKEN_VALUE"

    def test_call_only_calls_auth_apis_first_time(
        self, mock_tmp_auth_conn, mock_request, mock_storage_auth_token_conn
    ):
        auth = SecurityArchiveAuth(
            mock_tmp_auth_conn, TEST_PLAN_UID, TEST_DESTINATION_GUID
        )
        auth(mock_request)
        assert mock_tmp_auth_conn.post.call_count == 1
        assert mock_storage_auth_token_conn.post.call_count == 1
        auth(mock_request)
        assert mock_tmp_auth_conn.post.call_count == 1
        assert mock_storage_auth_token_conn.post.call_count == 1

    def test_call_calls_auth_apis_with_expected_urls(
        self, mock_tmp_auth_conn, mock_request, mock_storage_auth_token_conn
    ):
        auth = SecurityArchiveAuth(
            mock_tmp_auth_conn, TEST_PLAN_UID, TEST_DESTINATION_GUID
        )
        auth(mock_request)
        data = {"planUid": TEST_PLAN_UID, "destinationGuid": TEST_DESTINATION_GUID}
        mock_tmp_auth_conn.post.assert_called_once_with(
            "/api/StorageAuthToken", json=data
        )
        mock_storage_auth_token_conn.post.assert_called_once_with(
            "api/AuthToken",
            headers={"Authorization": "login_token TEST_TMP_TOKEN_VALUE"},
        )

    def test_clear_credentials_causes_auth_apis_to_be_called_on_subsequent_calls(
        self, mock_tmp_auth_conn, mock_request, mock_storage_auth_token_conn
    ):
        auth = SecurityArchiveAuth(
            mock_tmp_auth_conn, TEST_PLAN_UID, TEST_DESTINATION_GUID
        )
        auth(mock_request)
        assert mock_tmp_auth_conn.post.call_count == 1
        assert mock_storage_auth_token_conn.post.call_count == 1
        auth.clear_credentials()
        auth(mock_request)
        assert mock_tmp_auth_conn.post.call_count == 2
        assert mock_storage_auth_token_conn.post.call_count == 2

    def test_get_storage_url_returns_expected_value(
        self, mock_tmp_auth_conn, mock_storage_auth_token_conn
    ):
        auth = SecurityArchiveAuth(
            mock_tmp_auth_conn, TEST_PLAN_UID, TEST_DESTINATION_GUID
        )
        assert auth.get_storage_url() == "testhost.com"

    def test_get_storage_url_only_calls_auth_apis_first_time(
        self, mock_tmp_auth_conn, mock_storage_auth_token_conn
    ):
        auth = SecurityArchiveAuth(
            mock_tmp_auth_conn, TEST_PLAN_UID, TEST_DESTINATION_GUID
        )
        auth.get_storage_url()
        assert mock_tmp_auth_conn.post.call_count == 1
        assert mock_storage_auth_token_conn.post.call_count == 1
        auth.get_storage_url()
        assert mock_tmp_auth_conn.post.call_count == 1
        assert mock_storage_auth_token_conn.post.call_count == 1
