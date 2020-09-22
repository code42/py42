from collections import namedtuple

import pytest
from tests.conftest import create_mock_response
from tests.conftest import TEST_BACKUP_SET_ID
from tests.conftest import TEST_DATA_KEY_TOKEN

from py42.clients._archiveaccess import FileSelection
from py42.services.archive import ArchiveService

param = namedtuple("param", "name new_val expected_stored_val dict_location")

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
