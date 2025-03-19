import pytest
from requests import HTTPError
from requests import Response
from requests import Session

from pycpg.clients._archiveaccess import FileSelection
from pycpg.clients._archiveaccess import FileType
from pycpg.exceptions import PycpgNotFoundError
from pycpg.exceptions import PycpgUnauthorizedError
from pycpg.response import PycpgResponse
from pycpg.sdk.queries.query_filter import QueryFilter
from pycpg.services._connection import Connection
from pycpg.usercontext import UserContext

TENANT_ID_FROM_RESPONSE = "00000000-0000-0000-0000-000000000000"


@pytest.fixture
def user_context(mocker):
    client = mocker.MagicMock(spec=UserContext)
    client.get_current_tenant_id.return_value = TENANT_ID_FROM_RESPONSE
    return client


HOST_ADDRESS = "http://example.com"

URL = "/api/resource"
DATA_VALUE = "value"
JSON_VALUE = {"key": "value"}

KWARGS_INDEX = 1
DATA_KEY = "data"
JSON_KEY = "json"

TEST_RESPONSE_CONTENT = '{"key":"test_response_content"}'

REQUEST_EXCEPTION_MESSAGE = "Internal server error"
TRACEBACK = "Traceback..."


TEST_ACCEPTING_GUID = "accepting-device-guid"
TEST_ADDED_PATH = "E:/"
TEST_ADDED_EXCLUDED_PATH = "C:/Users/TestUser/Downloads/"
TEST_BACKUP_SET_ID = "backup-set-id"
TEST_COMPUTER_ID = 4290210
TEST_COMPUTER_GUID = 42000000
TEST_COMPUTER_ORG_ID = 424242
TEST_COMPUTER_NAME = "Settings Test Device"
TEST_DATA_KEY_TOKEN = "FAKE_DATA_KEY_TOKEN"
TEST_DEVICE_GUID = "device-guid"
TEST_DESTINATION_GUID_1 = "4200"
TEST_DESTINATION_GUID_2 = "4300"
TEST_DESTINATION_GUID_3 = "4400"
TEST_DESTINATION_NAME_1 = "Dest42"
TEST_DESTINATION_NAME_2 = "Dest43"
TEST_DESTINATION_NAME_3 = "Dest44"
TEST_DEVICE_VERSION = 1525200006800
TEST_DOWNLOADS_FILE_ID = "69e930e774cbc1ee6d0c0ff2ba5804ee"
TEST_CONFIG_DATE_MS = "1577858400000"  # Jan 1, 2020
TEST_DOWNLOADS_DIR = "/Users/qa/Downloads"
TEST_DOWNLOADS_DIR_ID = "f939cfc4d476ec5535ccb0f6c0377ef4"
TEST_ENCRYPTION_KEY = "encryption-key"
TEST_EXTERNAL_DOCUMENTS_DIR = "D:/Documents/"
TEST_FILE_ID = "file-id"
TEST_NODE_GUID = "server-node-guid"
TEST_PASSWORD = "password"
TEST_PATH_TO_FILE_IN_DOWNLOADS_DIR = "/Users/qa/Downloads/terminator-genisys.jpg"
TEST_PHOTOS_DIR = "C:/Users/TestUser/Pictures/"
TEST_RESTORE_PATH = "C:/store/here/"
TEST_SESSION_ID = "FAKE_SESSION_ID"
TEST_USER_ID = 13548744


@pytest.fixture
def http_error():
    return HTTPError(REQUEST_EXCEPTION_MESSAGE)


@pytest.fixture
def successful_response(mocker):
    response = mocker.MagicMock(spec=Response)
    response.text = TEST_RESPONSE_CONTENT
    response.status_code = 200
    response.encoding = None
    return response


@pytest.fixture
def error_response(mocker, http_error):
    error = http_error
    error.response = mocker.MagicMock(spec=Response)
    error.response.text = ""
    error.response.status_code = 500
    error.response.raise_for_status.side_effect = http_error
    return error


@pytest.fixture
def unauthorized_response(mocker, http_error):
    error = http_error
    response = mocker.MagicMock(spec=Response)
    response.text = TEST_RESPONSE_CONTENT
    response.status_code = 401
    response.encoding = None
    error.response = response
    response.raise_for_status.side_effect = [PycpgUnauthorizedError(error)]
    return response


@pytest.fixture
def traceback(mocker):
    format_exc = mocker.patch("traceback.format_exc")
    format_exc.return_value = TRACEBACK
    return format_exc


@pytest.fixture
def success_requests_session(mocker, successful_response):
    session = mocker.MagicMock(spec=Session)
    session.headers = {}
    session.send.return_value = successful_response
    return session


@pytest.fixture
def error_requests_session(mocker, error_response):
    session = mocker.MagicMock(spec=Session)
    session.headers = {}
    session.send.return_value = error_response.response
    return session


@pytest.fixture
def unauthorized_requests_session(mocker, unauthorized_response):
    session = mocker.MagicMock(spec=Session)
    session.headers = {}
    session.send.return_value = unauthorized_response
    return session


@pytest.fixture
def renewed_requests_session(mocker, unauthorized_response, successful_response):
    session = mocker.MagicMock(spec=Session)
    session.headers = {}
    # unauthorized, then corrected
    session.send.side_effect = [unauthorized_response, successful_response]
    return session


@pytest.fixture
def exception():
    return Exception()


@pytest.fixture
def mock_connection(mocker):
    connection = mocker.MagicMock(spec=Connection)
    connection._session = mocker.MagicMock(spec=Session)
    connection.headers = {}

    return connection


@pytest.fixture
def mock_successful_connection(mock_connection, successful_response):
    mock_connection.get.return_value = successful_response
    return mock_connection


def create_mock_response(mocker, text, status_code=200):
    response = mocker.MagicMock(spec=Response)
    response.text = text
    response.status_code = status_code
    response.encoding = None
    return PycpgResponse(response)


def create_mock_error(err_class, mocker, text):
    mock_http_error = mocker.MagicMock(spec=HTTPError)
    mock_http_error.response = create_mock_response(mocker, text)
    return err_class(mock_http_error)


@pytest.fixture
def mock_post_not_found_session(mocker, mock_connection):
    response = mocker.MagicMock(spec=Response)
    response.status_code = 404
    exception = mocker.MagicMock(spec=HTTPError)
    exception.response = response
    mock_connection.post.side_effect = PycpgNotFoundError(exception)
    return mock_connection


@pytest.fixture
def single_file_selection():
    return [get_file_selection(FileType.FILE, TEST_PATH_TO_FILE_IN_DOWNLOADS_DIR)]


@pytest.fixture
def double_file_selection():
    return [
        get_file_selection(FileType.FILE, TEST_PATH_TO_FILE_IN_DOWNLOADS_DIR, 1, 2, 3),
        get_file_selection(FileType.DIRECTORY, TEST_DOWNLOADS_DIR, 4, 5, 6),
    ]


def get_file_selection(file_type, file_path, num_files=1, num_dirs=1, num_bytes=1):
    return FileSelection(
        {"fileType": file_type, "path": file_path, "selected": True},
        num_files,
        num_dirs,
        num_bytes,
    )


@pytest.fixture
def mock_error_response(mocker):
    response = mocker.MagicMock(sepc=Response)
    response.status_code = 400
    return response
