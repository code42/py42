import pytest
from requests import Request
from tests.conftest import create_mock_response

from pycpg.services._connection import Connection

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
        "pycpg.services.storage._auth._get_new_storage_connection",
        return_value=mock_connection,
    )
    return mock_connection
