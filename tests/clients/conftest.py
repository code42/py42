from collections import namedtuple

import pytest
from tests.conftest import create_mock_response

from py42.clients._archiveaccess import FileSelection
from py42.services.archive import ArchiveService

param = namedtuple("param", "name new_val expected_stored_val dict_location")

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

PHOTOS_REGEX = ".*/Photos/"
PICTURES_REGEX = ".*/Pictures/"


@pytest.fixture
def archive_service(mocker):
    service = mocker.MagicMock(spec=ArchiveService)
    data_key_text = '{{"dataKeyToken": "{0}"}}'.format(TEST_DATA_KEY_TOKEN)
    data_key_response = create_mock_response(mocker, data_key_text)
    service.get_data_key_token.return_value = data_key_response
    backup_set_text = '{{"backupSets": [{{"backupSetId": "{0}"}}]}}'.format(
        TEST_BACKUP_SET_ID
    )
    backup_set_response = create_mock_response(mocker, backup_set_text)
    service.get_backup_sets.return_value = backup_set_response
    return service


def get_file_selection(file_type, file_path, num_files=1, num_dirs=1, num_bytes=1):
    return FileSelection(
        {"fileType": file_type, "path": file_path, "selected": True},
        num_files,
        num_dirs,
        num_bytes,
    )
