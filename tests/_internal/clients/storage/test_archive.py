import pytest

from py42._internal.clients.storage.archive import StorageArchiveClient
from py42._internal.session import Py42Session

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
EXCEPTIONS_KEY = "exceptions"
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
EXCEPTIONS = [
    {"path": "/dir/file.ext", TIMESTAMP_KEY: TIMESTAMP},
    {"path": "/dir2/file2.ext", TIMESTAMP_KEY: TIMESTAMP},
]
BACKUP_SET_ID = "12345"
WEB_RESTORE_JOB_ID = "46289723"


@pytest.fixture
def session(mocker):
    return mocker.MagicMock(spec=Py42Session)


class TestStorageArchiveClient(object):
    def test_create_web_restore_session_calls_post_with_correct_url(self, mocker, session):
        storage_archive_client = StorageArchiveClient(session)
        storage_archive_client.create_web_restore_session(DEVICE_GUID)
        session.post.assert_called_once_with(WEB_RESTORE_SESSION_URL, json=mocker.ANY)

    def test_create_web_restore_session_with_device_guid_calls_post_with_device_guid_in_json(
        self, session
    ):
        storage_archive_client = StorageArchiveClient(session)
        storage_archive_client.create_web_restore_session(DEVICE_GUID)
        json_arg = session.post.call_args[KWARGS_INDEX][JSON_KEYWORD]
        assert json_arg.get(COMPUTER_GUID_KEY) == DEVICE_GUID

    def test_create_web_restore_session_with_data_key_token_calls_post_with_data_key_token_in_json(
        self, session
    ):
        storage_archive_client = StorageArchiveClient(session)
        storage_archive_client.create_web_restore_session(
            DEVICE_GUID, data_key_token=DATA_KEY_TOKEN
        )
        json_arg = session.post.call_args[KWARGS_INDEX][JSON_KEYWORD]
        assert json_arg.get(DATA_KEY_TOKEN_KEY) == DATA_KEY_TOKEN

    def test_create_web_restore_session_with_private_password_calls_post_with_private_password_in_json(
        self, session
    ):
        storage_archive_client = StorageArchiveClient(session)
        storage_archive_client.create_web_restore_session(
            DEVICE_GUID, private_password=PRIVATE_PASSWORD
        )
        json_arg = session.post.call_args[KWARGS_INDEX][JSON_KEYWORD]
        assert json_arg.get(PRIVATE_PASSWORD_KEY) == PRIVATE_PASSWORD

    def test_create_web_restore_session_with_encryption_key_calls_post_with_encryption_key_in_json(
        self, session
    ):
        storage_archive_client = StorageArchiveClient(session)
        storage_archive_client.create_web_restore_session(
            DEVICE_GUID, encryption_key=ENCRYPTION_KEY
        )
        json_arg = session.post.call_args[KWARGS_INDEX][JSON_KEYWORD]
        assert json_arg.get(ENCRYPTION_KEY_KEY) == ENCRYPTION_KEY

    def test_submit_web_restore_job_calls_post_with_correct_url(self, session):
        storage_archive_client = StorageArchiveClient(session)
        storage_archive_client.submit_web_restore_job(
            DEVICE_GUID, WEB_RESTORE_SESSION_ID, PATH_SET, NUM_FILES, NUM_DIRS, SIZE
        )
        assert session.post.call_args[ARGS_INDEX][ARGS_INDEX] == WEB_RESTORE_JOB_URL

    def test_submit_web_restore_job_with_required_args_calls_post_with_all_args_in_json(
        self, session
    ):
        storage_archive_client = StorageArchiveClient(session)
        storage_archive_client.submit_web_restore_job(
            DEVICE_GUID, WEB_RESTORE_SESSION_ID, PATH_SET, NUM_FILES, NUM_DIRS, SIZE
        )
        json_arg = session.post.call_args[KWARGS_INDEX][JSON_KEYWORD]

        keys = [
            GUID_KEY,
            WEB_RESTORE_SESSION_ID_KEY,
            PATH_SET_KEY,
            NUM_FILES_KEY,
            NUM_DIRS_KEY,
            SIZE_KEY,
            ZIP_RESULT_KEY,
            EXPIRE_JOB_KEY,
            SHOW_DELETED_KEY,
            RESTORE_FULL_PATH_KEY,
            TIMESTAMP_KEY,
            EXCEPTIONS_KEY,
            BACKUP_SET_ID_KEY,
        ]

        assert sorted(json_arg.keys()) == sorted(keys)

    def test_submit_web_restore_job_with_opt_zip_result_as_false_calls_post_with_zip_result_in_data(
        self, session
    ):
        storage_archive_client = StorageArchiveClient(session)
        storage_archive_client.submit_web_restore_job(
            DEVICE_GUID,
            WEB_RESTORE_SESSION_ID,
            PATH_SET,
            NUM_FILES,
            NUM_DIRS,
            SIZE,
            zip_result=False,
        )
        json_arg = session.post.call_args[KWARGS_INDEX][JSON_KEYWORD]
        assert json_arg.get(ZIP_RESULT_KEY) is False

    def test_submit_web_restore_job_with_opt_zip_result_as_true_calls_post_with_zip_result_in_data(
        self, session
    ):
        storage_archive_client = StorageArchiveClient(session)
        storage_archive_client.submit_web_restore_job(
            DEVICE_GUID,
            WEB_RESTORE_SESSION_ID,
            PATH_SET,
            NUM_FILES,
            NUM_DIRS,
            SIZE,
            zip_result=True,
        )
        json_arg = session.post.call_args[KWARGS_INDEX][JSON_KEYWORD]
        assert json_arg.get(ZIP_RESULT_KEY) is True

    def test_submit_web_restore_job_with_expire_job_as_true_calls_post_with_expire_job_in_data(
        self, session
    ):
        storage_archive_client = StorageArchiveClient(session)
        storage_archive_client.submit_web_restore_job(
            DEVICE_GUID,
            WEB_RESTORE_SESSION_ID,
            PATH_SET,
            NUM_FILES,
            NUM_DIRS,
            SIZE,
            expire_job=True,
        )
        json_arg = session.post.call_args[KWARGS_INDEX][JSON_KEYWORD]
        assert json_arg.get(EXPIRE_JOB_KEY) is True

    def test_submit_web_restore_job_with_expire_job_as_false_calls_post_with_expire_job_in_data(
        self, session
    ):
        storage_archive_client = StorageArchiveClient(session)
        storage_archive_client.submit_web_restore_job(
            DEVICE_GUID,
            WEB_RESTORE_SESSION_ID,
            PATH_SET,
            NUM_FILES,
            NUM_DIRS,
            SIZE,
            expire_job=False,
        )
        json_arg = session.post.call_args[KWARGS_INDEX][JSON_KEYWORD]
        assert json_arg.get(EXPIRE_JOB_KEY) is False

    def test_submit_web_restore_job_with_show_deleted_true_calls_post_with_show_deleted_in_data(
        self, session
    ):
        storage_archive_client = StorageArchiveClient(session)
        storage_archive_client.submit_web_restore_job(
            DEVICE_GUID,
            WEB_RESTORE_SESSION_ID,
            PATH_SET,
            NUM_FILES,
            NUM_DIRS,
            SIZE,
            show_deleted=True,
        )
        json_arg = session.post.call_args[KWARGS_INDEX][JSON_KEYWORD]
        assert json_arg.get(SHOW_DELETED_KEY) is True

    def test_submit_web_restore_job_with_show_deleted_false_calls_post_with_show_deleted_false_in_data(
        self, session
    ):
        storage_archive_client = StorageArchiveClient(session)
        storage_archive_client.submit_web_restore_job(
            DEVICE_GUID,
            WEB_RESTORE_SESSION_ID,
            PATH_SET,
            NUM_FILES,
            NUM_DIRS,
            SIZE,
            show_deleted=False,
        )
        json_arg = session.post.call_args[KWARGS_INDEX][JSON_KEYWORD]
        assert json_arg.get(SHOW_DELETED_KEY) is False

    def test_submit_web_restore_job_with_restore_full_path_true_calls_post_with_restore_full_path_true_in_data(
        self, session
    ):
        storage_archive_client = StorageArchiveClient(session)
        storage_archive_client.submit_web_restore_job(
            DEVICE_GUID,
            WEB_RESTORE_SESSION_ID,
            PATH_SET,
            NUM_FILES,
            NUM_DIRS,
            SIZE,
            restore_full_path=True,
        )
        json_arg = session.post.call_args[KWARGS_INDEX][JSON_KEYWORD]
        assert json_arg.get(RESTORE_FULL_PATH_KEY) is True

    def test_submit_web_restore_job_with_restore_full_path_false_calls_post_with_restore_full_path_true_in_data(
        self, session
    ):
        storage_archive_client = StorageArchiveClient(session)
        storage_archive_client.submit_web_restore_job(
            DEVICE_GUID,
            WEB_RESTORE_SESSION_ID,
            PATH_SET,
            NUM_FILES,
            NUM_DIRS,
            SIZE,
            restore_full_path=False,
        )
        json_arg = session.post.call_args[KWARGS_INDEX][JSON_KEYWORD]
        assert json_arg.get(RESTORE_FULL_PATH_KEY) is False

    def test_submit_web_restore_job_with_timestamp_calls_post_with_timestamp_in_data(self, session):
        storage_archive_client = StorageArchiveClient(session)
        storage_archive_client.submit_web_restore_job(
            DEVICE_GUID,
            WEB_RESTORE_SESSION_ID,
            PATH_SET,
            NUM_FILES,
            NUM_DIRS,
            SIZE,
            timestamp=TIMESTAMP,
        )
        json_arg = session.post.call_args[KWARGS_INDEX][JSON_KEYWORD]
        assert json_arg.get(TIMESTAMP_KEY) == TIMESTAMP

    def test_submit_web_restore_job_with_exceptions_calls_post_with_exceptions_in_data(
        self, session
    ):
        storage_archive_client = StorageArchiveClient(session)
        storage_archive_client.submit_web_restore_job(
            DEVICE_GUID,
            WEB_RESTORE_SESSION_ID,
            PATH_SET,
            NUM_FILES,
            NUM_DIRS,
            SIZE,
            exceptions=EXCEPTIONS,
        )
        json_arg = session.post.call_args[KWARGS_INDEX][JSON_KEYWORD]
        assert json_arg.get(EXCEPTIONS_KEY) == EXCEPTIONS

    def test_submit_web_restore_job_with_backup_set_id_calls_post_with_backup_set_id_in_data(
        self, session
    ):
        storage_archive_client = StorageArchiveClient(session)
        storage_archive_client.submit_web_restore_job(
            DEVICE_GUID,
            WEB_RESTORE_SESSION_ID,
            PATH_SET,
            NUM_FILES,
            NUM_DIRS,
            SIZE,
            backup_set_id=BACKUP_SET_ID,
        )
        json_arg = session.post.call_args[KWARGS_INDEX][JSON_KEYWORD]
        assert json_arg.get(BACKUP_SET_ID_KEY) == BACKUP_SET_ID

    def test_submit_web_restore_job_with_all_args_calls_post_with_all_args_in_data(self, session):
        storage_archive_client = StorageArchiveClient(session)
        storage_archive_client.submit_web_restore_job(
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
            exceptions=EXCEPTIONS,
            backup_set_id=BACKUP_SET_ID,
        )
        json_arg = session.post.call_args[KWARGS_INDEX][JSON_KEYWORD]
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
            EXCEPTIONS_KEY: EXCEPTIONS,
            BACKUP_SET_ID_KEY: BACKUP_SET_ID,
        }
        assert json_arg == expected_data

    def test_get_web_restore_job_calls_get_with_correct_url(self, session):
        storage_archive_client = StorageArchiveClient(session)
        storage_archive_client.get_web_restore_job(WEB_RESTORE_JOB_ID)
        expected_url = WEB_RESTORE_JOB_URL + "/" + WEB_RESTORE_JOB_ID
        session.get.assert_called_once_with(expected_url)

    def test_cancel_web_restore_job_calls_delete_with_correct_url(self, mocker, session):
        storage_archive_client = StorageArchiveClient(session)
        storage_archive_client.cancel_web_restore_job(WEB_RESTORE_JOB_ID)
        session.delete.assert_called_once_with(WEB_RESTORE_JOB_URL, json=mocker.ANY)

    def test_cancel_web_restore_job_calls_delete_with_job_id_in_data(self, session):
        storage_archive_client = StorageArchiveClient(session)
        storage_archive_client.cancel_web_restore_job(WEB_RESTORE_JOB_ID)
        json_arg = session.delete.call_args[KWARGS_INDEX][JSON_KEYWORD]
        expected_data = {JOB_ID_KEY: WEB_RESTORE_JOB_ID}
        assert json_arg == expected_data

    def test_get_web_restore_job_result_calls_get_with_correct_url(self, session):
        storage_archive_client = StorageArchiveClient(session)
        storage_archive_client.get_web_restore_job_result(WEB_RESTORE_JOB_ID)
        expected_url = WEB_RESTORE_JOB_RESULT_URL + "/" + WEB_RESTORE_JOB_ID
        session.get.assert_called_once_with(expected_url, stream=True)
