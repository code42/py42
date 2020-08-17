import pytest
from requests import Request

from py42.services.storage._auth import FileArchiveTmpAuth
from py42.services.storage._auth import SecurityArchiveTmpAuth
from py42.services.storage._auth import V1Auth

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
def mock_tmp_auth_conn(mock_connection, py42_response):
    py42_response.text = '{"loginToken": "TEST_TMP_TOKEN_VALUE"}'
    mock_connection.post.return_value = py42_response
    return mock_connection


@pytest.fixture
def mock_v1_auth_conn(mock_connection, py42_response):
    py42_response.text = '["TEST_V1", "TOKEN_VALUE"]'
    mock_connection.post.return_value = py42_response
    return mock_connection


class TestFileArchiveTmpAuth(object):
    def test_call_returns_request_with_expected_header(self, mock_tmp_auth_conn, mock_request):
        auth = FileArchiveTmpAuth(mock_tmp_auth_conn, TEST_USER_ID, TEST_DEVICE_GUID, TEST_DESTINATION_GUID)
        request = auth(mock_request)
        assert request.headers["Authorization"] == "login_token TEST_TMP_TOKEN_VALUE"

    def test_call_only_calls_auth_api_first_time(self, mock_tmp_auth_conn, mock_request):
        auth = FileArchiveTmpAuth(mock_tmp_auth_conn, TEST_USER_ID, TEST_DEVICE_GUID, TEST_DESTINATION_GUID)
        auth(mock_request)
        assert mock_tmp_auth_conn.post.call_count == 1
        auth(mock_request)
        assert mock_tmp_auth_conn.post.call_count == 1

    def test_call_calls_auth_api_with_expected_url(self, mock_tmp_auth_conn, mock_request):
        auth = FileArchiveTmpAuth(mock_tmp_auth_conn, TEST_USER_ID, TEST_DEVICE_GUID, TEST_DESTINATION_GUID)
        auth(mock_request)
        data = {
            u"userId": TEST_USER_ID,
            u"sourceGuid": TEST_DEVICE_GUID,
            u"destinationGuid": TEST_DESTINATION_GUID,
        }
        mock_tmp_auth_conn.post.assert_called_once_with("/api/LoginToken", json=data)

    def test_clear_credentials_causes_auth_api_to_be_called_on_subsequent_calls(self, mock_tmp_auth_conn, mock_request):
        auth = FileArchiveTmpAuth(mock_tmp_auth_conn, TEST_USER_ID, TEST_DEVICE_GUID, TEST_DESTINATION_GUID)
        auth(mock_request)
        assert mock_tmp_auth_conn.post.call_count == 1
        auth.clear_credentials()
        auth(mock_request)
        assert mock_tmp_auth_conn.post.call_count == 2


class TestSecurityArchiveTmpAuth(object):
    def test_call_returns_request_with_expected_header(self, mock_tmp_auth_conn, mock_request):
        auth = SecurityArchiveTmpAuth(mock_tmp_auth_conn, TEST_PLAN_UID, TEST_DESTINATION_GUID)
        request = auth(mock_request)
        assert request.headers["Authorization"] == "login_token TEST_TMP_TOKEN_VALUE"

    def test_call_only_calls_auth_api_first_time(self, mock_tmp_auth_conn, mock_request):
        auth = SecurityArchiveTmpAuth(mock_tmp_auth_conn, TEST_PLAN_UID, TEST_DESTINATION_GUID)
        auth(mock_request)
        assert mock_tmp_auth_conn.post.call_count == 1
        auth(mock_request)
        assert mock_tmp_auth_conn.post.call_count == 1

    def test_call_calls_auth_api_with_expected_url(self, mock_tmp_auth_conn, mock_request):
        auth = SecurityArchiveTmpAuth(mock_tmp_auth_conn, TEST_PLAN_UID, TEST_DESTINATION_GUID)
        auth(mock_request)
        data = {u"planUid": TEST_PLAN_UID, u"destinationGuid": TEST_DESTINATION_GUID}
        mock_tmp_auth_conn.post.assert_called_once_with("/api/StorageAuthToken", json=data)

    def test_clear_credentials_causes_auth_api_to_be_called_on_subsequent_calls(self, mock_tmp_auth_conn, mock_request):
        auth = SecurityArchiveTmpAuth(mock_tmp_auth_conn, TEST_PLAN_UID, TEST_DESTINATION_GUID)
        auth(mock_request)
        assert mock_tmp_auth_conn.post.call_count == 1
        auth.clear_credentials()
        auth(mock_request)
        assert mock_tmp_auth_conn.post.call_count == 2


class TestV1Auth(object):
    def test_call_returns_request_with_expected_header(self, mock_v1_auth_conn, mock_request):
        auth = V1Auth(mock_v1_auth_conn)
        request = auth(mock_request)
        assert request.headers["Authorization"] == "token TEST_V1-TOKEN_VALUE"

    def test_call_only_calls_auth_api_first_time(self, mock_v1_auth_conn, mock_request):
        auth = V1Auth(mock_v1_auth_conn)
        auth(mock_request)
        assert mock_v1_auth_conn.post.call_count == 1
        auth(mock_request)
        assert mock_v1_auth_conn.post.call_count == 1

    def test_call_calls_auth_api_with_expected_url(self, mock_v1_auth_conn, mock_request):
        auth = V1Auth(mock_v1_auth_conn)
        auth(mock_request)
        mock_v1_auth_conn.post.assert_called_once_with("/api/AuthToken")

    def test_clear_credentials_causes_auth_api_to_be_called_on_subsequent_calls(self, mock_v1_auth_conn, mock_request):
        auth = V1Auth(mock_v1_auth_conn)
        auth(mock_request)
        assert mock_v1_auth_conn.post.call_count == 1
        auth.clear_credentials()
        auth(mock_request)
        assert mock_v1_auth_conn.post.call_count == 2
