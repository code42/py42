from collections import namedtuple

import pytest
from tests.conftest import create_mock_response
from tests.conftest import TEST_BACKUP_SET_ID
from tests.conftest import TEST_DATA_KEY_TOKEN
from tests.conftest import TEST_DESTINATION_GUID_1
from tests.conftest import TEST_DEVICE_GUID
from tests.conftest import TEST_NODE_GUID

from pycpg.services.archive import ArchiveService

param = namedtuple("param", "name new_val expected_stored_val dict_location")

PHOTOS_REGEX = ".*/Photos/"
PICTURES_REGEX = ".*/Pictures/"
TEST_HOME_DIR = "C:/Users/TestUser/"
TEST_EXTERNAL_DOCUMENTS_DIR = "D:/Documents/"
TEST_PHOTOS_DIR = "C:/Users/TestUser/Pictures/"
TEST_ADDED_PATH = "E:/"
TEST_ADDED_EXCLUDED_PATH = "C:/Users/TestUser/Downloads/"


@pytest.fixture
def archive_service(mocker):
    service = mocker.MagicMock(spec=ArchiveService)
    data_key_text = f'{{"dataKeyToken": "{TEST_DATA_KEY_TOKEN}"}}'
    data_key_response = create_mock_response(mocker, data_key_text)
    service.get_data_key_token.return_value = data_key_response
    backup_set_text = f'{{"backupSets": [{{"backupSetId": "{TEST_BACKUP_SET_ID}"}}]}}'
    backup_set_response = create_mock_response(mocker, backup_set_text)
    service.get_backup_sets.return_value = backup_set_response
    restore_info_text = f'{{"nodeGuid": "{TEST_NODE_GUID}"}}'
    restore_info_resp = create_mock_response(mocker, restore_info_text)

    def get_web_restore_info_side_effect(src_guid, dest_guid):
        if src_guid == TEST_DEVICE_GUID and dest_guid == TEST_DESTINATION_GUID_1:
            return restore_info_resp

    service.get_web_restore_info.side_effect = get_web_restore_info_side_effect
    return service
