import pytest

from py42.response import Py42Response
from py42.services._connection import Connection
from py42.services.storage.archive import StorageArchiveService

DATA_KEYWORD = "data"
JSON_KEYWORD = "json"
ARGS_INDEX = 0
KWARGS_INDEX = 1

WEB_RESTORE_SESSION_URL = "/api/WebRestoreSession"
START_WEB_RESTORE_JOB_URL = "/api/v9/restore/web"
WEB_RESTORE_JOB_URL = "/api/WebRestoreJob"
WEB_RESTORE_JOB_RESULT_URL = "/api/WebRestoreJobResult"

COMPUTER_GUID_KEY = "computerGuid"
DATA_KEY_TOKEN_KEY = "dataKeyToken"
PRIVATE_PASSWORD_KEY = "privatePassword"
ENCRYPTION_KEY_KEY = "encryptionKey"

DEVICE_GUID_KEY = "sourceComputerGuid"
WEB_RESTORE_SESSION_ID_KEY = "webRestoreSessionId"
RESTORE_GROUPS_KEY = "restoreGroups"
NUM_FILES_KEY = "numFiles"
NUM_DIRS_KEY = "numDirs"
NUM_BYTES_KEY = "numBytes"
EXPIRE_JOB_KEY = "expireJob"
SHOW_DELETED_KEY = "showDeleted"
RESTORE_FULL_PATH_KEY = "restoreFullPath"
RESTORE_TO_SERVER_KEY = "restoreToServer"
JOB_ID_KEY = "jobId"

DEVICE_GUID = "device-guid"
DATA_KEY_TOKEN = "data-key-token"
ENCRYPTION_KEY = "1234567890"
PRIVATE_PASSWORD = "password123"
DEST_GUID = "test-dest-guid"
WEB_RESTORE_SESSION_ID = "56729164827"
FILE_PATH = "/directory/file.txt"
RESTORE_GROUPS = [
    {
        "backupSetId": "BACKUP_SET_ID",
        "files": [{"fileType": "FILE", "path": "some/path", "selected": "true"}],
    }
]
NUM_FILES = 1
NUM_DIRS = 0
NUM_BYTES = 3
BACKUP_SET_ID = "12345"
WEB_RESTORE_JOB_ID = "46289723"


@pytest.fixture
def connection(mocker, py42_response):
    py_connection = mocker.MagicMock(spec=Connection)
    py42_response.text = '{"dataKeyToken": "FAKE_DATA_KEY_TOKEN"}'
    py_connection._auth = mocker.MagicMock()
    py_connection._auth.destination_guid = DEST_GUID
    py_connection.post.return_value = py42_response
    return py_connection


@pytest.fixture
def storage_archive_service(mocker):
    return mocker.MagicMock(spec=StorageArchiveService)


class TestStorageArchiveService(object):
    def test_search_paths_calls_get_with_expected_params(self, connection):
        storage_archive_service = StorageArchiveService(connection)
        storage_archive_service.search_paths(
            "session_id", "device_id", "regex", 1000, "timestamp", True
        )
        connection.get.assert_called_once_with(
            "/api/WebRestoreSearch",
            params={
                "webRestoreSessionId": "session_id",
                "guid": "device_id",
                "regex": "regex",
                "maxResults": 1000,
                "timestamp": "timestamp",
                "showDeleted": True,
            },
        )

    def test_get_file_size_calls_get_with_expected_params(self, connection):
        storage_archive_service = StorageArchiveService(connection)
        storage_archive_service.get_file_size(
            "device_guid", "file_id", "timestamp", True, "backupset_id"
        )
        connection.get.assert_called_once_with(
            u"/api/WebRestoreFileSize",
            params={
                "guid": "device_guid",
                "fileId": "file_id",
                "timestamp": "timestamp",
                "showDeleted": True,
                "backupSetId": "backupset_id",
            },
        )

    def test_create_file_size_job_calls_post_with_expected_params(self, connection):
        storage_archive_service = StorageArchiveService(connection)
        storage_archive_service.create_file_size_job("device_guid", "file_id", 0, False)
        json_dict = {
            "guid": "device_guid",
            "fileId": "file_id",
            "timestamp": 0,
            "showDeleted": False,
        }
        connection.post.assert_called_once_with(
            "/api/WebRestoreFileSizePolling", json=json_dict
        )

    def test_get_file_size_job_calls_get_with_expected_params(self, connection):
        storage_archive_service = StorageArchiveService(connection)
        storage_archive_service.get_file_size_job("job_id", "device_guid")
        connection.get.assert_called_once_with(
            "/api/WebRestoreFileSizePolling",
            params={"jobId": "job_id", "guid": "device_guid"},
        )

    def test_get_file_path_metadata_calls_get_with_expected_params(self, connection):
        storage_archive_service = StorageArchiveService(connection)
        storage_archive_service.get_file_path_metadata(
            "session",
            "guid",
            "file_id",
            "timestamp",
            True,
            "batch_size",
            "lastBatchId",
            "backupset_id",
            True,
        )
        connection.get.assert_called_once_with(
            u"/api/WebRestoreTreeNode",
            params={
                "webRestoreSessionId": "session",
                "guid": "guid",
                "fileId": "file_id",
                "timestamp": "timestamp",
                "showDeleted": True,
                "batchSize": "batch_size",
                "lastBatchFileId": "lastBatchId",
                "backupSetId": "backupset_id",
                "includeOsMetadata": True,
            },
        )

    def test_create_restore_session_calls_post_with_correct_url(
        self, mocker, connection
    ):
        storage_archive_service = StorageArchiveService(connection)
        storage_archive_service.create_restore_session(DEVICE_GUID)
        connection.post.assert_called_once_with(
            WEB_RESTORE_SESSION_URL, json=mocker.ANY
        )

    def test_create_restore_session_with_device_guid_calls_post_with_device_guid_in_json(
        self, connection
    ):
        storage_archive_service = StorageArchiveService(connection)

        storage_archive_service.create_restore_session(DEVICE_GUID)
        json_arg = connection.post.call_args[KWARGS_INDEX][JSON_KEYWORD]
        assert json_arg.get(COMPUTER_GUID_KEY) == DEVICE_GUID

    def test_create_restore_session_with_data_key_token_calls_post_with_data_key_token_in_json(
        self, connection
    ):
        storage_archive_service = StorageArchiveService(connection)

        storage_archive_service.create_restore_session(
            DEVICE_GUID, data_key_token=DATA_KEY_TOKEN
        )
        json_arg = connection.post.call_args[KWARGS_INDEX][JSON_KEYWORD]
        assert json_arg.get(DATA_KEY_TOKEN_KEY) == DATA_KEY_TOKEN

    def test_create_restore_session_with_private_password_calls_post_with_private_password_in_json(
        self, connection
    ):
        storage_archive_service = StorageArchiveService(connection)

        storage_archive_service.create_restore_session(
            DEVICE_GUID, private_password=PRIVATE_PASSWORD
        )
        json_arg = connection.post.call_args[KWARGS_INDEX][JSON_KEYWORD]
        assert json_arg.get(PRIVATE_PASSWORD_KEY) == PRIVATE_PASSWORD

    def test_create_restore_session_with_encryption_key_calls_post_with_encryption_key_in_json(
        self, connection
    ):
        storage_archive_service = StorageArchiveService(connection)

        storage_archive_service.create_restore_session(
            DEVICE_GUID, encryption_key=ENCRYPTION_KEY
        )
        json_arg = connection.post.call_args[KWARGS_INDEX][JSON_KEYWORD]
        assert json_arg.get(ENCRYPTION_KEY_KEY) == ENCRYPTION_KEY

    def test_start_restore_calls_post_with_correct_url(self, connection):
        storage_archive_service = StorageArchiveService(connection)

        storage_archive_service.start_restore(
            DEVICE_GUID,
            WEB_RESTORE_SESSION_ID,
            RESTORE_GROUPS,
            NUM_FILES,
            NUM_DIRS,
            NUM_BYTES,
        )
        assert (
            connection.post.call_args[ARGS_INDEX][ARGS_INDEX]
            == START_WEB_RESTORE_JOB_URL
        )

    def test_start_restore_posts_expected_data_to_expected_url(self, connection):
        storage_archive_service = StorageArchiveService(connection)
        storage_archive_service.start_restore(
            DEVICE_GUID,
            WEB_RESTORE_SESSION_ID,
            RESTORE_GROUPS,
            NUM_FILES,
            NUM_DIRS,
            NUM_BYTES,
            True,
            True,
            True,
            True,
        )
        expected_data = {
            DEVICE_GUID_KEY: DEVICE_GUID,
            WEB_RESTORE_SESSION_ID_KEY: WEB_RESTORE_SESSION_ID,
            RESTORE_GROUPS_KEY: RESTORE_GROUPS,
            NUM_FILES_KEY: NUM_FILES,
            NUM_DIRS_KEY: NUM_DIRS,
            NUM_BYTES_KEY: NUM_BYTES,
            EXPIRE_JOB_KEY: True,
            SHOW_DELETED_KEY: True,
            RESTORE_FULL_PATH_KEY: True,
            RESTORE_TO_SERVER_KEY: True,
        }
        connection.post.assert_called_once_with(
            START_WEB_RESTORE_JOB_URL, json=expected_data
        )

    def test_get_restore_status_calls_get_with_correct_url(self, mocker, connection):
        storage_archive_service = StorageArchiveService(connection)
        api_response = mocker.MagicMock(spec=Py42Response)
        connection.get.return_value = api_response
        storage_archive_service.get_restore_status(WEB_RESTORE_JOB_ID)
        expected_url = WEB_RESTORE_JOB_URL + "/" + WEB_RESTORE_JOB_ID
        connection.get.assert_called_once_with(expected_url)

    def test_cancel_restore_calls_delete_with_correct_url_and_data(
        self, mocker, connection
    ):
        storage_archive_service = StorageArchiveService(connection)
        api_response = mocker.MagicMock(spec=Py42Response)
        connection.delete.return_value = api_response
        storage_archive_service.cancel_restore(WEB_RESTORE_JOB_ID)
        connection.delete.assert_called_once_with(
            WEB_RESTORE_JOB_URL, json={JOB_ID_KEY: WEB_RESTORE_JOB_ID}
        )

    def test_stream_restore_result_status_calls_get_with_correct_url(
        self, mocker, connection
    ):
        storage_archive_service = StorageArchiveService(connection)
        api_response = mocker.MagicMock(spec=Py42Response)
        connection.get.return_value = api_response
        storage_archive_service.stream_restore_result(WEB_RESTORE_JOB_ID)
        expected_url = WEB_RESTORE_JOB_RESULT_URL + "/" + WEB_RESTORE_JOB_ID
        connection.get.assert_called_once_with(expected_url, stream=True)
