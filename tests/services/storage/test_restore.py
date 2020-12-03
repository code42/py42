from tests.conftest import TEST_ACCEPTING_GUID
from tests.conftest import TEST_BACKUP_SET_ID
from tests.conftest import TEST_DEVICE_GUID
from tests.conftest import TEST_NODE_GUID
from tests.conftest import TEST_RESTORE_PATH
from tests.conftest import TEST_SESSION_ID
from tests.services.storage.test_archive import TEST_NUM_BYTES
from tests.services.storage.test_archive import TEST_NUM_FILES

from py42.services.storage.restore import PushRestoreLocation
from py42.services.storage.restore import PushRestoreService


def _create_expected_restore_groups(file):
    return [{"backupSetId": TEST_BACKUP_SET_ID, "files": [file]}]


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
        }
        mock_successful_connection.post.assert_called_once_with(
            self.EXPECTED_URL, json=expected_params
        )

    #
    # def test_stream_to_device_when_bad_request_raised_with_create_failed_text_raises_bad_restore_error(
    #     self, push_service, restore_job_manager_with_bad_request, file_size_poller,
    # ):
    #     accessor = ArchiveContentPusher(
    #         TEST_DEVICE_GUID,
    #         TEST_DESTINATION_GUID_1,
    #         TEST_NODE_GUID,
    #         TEST_SESSION_ID,
    #         push_service,
    #         restore_job_manager_with_bad_request,
    #         file_size_poller,
    #     )
    # with pytest.raises(Py42BadRestoreError) as err:
    #     accessor.stream_to_device(
    #         TEST_RESTORE_PATH,
    #         TEST_ACCEPTING_GUID,
    #         TEST_DOWNLOADS_DIR,
    #         TEST_BACKUP_SET_ID,
    #         True,
    #     )
    #
    # assert (
    #     str(err.value)
    #     == "Unable to create restore session because of the given arguments."
    # )
    #
    #
    # def test_stream_to_device_when_bad_request_raised_with_create_failed_text_and_unequal_guids_and_restoring_to_original_location_raises_bad_restore_error_with_additional_message(
    #     self, push_service, restore_job_manager_with_bad_request, file_size_poller,
    # ):
    #     accessor = ArchiveContentPusher(
    #         TEST_DEVICE_GUID,
    #         TEST_DESTINATION_GUID_1,
    #         TEST_NODE_GUID,
    #         TEST_SESSION_ID,
    #         push_service,
    #         restore_job_manager_with_bad_request,
    #         file_size_poller,
    #     )
    #     with pytest.raises(Py42BadRestoreError) as err:
    #         accessor.stream_to_device(
    #             TEST_RESTORE_PATH,
    #             TEST_ACCEPTING_GUID,
    #             TEST_DOWNLOADS_DIR,
    #             TEST_BACKUP_SET_ID,
    #             True,
    #             PushRestoreLocation.ORIGINAL,
    #         )
    #
    #     expected = (
    #         "Unable to create restore session because of the given arguments. "
    #         "Warning: Trying to restore to original location when the accepting GUID "
    #         "'{}' is different from the archive source GUID '{}'.".format(
    #             TEST_ACCEPTING_GUID, TEST_DEVICE_GUID
    #         )
    #     )
    #     assert str(err.value) == expected
