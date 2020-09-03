import pytest

from py42.response import Py42Response
from py42.services._connection import Connection
from py42.services.storage.archive import StorageArchiveService

DATA_KEYWORD = "data"
JSON_KEYWORD = "json"
ARGS_INDEX = 0
KWARGS_INDEX = 1

WEB_RESTORE_SESSION_URL = "/api/WebRestoreSession"
WEB_RESTORE_JOB_URL = "/api/WebRestoreJob"
WEB_RESTORE_JOB_RESULT_URL = "/api/WebRestoreJobResult"

COMPUTER_GUID_KEY = "computerGuid"
DATA_KEY_TOKEN_KEY = "dataKeyToken"
PRIVATE_PASSWORD_KEY = "privatePassword"
ENCRYPTION_KEY_KEY = "encryptionKey"

GUID_KEY = "guid"
WEB_RESTORE_SESSION_ID_KEY = "webRestoreSessionId"
PATH_SET_KEY = "pathSet"
NUM_FILES_KEY = "numFiles"
NUM_DIRS_KEY = "numDirs"
SIZE_KEY = "size"
ZIP_RESULT_KEY = "zipResult"
EXPIRE_JOB_KEY = "expireJob"
SHOW_DELETED_KEY = "showDeleted"
RESTORE_FULL_PATH_KEY = "restoreFullPath"
TIMESTAMP_KEY = "timestamp"
BACKUP_SET_ID_KEY = "backupSetId"
JOB_ID_KEY = "jobId"

DEVICE_GUID = "device-guid"
DATA_KEY_TOKEN = "data-key-token"
ENCRYPTION_KEY = "1234567890"
PRIVATE_PASSWORD = "password123"
WEB_RESTORE_SESSION_ID = "56729164827"
FILE_PATH = "/directory/file.txt"
PATH_SET = [{"type": "file", "path": FILE_PATH, "selected": True}]
NUM_FILES = 1
NUM_DIRS = 0
SIZE = 3
ZIP_RESULT = True
TIMESTAMP = 1557139716
BACKUP_SET_ID = "12345"
WEB_RESTORE_JOB_ID = "46289723"

SOURCE_GUID_KEY = "sourceGuid"
TARGET_NODE_GUID_KEY = "targetNodeGuid"
ACCEPTING_GUID_KEY = "acceptingGuid"
RESTORE_PATH_KEY = "restorePath"
NUM_BYTES_KEY = "numBytes"
PUSH_RESTORE_STRATEGY_KEY = "pushRestoreStrategy"
PERMIT_RESTORE_TO_DIFFERENT_OS_VERSION_KEY = "permitRestoreToDifferentOsVersion"
EXISTING_FILES_KEY = "existingFiles"
FILE_PERMISSIONS_KEY = "filePermissions"

NODE_GUID = "node-guid"
ACCEPTING_GUID = "accepting-guid"
RESTORE_PATH = "path/to/restore/to"
PUSH_RESTORE_STRATEGY = "TARGET_DIRECTORY"
EXISTING_FILES = "OVERWRITE_ORIGINAL"
FILE_PERMISSIONS = "CURRENT"


@pytest.fixture
def connection(mocker, py42_response):
    py_session = mocker.MagicMock(spec=Connection)
    py42_response.text = '{"dataKeyToken": "FAKE_DATA_KEY_TOKEN"}'

    py_session.post.return_value = py42_response
    return py_session


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

    def test_start_web_restore_calls_post_with_expected_url_and_data(self, connection):
        storage_archive_service = StorageArchiveService(connection)
        storage_archive_service.start_web_restore(
            DEVICE_GUID,
            WEB_RESTORE_SESSION_ID,
            PATH_SET,
            NUM_FILES,
            NUM_DIRS,
            SIZE,
            zip_result=True,
            expire_job=True,
            show_deleted=True,
            restore_full_path=True,
            timestamp=TIMESTAMP,
            backup_set_id=BACKUP_SET_ID,
        )
        json_arg = connection.post.call_args[KWARGS_INDEX][JSON_KEYWORD]
        expected_data = {
            GUID_KEY: DEVICE_GUID,
            WEB_RESTORE_SESSION_ID_KEY: WEB_RESTORE_SESSION_ID,
            PATH_SET_KEY: PATH_SET,
            NUM_FILES_KEY: NUM_FILES,
            NUM_DIRS_KEY: NUM_DIRS,
            SIZE_KEY: SIZE,
            ZIP_RESULT_KEY: True,
            EXPIRE_JOB_KEY: True,
            SHOW_DELETED_KEY: True,
            RESTORE_FULL_PATH_KEY: True,
            TIMESTAMP_KEY: TIMESTAMP,
            BACKUP_SET_ID_KEY: BACKUP_SET_ID,
        }
        assert json_arg == expected_data

    def test_start_push_restore_calls_post_with_expected_url_and_data(self, connection):
        storage_archive_service = StorageArchiveService(connection)
        storage_archive_service.start_push_restore(
            DEVICE_GUID,
            WEB_RESTORE_SESSION_ID,
            NODE_GUID,
            ACCEPTING_GUID,
            RESTORE_PATH,
            PATH_SET,
            NUM_FILES,
            SIZE,
            show_deleted=True,
            restore_full_path=True,
            timestamp=TIMESTAMP,
            backup_set_id=BACKUP_SET_ID,
            push_restore_strategy=PUSH_RESTORE_STRATEGY,
            existing_files=EXISTING_FILES,
            file_permissions=FILE_PERMISSIONS,
            permit_restore_to_different_os_version=True,
        )
        json_arg = connection.post.call_args[KWARGS_INDEX][JSON_KEYWORD]
        expected_data = {
            SOURCE_GUID_KEY: DEVICE_GUID,
            WEB_RESTORE_SESSION_ID_KEY: WEB_RESTORE_SESSION_ID,
            TARGET_NODE_GUID_KEY: NODE_GUID,
            ACCEPTING_GUID_KEY: ACCEPTING_GUID,
            RESTORE_PATH_KEY: RESTORE_PATH,
            PATH_SET_KEY: PATH_SET,
            NUM_FILES_KEY: NUM_FILES,
            NUM_BYTES_KEY: SIZE,
            SHOW_DELETED_KEY: True,
            RESTORE_FULL_PATH_KEY: True,
            TIMESTAMP_KEY: TIMESTAMP,
            BACKUP_SET_ID_KEY: BACKUP_SET_ID,
            PUSH_RESTORE_STRATEGY_KEY: PUSH_RESTORE_STRATEGY,
            EXISTING_FILES_KEY: EXISTING_FILES,
            FILE_PERMISSIONS_KEY: FILE_PERMISSIONS,
            PERMIT_RESTORE_TO_DIFFERENT_OS_VERSION_KEY: True,
        }
        assert json_arg == expected_data

    def test_get_restore_status_calls_get_with_correct_url(self, mocker, connection):
        storage_archive_service = StorageArchiveService(connection)
        api_response = mocker.MagicMock(spec=Py42Response)
        connection.get.return_value = api_response
        storage_archive_service.get_restore_status(WEB_RESTORE_JOB_ID)
        expected_url = WEB_RESTORE_JOB_URL + "/" + WEB_RESTORE_JOB_ID
        connection.get.assert_called_once_with(expected_url)

    def test_cancel_restore_calls_delete_with_correct_url(self, mocker, connection):
        storage_archive_service = StorageArchiveService(connection)
        api_response = mocker.MagicMock(spec=Py42Response)
        connection.delete.return_value = api_response
        storage_archive_service.cancel_restore(WEB_RESTORE_JOB_ID)
        connection.delete.assert_called_once_with(WEB_RESTORE_JOB_URL, json=mocker.ANY)

    def test_cancel_restore_calls_delete_with_job_id_in_data(self, mocker, connection):
        storage_archive_service = StorageArchiveService(connection)
        api_response = mocker.MagicMock(spec=Py42Response)
        connection.delete.return_value = api_response
        storage_archive_service.cancel_restore(WEB_RESTORE_JOB_ID)
        json_arg = connection.delete.call_args[KWARGS_INDEX][JSON_KEYWORD]
        expected_data = {JOB_ID_KEY: WEB_RESTORE_JOB_ID}
        assert json_arg == expected_data

    def test_stream_restore_result_status_calls_get_with_correct_url(
        self, mocker, connection
    ):
        storage_archive_service = StorageArchiveService(connection)
        api_response = mocker.MagicMock(spec=Py42Response)
        connection.get.return_value = api_response
        storage_archive_service.stream_restore_result(WEB_RESTORE_JOB_ID)
        expected_url = WEB_RESTORE_JOB_RESULT_URL + "/" + WEB_RESTORE_JOB_ID
        connection.get.assert_called_once_with(expected_url, stream=True)
