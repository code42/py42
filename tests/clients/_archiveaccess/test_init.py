from py42.clients._archiveaccess import ArchiveAccessor

from tests.clients._archiveaccess.conftest import DEVICE_GUID
from tests.clients._archiveaccess.conftest import WEB_RESTORE_SESSION_ID
from tests.clients._archiveaccess.conftest import mock_get_file_path_metadata_responses



class TestArchiveAccessor(object):
    def test_archive_accessor_constructor_constructs_successfully(
        self, storage_archive_service, restore_job_manager, file_size_poller
    ):
        assert ArchiveAccessor(
            DEVICE_GUID,
            WEB_RESTORE_SESSION_ID,
            storage_archive_service,
            restore_job_manager,
            file_size_poller,
        )

    def test_stream_from_backup_with_root_folder_path_calls_get_stream(
        self, mocker, storage_archive_service, restore_job_manager, file_size_poller
    ):
        mock_get_file_path_metadata_responses(
            mocker, storage_archive_service, [GetFilePathMetadataResponses.NULL_ID]
        )
        archive_accessor = ArchiveAccessor(
            DEVICE_GUID,
            WEB_RESTORE_SESSION_ID,
            storage_archive_service,
            restore_job_manager,
            file_size_poller,
        )
        archive_accessor.stream_from_backup("/", file_size_calc_timeout=0)
        expected_file_selection = [get_file_selection(FileType.DIRECTORY, "/")]
        restore_job_manager.get_stream.assert_called_once_with(expected_file_selection)

    def test_stream_from_backup_with_root_level_folder_calls_get_stream(
        self, mocker, storage_archive_service, restore_job_manager, file_size_poller
    ):
        mock_get_file_path_metadata_responses(
            mocker,
            storage_archive_service,
            [GetFilePathMetadataResponses.NULL_ID, GetFilePathMetadataResponses.ROOT],
        )
        archive_accessor = ArchiveAccessor(
            DEVICE_GUID,
            WEB_RESTORE_SESSION_ID,
            storage_archive_service,
            restore_job_manager,
            file_size_poller,
        )
        archive_accessor.stream_from_backup(USERS_DIR)
        expected_file_selection = [get_file_selection(FileType.DIRECTORY, USERS_DIR)]
        restore_job_manager.get_stream.assert_called_once_with(expected_file_selection)

    def test_stream_from_backup_with_file_path_calls_get_stream(
        self, mocker, storage_archive_service, restore_job_manager, file_size_poller
    ):
        mock_walking_to_downloads_folder(mocker, storage_archive_service)
        archive_accessor = ArchiveAccessor(
            DEVICE_GUID,
            WEB_RESTORE_SESSION_ID,
            storage_archive_service,
            restore_job_manager,
            file_size_poller,
        )
        archive_accessor.stream_from_backup(
            PATH_TO_FILE_IN_DOWNLOADS_FOLDER, file_size_calc_timeout=0
        )
        expected_file_selection = [
            get_file_selection(FileType.FILE, PATH_TO_FILE_IN_DOWNLOADS_FOLDER)
        ]
        restore_job_manager.get_stream.assert_called_once_with(expected_file_selection)

    def test_stream_from_backup_normalizes_windows_paths(
        self, mocker, storage_archive_service, restore_job_manager, file_size_poller,
    ):
        mock_walking_tree_for_windows_path(mocker, storage_archive_service)
        archive_accessor = ArchiveAccessor(
            DEVICE_GUID,
            WEB_RESTORE_SESSION_ID,
            storage_archive_service,
            restore_job_manager,
            file_size_poller,
        )
        archive_accessor.stream_from_backup("C:\\", file_size_calc_timeout=0)
        expected_file_selection = [get_file_selection(FileType.DIRECTORY, "C:/")]
        restore_job_manager.get_stream.assert_called_once_with(expected_file_selection)

    def test_stream_from_backup_calls_get_file_size_with_expected_params(
        self, mocker, storage_archive_service, restore_job_manager, file_size_poller,
    ):
        mock_walking_to_downloads_folder(mocker, storage_archive_service)
        archive_accessor = ArchiveAccessor(
            DEVICE_GUID,
            WEB_RESTORE_SESSION_ID,
            storage_archive_service,
            restore_job_manager,
            file_size_poller,
        )
        archive_accessor.stream_from_backup(
            PATH_TO_FILE_IN_DOWNLOADS_FOLDER, file_size_calc_timeout=10
        )
        file_size_poller.get_file_sizes.assert_called_once_with(
            [DOWNLOADS_ID], timeout=10
        )

    def test_stream_from_backup_when_not_ignoring_file_size_calc_returns_size_sums_from_response(
        self, mocker, storage_archive_service, restore_job_manager, file_size_poller
    ):
        mock_walking_to_downloads_folder(mocker, storage_archive_service)
        archive_accessor = ArchiveAccessor(
            DEVICE_GUID,
            WEB_RESTORE_SESSION_ID,
            storage_archive_service,
            restore_job_manager,
            file_size_poller,
        )

        def get_file_sizes(*args, **kwargs):
            return [
                {"numFiles": 1, "numDirs": 2, "size": 3},
                {"numFiles": 4, "numDirs": 5, "size": 6},
            ]

        file_size_poller.get_file_sizes.side_effect = get_file_sizes
        archive_accessor.stream_from_backup(
            [PATH_TO_FILE_IN_DOWNLOADS_FOLDER, PATH_TO_DESKTOP_FOLDER],
        )
        expected_file_selection = [
            get_file_selection(
                FileType.FILE, PATH_TO_FILE_IN_DOWNLOADS_FOLDER, 1, 2, 3,
            ),
            get_file_selection(FileType.DIRECTORY, PATH_TO_DESKTOP_FOLDER, 4, 5, 6,),
        ]
        restore_job_manager.get_stream.assert_called_once_with(expected_file_selection)

    def test_stream_from_backup_with_file_not_in_archive_raises_exception(
        self, mocker, storage_archive_service, restore_job_manager, file_size_poller,
    ):
        mock_walking_to_downloads_folder(mocker, storage_archive_service)
        archive_accessor = ArchiveAccessor(
            DEVICE_GUID,
            WEB_RESTORE_SESSION_ID,
            storage_archive_service,
            restore_job_manager,
            file_size_poller,
        )
        invalid_path_in_downloads_folder = "/Users/qa/Downloads/file-not-in-archive.txt"
        with pytest.raises(Exception) as e:
            archive_accessor.stream_from_backup(invalid_path_in_downloads_folder)
        expected_message = u"File not found in archive for device device-guid at path {}".format(
            invalid_path_in_downloads_folder
        )
        assert e.value.args[0] == expected_message
        restore_job_manager.get_stream.assert_not_called()

    def test_stream_from_backup_with_unicode_file_path_not_in_archive_raises_exception(
        self, mocker, storage_archive_service, restore_job_manager, file_size_poller,
    ):
        mock_walking_to_downloads_folder(mocker, storage_archive_service)
        archive_accessor = ArchiveAccessor(
            DEVICE_GUID,
            WEB_RESTORE_SESSION_ID,
            storage_archive_service,
            restore_job_manager,
            file_size_poller,
        )
        invalid_path_in_downloads_folder = u"/Users/qa/Downloads/吞"

        with pytest.raises(Py42ArchiveFileNotFoundError) as e:
            archive_accessor.stream_from_backup(invalid_path_in_downloads_folder)
        expected_message = u"File not found in archive for device device-guid at path {}".format(
            invalid_path_in_downloads_folder
        )
        assert e.value.args[0] == expected_message
        restore_job_manager.get_stream.assert_not_called()

    def test_stream_from_backup_with_drive_not_in_archive_raises_exception(
        self, mocker, storage_archive_service, restore_job_manager, file_size_poller,
    ):
        mock_walking_to_downloads_folder(mocker, storage_archive_service)
        archive_accessor = ArchiveAccessor(
            DEVICE_GUID,
            WEB_RESTORE_SESSION_ID,
            storage_archive_service,
            restore_job_manager,
            file_size_poller,
        )
        invalid_path_in_downloads_folder = (
            "C:/Users/qa/Downloads/file-not-in-archive.txt"
        )
        with pytest.raises(Py42ArchiveFileNotFoundError) as e:
            archive_accessor.stream_from_backup(invalid_path_in_downloads_folder)

        expected_message = u"File not found in archive for device device-guid at path {}".format(
            invalid_path_in_downloads_folder
        )
        assert e.value.args[0] == expected_message
        restore_job_manager.get_stream.assert_not_called()

    def test_stream_from_backup_with_case_sensitive_drive_not_in_archive_raises_exception(
        self, mocker, storage_archive_service, restore_job_manager, file_size_poller,
    ):
        mock_walking_to_downloads_folder(mocker, storage_archive_service)
        archive_accessor = ArchiveAccessor(
            DEVICE_GUID,
            WEB_RESTORE_SESSION_ID,
            storage_archive_service,
            restore_job_manager,
            file_size_poller,
        )
        invalid_path_in_downloads_folder = (
            "c:/Users/qa/Downloads/file-not-in-archive.txt"
        )
        with pytest.raises(Py42ArchiveFileNotFoundError) as e:
            archive_accessor.stream_from_backup(invalid_path_in_downloads_folder)

        expected_message = u"File not found in archive for device device-guid at path {}".format(
            invalid_path_in_downloads_folder
        )
        assert e.value.args[0] == expected_message
        restore_job_manager.get_stream.assert_not_called()

    def test_stream_from_backup_uses_show_deleted_param_on_get_file_path_metadata(
        self, mocker, storage_archive_service, restore_job_manager, file_size_poller,
    ):
        mock_walking_to_downloads_folder(mocker, storage_archive_service)
        archive_accessor = ArchiveAccessor(
            DEVICE_GUID,
            WEB_RESTORE_SESSION_ID,
            storage_archive_service,
            restore_job_manager,
            file_size_poller,
        )
        archive_accessor.stream_from_backup(PATH_TO_FILE_IN_DOWNLOADS_FOLDER)
        storage_archive_service.get_file_path_metadata.assert_called_with(
            WEB_RESTORE_SESSION_ID, DEVICE_GUID, file_id=mocker.ANY, show_deleted=True
        )


