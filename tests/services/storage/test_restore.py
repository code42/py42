import pytest
from tests.conftest import create_mock_error
from tests.conftest import TEST_ACCEPTING_GUID
from tests.conftest import TEST_BACKUP_SET_ID
from tests.conftest import TEST_DEVICE_GUID
from tests.conftest import TEST_NODE_GUID
from tests.conftest import TEST_RESTORE_PATH
from tests.conftest import TEST_SESSION_ID
from tests.services.storage.test_archive import TEST_NUM_BYTES
from tests.services.storage.test_archive import TEST_NUM_FILES

from pycpg.exceptions import PycpgBadRequestError
from pycpg.exceptions import PycpgBadRestoreRequestError
from pycpg.services.storage.restore import PushRestoreExistingFiles
from pycpg.services.storage.restore import PushRestoreLocation
from pycpg.services.storage.restore import PushRestoreService


def _create_expected_restore_groups(file):
    return [{"backupSetId": TEST_BACKUP_SET_ID, "files": [file]}]


@pytest.fixture
def mock_restore_connection_with_bad_request(mocker, mock_connection):
    mock_connection.post.side_effect = create_mock_error(
        PycpgBadRequestError, mocker, "CREATE_FAILED"
    )
    return mock_connection


class TestPushRestoreService:
    TEST_PERMISSIONS = "PERMISSIONS"
    EXPECTED_URL = "/api/v9/restore/push"

    def test_start_push_restore_uses_expected_request_parameters(
        self, mock_successful_connection, single_file_selection
    ):
        service = PushRestoreService(mock_successful_connection)
        restore_groups = _create_expected_restore_groups(single_file_selection[0].file)
        service.start_push_restore(
            TEST_DEVICE_GUID,
            TEST_ACCEPTING_GUID,
            TEST_SESSION_ID,
            TEST_NODE_GUID,
            TEST_RESTORE_PATH,
            restore_groups,
            TEST_NUM_FILES,
            TEST_NUM_BYTES,
            show_deleted=False,
            permit_restore_to_different_os_version=True,
            file_permissions=self.TEST_PERMISSIONS,
            restore_full_path=True,
            file_location=PushRestoreLocation.TARGET_DIRECTORY,
            existing_files=PushRestoreExistingFiles.OVERWRITE_ORIGINAL,
        )
        expected_params = {
            "sourceComputerGuid": TEST_DEVICE_GUID,
            "acceptingComputerGuid": TEST_ACCEPTING_GUID,
            "webRestoreSessionId": TEST_SESSION_ID,
            "targetNodeGuid": TEST_NODE_GUID,
            "restorePath": TEST_RESTORE_PATH,
            "restoreGroups": restore_groups,
            "numFiles": TEST_NUM_FILES,
            "numBytes": TEST_NUM_BYTES,
            "showDeleted": False,
            "permitRestoreToDifferentOsVersion": True,
            "filePermissions": self.TEST_PERMISSIONS,
            "restoreFullPath": True,
            "fileLocation": PushRestoreLocation.TARGET_DIRECTORY,
            "existingFiles": PushRestoreExistingFiles.OVERWRITE_ORIGINAL,
        }
        mock_successful_connection.post.assert_called_once_with(
            self.EXPECTED_URL, json=expected_params
        )

    def test_start_push_restore_when_bad_request_raised_with_create_failed_text_raises_bad_restore_error(
        self, mock_restore_connection_with_bad_request, single_file_selection
    ):
        service = PushRestoreService(mock_restore_connection_with_bad_request)
        restore_groups = _create_expected_restore_groups(single_file_selection[0].file)
        with pytest.raises(PycpgBadRestoreRequestError) as err:
            service.start_push_restore(
                TEST_DEVICE_GUID,
                TEST_ACCEPTING_GUID,
                TEST_SESSION_ID,
                TEST_NODE_GUID,
                TEST_RESTORE_PATH,
                restore_groups,
                TEST_NUM_FILES,
                TEST_NUM_BYTES,
                show_deleted=False,
                permit_restore_to_different_os_version=True,
                file_permissions=self.TEST_PERMISSIONS,
                restore_full_path=True,
                file_location=PushRestoreLocation.TARGET_DIRECTORY,
            )
        assert str(err.value) == "Unable to create restore session."
