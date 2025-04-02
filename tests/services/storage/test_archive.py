import pytest
from requests import HTTPError
from requests import Response
from tests.conftest import create_mock_response
from tests.conftest import TEST_BACKUP_SET_ID
from tests.conftest import TEST_DATA_KEY_TOKEN
from tests.conftest import TEST_DESTINATION_GUID_1
from tests.conftest import TEST_DEVICE_GUID
from tests.conftest import TEST_ENCRYPTION_KEY
from tests.conftest import TEST_PASSWORD
from tests.conftest import TEST_SESSION_ID

from pycpg.exceptions import PycpgInternalServerError
from pycpg.exceptions import PycpgInvalidArchiveEncryptionKey
from pycpg.exceptions import PycpgInvalidArchivePassword
from pycpg.response import PycpgResponse
from pycpg.services._connection import Connection
from pycpg.services.storage.archive import StorageArchiveService


JSON_KEYWORD = "json"
ARGS_INDEX = 0
KWARGS_INDEX = 1

WEB_RESTORE_SESSION_URL = "/api/v1/WebRestoreSession"
START_WEB_RESTORE_JOB_URL = "/api/v9/restore/web"
WEB_RESTORE_JOB_URL = "/api/v1/WebRestoreJob"
WEB_RESTORE_JOB_RESULT_URL = "/api/v1/WebRestoreJobResult"


FILE_PATH = "/directory/file.txt"
RESTORE_GROUPS = [
    {
        "backupSetId": "BACKUP_SET_ID",
        "files": [{"fileType": "FILE", "path": "some/path", "selected": "true"}],
    }
]


TEST_NUM_FILES = 1
TEST_NUM_DIRS = 0
TEST_NUM_BYTES = 3
TEST_JOB_ID = "46289723"


@pytest.fixture
def connection(mocker):
    py_connection = mocker.MagicMock(spec=Connection)
    py_connection._auth = mocker.MagicMock()
    py_connection._auth.destination_guid = TEST_DESTINATION_GUID_1
    py_connection.post.return_value = create_mock_response(
        mocker, '{"dataKeyToken": "FAKE_DATA_KEY_TOKEN"}'
    )
    return py_connection


@pytest.fixture
def storage_archive_service(mocker):
    return mocker.MagicMock(spec=StorageArchiveService)


class TestStorageArchiveService:
    def test_search_paths_calls_get_with_expected_params(self, connection):
        storage_archive_service = StorageArchiveService(connection)
        storage_archive_service.search_paths(
            "session_id", "device_id", "regex", 1000, "timestamp", True
        )
        connection.get.assert_called_once_with(
            "/api/v1/WebRestoreSearch",
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
            "/api/v1/WebRestoreFileSize",
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
            "/api/v1/WebRestoreFileSizePolling", json=json_dict
        )

    def test_get_file_size_job_calls_get_with_expected_params(self, connection):
        storage_archive_service = StorageArchiveService(connection)
        storage_archive_service.get_file_size_job("job_id", "device_guid")
        connection.get.assert_called_once_with(
            "/api/v1/WebRestoreFileSizePolling",
            params={"jobId": "job_id", "guid": "device_guid"},
        )

    def test_get_file_path_metadata_calls_get_with_expected_params(self, connection):
        storage_archive_service = StorageArchiveService(connection)
        storage_archive_service.get_file_path_metadata(
            TEST_SESSION_ID,
            TEST_DEVICE_GUID,
            TEST_BACKUP_SET_ID,
            file_id="file_id",
            timestamp="timestamp",
            show_deleted=True,
            batch_size="batch_size",
            last_batch_file_id="lastBatchId",
            include_os_metadata=True,
        )
        connection.get.assert_called_once_with(
            "/api/v1/WebRestoreTreeNode",
            params={
                "webRestoreSessionId": TEST_SESSION_ID,
                "guid": TEST_DEVICE_GUID,
                "fileId": "file_id",
                "timestamp": "timestamp",
                "showDeleted": True,
                "batchSize": "batch_size",
                "lastBatchFileId": "lastBatchId",
                "backupSetId": TEST_BACKUP_SET_ID,
                "includeOsMetadata": True,
            },
        )

    def test_create_restore_session_calls_post_with_correct_url(
        self, mocker, connection
    ):
        storage_archive_service = StorageArchiveService(connection)
        storage_archive_service.create_restore_session(TEST_DEVICE_GUID)
        connection.post.assert_called_once_with(
            WEB_RESTORE_SESSION_URL, json=mocker.ANY
        )

    def test_create_restore_session_with_device_guid_calls_post_with_device_guid_in_json(
        self, connection
    ):
        storage_archive_service = StorageArchiveService(connection)

        storage_archive_service.create_restore_session(TEST_DEVICE_GUID)
        json_arg = connection.post.call_args[KWARGS_INDEX][JSON_KEYWORD]
        assert json_arg.get("computerGuid") == TEST_DEVICE_GUID

    def test_create_restore_session_with_data_key_token_calls_post_with_data_key_token_in_json(
        self, connection
    ):
        storage_archive_service = StorageArchiveService(connection)

        storage_archive_service.create_restore_session(
            TEST_DEVICE_GUID, data_key_token=TEST_DATA_KEY_TOKEN
        )
        json_arg = connection.post.call_args[KWARGS_INDEX][JSON_KEYWORD]
        assert json_arg.get("dataKeyToken") == TEST_DATA_KEY_TOKEN

    def test_create_restore_session_with_private_password_calls_post_with_private_password_in_json(
        self, connection
    ):
        storage_archive_service = StorageArchiveService(connection)

        storage_archive_service.create_restore_session(
            TEST_DEVICE_GUID, private_password=TEST_PASSWORD
        )
        json_arg = connection.post.call_args[KWARGS_INDEX][JSON_KEYWORD]
        assert json_arg.get("privatePassword") == TEST_PASSWORD

    def test_create_restore_session_when_invalid_password_raises_expected_error(
        self, mocker, connection
    ):
        def side_effect(*args, **kwargs):
            base_err = HTTPError()
            base_err.response = mocker.MagicMock(spec=Response)
            base_err.response.text = """
                [{"name":"PRIVATE_PASSWORD_INVALID","description":"An error has
                occurred. See server logs for more information.","objects":[]}]
            """
            raise PycpgInternalServerError(base_err)

        connection.post.side_effect = side_effect
        storage_archive_service = StorageArchiveService(connection)

        with pytest.raises(PycpgInvalidArchivePassword) as err:
            storage_archive_service.create_restore_session(
                TEST_DEVICE_GUID, private_password=TEST_PASSWORD
            )

        assert "Invalid archive password." in str(err.value)

    def test_create_restore_session_with_encryption_key_calls_post_with_encryption_key_in_json(
        self, connection
    ):
        storage_archive_service = StorageArchiveService(connection)

        storage_archive_service.create_restore_session(
            TEST_DEVICE_GUID, encryption_key=TEST_ENCRYPTION_KEY
        )
        json_arg = connection.post.call_args[KWARGS_INDEX][JSON_KEYWORD]
        assert json_arg.get("encryptionKey") == TEST_ENCRYPTION_KEY

    def test_create_restore_session_when_invalid_encryption_key_raises_expected_error(
        self, mocker, connection
    ):
        def side_effect(*args, **kwargs):
            base_err = HTTPError()
            base_err.response = mocker.MagicMock(spec=Response)
            base_err.response.text = """
                [{"name":"CUSTOM_KEY_INVALID","description":"An error has
                occurred. See server logs for more information.","objects":[]}]
            """
            raise PycpgInternalServerError(base_err)

        connection.post.side_effect = side_effect
        storage_archive_service = StorageArchiveService(connection)

        with pytest.raises(PycpgInvalidArchiveEncryptionKey) as err:
            storage_archive_service.create_restore_session(
                TEST_DEVICE_GUID, encryption_key=TEST_ENCRYPTION_KEY
            )

        assert "Invalid archive encryption key." in str(err.value)

    def test_start_restore_calls_post_with_correct_url(self, connection):
        storage_archive_service = StorageArchiveService(connection)

        storage_archive_service.start_restore(
            TEST_DEVICE_GUID,
            TEST_SESSION_ID,
            RESTORE_GROUPS,
            TEST_NUM_FILES,
            TEST_NUM_DIRS,
            TEST_NUM_BYTES,
        )
        assert (
            connection.post.call_args[ARGS_INDEX][ARGS_INDEX]
            == START_WEB_RESTORE_JOB_URL
        )

    def test_start_restore_posts_expected_data_to_expected_url(self, connection):
        storage_archive_service = StorageArchiveService(connection)
        storage_archive_service.start_restore(
            TEST_DEVICE_GUID,
            TEST_SESSION_ID,
            RESTORE_GROUPS,
            TEST_NUM_FILES,
            TEST_NUM_DIRS,
            TEST_NUM_BYTES,
            True,
            True,
            True,
            True,
        )
        expected_data = {
            "sourceComputerGuid": TEST_DEVICE_GUID,
            "webRestoreSessionId": TEST_SESSION_ID,
            "restoreGroups": RESTORE_GROUPS,
            "numFiles": TEST_NUM_FILES,
            "numDirs": TEST_NUM_DIRS,
            "numBytes": TEST_NUM_BYTES,
            "expireJob": True,
            "showDeleted": True,
            "restoreFullPath": True,
            "restoreToServer": True,
        }
        connection.post.assert_called_once_with(
            START_WEB_RESTORE_JOB_URL, json=expected_data
        )

    def test_get_restore_status_calls_get_with_correct_url(self, mocker, connection):
        storage_archive_service = StorageArchiveService(connection)
        api_response = mocker.MagicMock(spec=PycpgResponse)
        connection.get.return_value = api_response
        storage_archive_service.get_restore_status(TEST_JOB_ID)
        expected_url = WEB_RESTORE_JOB_URL + "/" + TEST_JOB_ID
        connection.get.assert_called_once_with(expected_url)

    def test_cancel_restore_calls_delete_with_correct_url_and_data(
        self, mocker, connection
    ):
        storage_archive_service = StorageArchiveService(connection)
        api_response = mocker.MagicMock(spec=PycpgResponse)
        connection.delete.return_value = api_response
        storage_archive_service.cancel_restore(TEST_JOB_ID)
        connection.delete.assert_called_once_with(
            WEB_RESTORE_JOB_URL, json={"jobId": TEST_JOB_ID}
        )

    def test_stream_restore_result_status_calls_get_with_correct_url(
        self, mocker, connection
    ):
        storage_archive_service = StorageArchiveService(connection)
        api_response = mocker.MagicMock(spec=PycpgResponse)
        connection.get.return_value = api_response
        storage_archive_service.stream_restore_result(TEST_JOB_ID)
        expected_url = WEB_RESTORE_JOB_RESULT_URL + "/" + TEST_JOB_ID
        connection.get.assert_called_once_with(
            expected_url, stream=True, headers={"Accept": "application/octet-stream"}
        )
