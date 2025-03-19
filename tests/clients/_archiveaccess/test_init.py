import pytest
from requests import Response
from tests.conftest import get_file_selection
from tests.conftest import TEST_ACCEPTING_GUID
from tests.conftest import TEST_BACKUP_SET_ID
from tests.conftest import TEST_DESTINATION_GUID_1
from tests.conftest import TEST_DEVICE_GUID
from tests.conftest import TEST_DOWNLOADS_DIR
from tests.conftest import TEST_DOWNLOADS_DIR_ID
from tests.conftest import TEST_DOWNLOADS_FILE_ID
from tests.conftest import TEST_NODE_GUID
from tests.conftest import TEST_PATH_TO_FILE_IN_DOWNLOADS_DIR
from tests.conftest import TEST_RESTORE_PATH
from tests.conftest import TEST_SESSION_ID

from pycpg.clients._archiveaccess import ArchiveContentPusher
from pycpg.clients._archiveaccess import ArchiveContentStreamer
from pycpg.clients._archiveaccess import FileType
from pycpg.exceptions import PycpgArchiveFileNotFoundError
from pycpg.response import PycpgResponse


USERS_DIR = "/Users"
PATH_TO_DOWNLOADS_FOLDER = "/Users/qa/Downloads"


def mock_walking_to_downloads_folder(mocker, storage_archive_service):
    responses = [
        GetFilePathMetadataResponses.NULL_ID,
        GetFilePathMetadataResponses.ROOT,
        GetFilePathMetadataResponses.USERS,
        GetFilePathMetadataResponses.USERS_QA,
        GetFilePathMetadataResponses.USERS_QA_DOWNLOADS,
    ]
    mock_get_file_path_metadata_responses(mocker, storage_archive_service, responses)


def mock_walking_tree_for_windows_path(mocker, storage_archive_service):
    responses = [GetFilePathMetadataResponses.WINDOWS_NULL_ID]
    mock_get_file_path_metadata_responses(mocker, storage_archive_service, responses)


class GetFilePathMetadataResponses:
    @staticmethod
    def get_file_id_from_request(response):
        return response[1]

    WINDOWS_NULL_ID = (
        """[
                {
                    "deleted": false,
                    "lastModified": "2018-06-22T10:08:37.000-05:00",
                    "filename": "/",
                    "lastBackup": "2019-04-12T12:56:55.023-05:00",
                    "lastBackupMs": 1555091815023,
                    "date": "04/12/19 12:56 PM",
                    "path": "C:/",
                    "hidden": false,
                    "lastModifiedMs": 1529680117000,
                    "type": "directory",
                    "id": null
                }
            ]
        """,
        None,
    )
    NULL_ID = (
        """[
                {
                    "deleted": false,
                    "lastModified": "2018-06-22T10:08:37.000-05:00",
                    "filename": "/",
                    "lastBackup": "2019-04-12T12:56:55.023-05:00",
                    "lastBackupMs": 1555091815023,
                    "date": "04/12/19 12:56 PM",
                    "path": "/",
                    "hidden": false,
                    "lastModifiedMs": 1529680117000,
                    "type": "directory",
                    "id": "885bf69dc0168f3624435346d7bf4836"
                }
            ]
        """,
        None,
    )
    ROOT = (
        """[
                {
                    "deleted": false,
                    "lastModified": "2018-06-22T10:02:44.000-05:00",
                    "filename": "Users",
                    "lastBackup": "2019-04-12T12:56:55.090-05:00",
                    "lastBackupMs": 1555091815090,
                    "date": "04/12/19 12:56 PM",
                    "path": "/Users",
                    "hidden": false,
                    "lastModifiedMs": 1529679764000,
                    "type": "directory",
                    "id": "c2dc0a9bc27be41cb84d6ae91f6a0974"
                }
            ]
        """,
        "885bf69dc0168f3624435346d7bf4836",
    )
    USERS = (
        """[
                {
                    "deleted": false,
                    "lastModified": "2018-06-19T14:58:36.000-05:00",
                    "filename": "qa",
                    "lastBackup": "2019-04-12T12:56:55.095-05:00",
                    "lastBackupMs": 1555091815095,
                    "date": "04/12/19 12:56 PM",
                    "path": "/Users/qa",
                    "hidden": false,
                    "lastModifiedMs": 1529438316000,
                    "type": "directory",
                    "id": "8f939e90bae37f9ec860ced08c5ffb7f"
                }
            ]
        """,
        "c2dc0a9bc27be41cb84d6ae91f6a0974",
    )
    USERS_QA = (
        """[
                {{
                    "deleted": false,
                    "lastModified": "2018-06-19T14:54:46.000-05:00",
                    "filename": ".bash_history",
                    "lastBackup": "2019-04-12T13:01:00.832-05:00",
                    "lastBackupMs": 1555092060832,
                    "date": "04/12/19 01:01 PM",
                    "path": "/Users/qa/.bash_history",
                    "hidden": true,
                    "lastModifiedMs": 1529438086000,
                    "type": "file",
                    "id": "97d8328d121983727cf854dc861d1ada"
                }},
                {{
                    "deleted": false,
                    "lastModified": "2018-06-19T14:58:36.000-05:00",
                    "filename": "Applications",
                    "lastBackup": "2019-04-12T13:00:35.478-05:00",
                    "lastBackupMs": 1555092035478,
                    "date": "04/12/19 01:00 PM",
                    "path": "/Users/qa/Applications",
                    "hidden": false,
                    "lastModifiedMs": 1529438316000,
                    "type": "directory",
                    "id": "13cc0e21c1f14ff102206edd44bfc6bc"
                }},
                {{
                    "deleted": false,
                    "lastModified": "2019-04-18T12:56:34.000-05:00",
                    "filename": "Desktop",
                    "lastBackup": "2019-04-19T03:01:11.566-05:00",
                    "lastBackupMs": 1555660871566,
                    "date": "04/19/19 03:01 AM",
                    "path": "/Users/qa/Desktop",
                    "hidden": false,
                    "lastModifiedMs": 1555610194000,
                    "type": "directory",
                    "id": "97c6bd9bff714bd45665130f7f381781"
                }},
                {{
                    "deleted": false,
                    "lastModified": "2018-02-12T12:30:03.000-06:00",
                    "filename": "Documents",
                    "lastBackup": "2019-04-12T13:04:18.169-05:00",
                    "lastBackupMs": 1555092258169,
                    "date": "04/12/19 01:04 PM",
                    "path": "/Users/qa/Documents",
                    "hidden": false,
                    "lastModifiedMs": 1518460203000,
                    "type": "directory",
                    "id": "9db2b57abab79c4a92c939ec82d3dd0e"
                }},
                {{
                    "deleted": false,
                    "lastModified": "2019-04-12T12:58:34.000-05:00",
                    "filename": "Downloads",
                    "lastBackup": "2019-04-12T13:01:00.891-05:00",
                    "lastBackupMs": 1555092060891,
                    "date": "04/12/19 01:01 PM",
                    "path": "/Users/qa/Downloads",
                    "hidden": false,
                    "lastModifiedMs": 1555091914000,
                    "type": "directory",
                    "id": "{0}"
                }},
                {{
                    "deleted": false,
                    "lastModified": "2019-04-12T10:43:49.000-05:00",
                    "filename": "Library",
                    "lastBackup": "2019-04-12T12:59:49.676-05:00",
                    "lastBackupMs": 1555091989676,
                    "date": "04/12/19 12:59 PM",
                    "path": "/Users/qa/Library",
                    "hidden": false,
                    "lastModifiedMs": 1555083829000,
                    "type": "directory",
                    "id": "bcf31dab21a4f7d4f67b812d6c891ed9"
                }}
            ]
        """.format(
            TEST_DOWNLOADS_DIR_ID
        ),
        "8f939e90bae37f9ec860ced08c5ffb7f",
    )
    USERS_QA_DOWNLOADS = (
        """[
                {{
                    "deleted": false,
                    "lastModified": "2019-04-12T12:58:13.000-05:00",
                    "filename": "Terminator II Screenplay.pdf",
                    "lastBackup": "2019-04-12T13:05:10.089-05:00",
                    "lastBackupMs": 1555092310089,
                    "date": "04/12/19 01:05 PM",
                    "path": "/Users/qa/Downloads/Terminator II Screenplay.pdf",
                    "hidden": false,
                    "lastModifiedMs": 1555091893000,
                    "type": "file",
                    "id": "f63aeee85943809ead0cb11cdc773625"
                }},
                {{
                    "deleted": true,
                    "lastModified": "2019-04-12T12:57:43.000-05:00",
                    "filename": "terminator-genisys.jpg",
                    "lastBackup": "2019-04-12T13:05:10.087-05:00",
                    "lastBackupMs": 1555092310087,
                    "date": "04/12/19 01:05 PM",
                    "path": "/Users/qa/Downloads/terminator-genisys.jpg",
                    "hidden": false,
                    "lastModifiedMs": 1555091863000,
                    "type": "file",
                    "id": "{0}"
                }}
            ]
        """.format(
            TEST_DOWNLOADS_FILE_ID
        ),
        "f939cfc4d476ec5535ccb0f6c0377ef4",
    )
    WINDOWS = (
        """[
                {
                    "deleted": true,
                    "lastModified": "2019-04-12T12:57:43.000-05:00",
                    "filename": "terminator-genisys.jpg",
                    "lastBackup": "2019-04-12T13:05:10.087-05:00",
                    "lastBackupMs": 1555092310087,
                    "date": "04/12/19 01:05 PM",
                    "path": "C:/Users/The Terminator/Documents/file.txt",
                    "hidden": false,
                    "lastModifiedMs": 1555091863000,
                    "type": "file",
                    "id": "1234cfc4d467895535abcdf6c00000f4"
                }
            ]
        """,
        "1234cfc4d467895535abcdf6c00000f4",
    )


def get_get_file_path_metadata_mock(mocker, session_id, device_guid, responses):
    """Mock responses to StorageArchiveService.get_file_path_metadata(). Responses are returned in the same order as
    they are in the given `responses` list"""

    file_id_responses = {}
    for response in responses:
        file_id = GetFilePathMetadataResponses.get_file_id_from_request(response)
        if file_id:
            file_id_responses[file_id] = response[0]
        else:
            if None in file_id_responses:
                raise Exception(
                    "Response list already has a response for a 'None' fileId"
                )
            file_id_responses[None] = response[0]

    def mock_get_file_path_metadata(*args, **kwargs):
        if not args[0] == session_id:
            raise Exception("Unexpected archive connection ID")

        if not args[1] == device_guid:
            raise Exception("Unexpected device GUID")

        file_id = kwargs["file_id"]

        if file_id not in file_id_responses:
            raise Exception(f"Unexpected request with file_id: {file_id}")

        mock_response = mocker.MagicMock(spec=Response)
        mock_response.status_code = 200
        mock_response.text = file_id_responses[file_id]
        get_file_path_metadata_response = PycpgResponse(mock_response)

        return get_file_path_metadata_response

    return mock_get_file_path_metadata


def mock_get_file_path_metadata_responses(mocker, storage_archive_service, responses):
    storage_archive_service.get_file_path_metadata.side_effect = (
        get_get_file_path_metadata_mock(
            mocker, TEST_SESSION_ID, TEST_DEVICE_GUID, responses
        )
    )


@pytest.fixture
def single_dir_selection():
    return [get_file_selection(FileType.DIRECTORY, PATH_TO_DOWNLOADS_FOLDER)]


class TestArchiveContentStreamer:
    def test_archive_accessor_constructor_constructs_successfully(
        self, storage_archive_service, restore_job_manager, file_size_poller
    ):
        assert ArchiveContentStreamer(
            TEST_DEVICE_GUID,
            TEST_SESSION_ID,
            TEST_DESTINATION_GUID_1,
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
        archive_accessor = ArchiveContentStreamer(
            TEST_DEVICE_GUID,
            TEST_SESSION_ID,
            TEST_DESTINATION_GUID_1,
            storage_archive_service,
            restore_job_manager,
            file_size_poller,
        )
        archive_accessor.stream_from_backup(
            TEST_BACKUP_SET_ID,
            "/",
            file_size_calc_timeout=0,
            show_deleted=True,
        )
        expected_file_selection = [get_file_selection(FileType.DIRECTORY, "/")]
        restore_job_manager.get_stream.assert_called_once_with(
            TEST_BACKUP_SET_ID, expected_file_selection, show_deleted=True
        )

    def test_stream_from_backup_with_root_level_folder_calls_get_stream(
        self, mocker, storage_archive_service, restore_job_manager, file_size_poller
    ):
        mock_get_file_path_metadata_responses(
            mocker,
            storage_archive_service,
            [GetFilePathMetadataResponses.NULL_ID, GetFilePathMetadataResponses.ROOT],
        )
        archive_accessor = ArchiveContentStreamer(
            TEST_DEVICE_GUID,
            TEST_SESSION_ID,
            TEST_DESTINATION_GUID_1,
            storage_archive_service,
            restore_job_manager,
            file_size_poller,
        )
        archive_accessor.stream_from_backup(
            TEST_BACKUP_SET_ID, USERS_DIR, show_deleted=True
        )
        expected_file_selection = [get_file_selection(FileType.DIRECTORY, USERS_DIR)]
        restore_job_manager.get_stream.assert_called_once_with(
            TEST_BACKUP_SET_ID,
            expected_file_selection,
            show_deleted=True,
        )

    def test_stream_from_backup_with_file_path_calls_get_stream(
        self, mocker, storage_archive_service, restore_job_manager, file_size_poller
    ):
        mock_walking_to_downloads_folder(mocker, storage_archive_service)
        archive_accessor = ArchiveContentStreamer(
            TEST_DEVICE_GUID,
            TEST_SESSION_ID,
            TEST_DESTINATION_GUID_1,
            storage_archive_service,
            restore_job_manager,
            file_size_poller,
        )
        archive_accessor.stream_from_backup(
            TEST_BACKUP_SET_ID,
            TEST_PATH_TO_FILE_IN_DOWNLOADS_DIR,
            file_size_calc_timeout=0,
        )
        expected_file_selection = [
            get_file_selection(FileType.FILE, TEST_PATH_TO_FILE_IN_DOWNLOADS_DIR)
        ]
        restore_job_manager.get_stream.assert_called_once_with(
            TEST_BACKUP_SET_ID,
            expected_file_selection,
            show_deleted=None,
        )

    def test_stream_from_backup_normalizes_windows_paths(
        self,
        mocker,
        storage_archive_service,
        restore_job_manager,
        file_size_poller,
    ):
        mock_walking_tree_for_windows_path(mocker, storage_archive_service)
        archive_accessor = ArchiveContentStreamer(
            TEST_DEVICE_GUID,
            TEST_SESSION_ID,
            TEST_DESTINATION_GUID_1,
            storage_archive_service,
            restore_job_manager,
            file_size_poller,
        )
        archive_accessor.stream_from_backup(
            TEST_BACKUP_SET_ID, "C:\\", file_size_calc_timeout=0
        )
        expected_file_selection = [get_file_selection(FileType.DIRECTORY, "C:/")]
        restore_job_manager.get_stream.assert_called_once_with(
            TEST_BACKUP_SET_ID,
            expected_file_selection,
            show_deleted=None,
        )

    def test_stream_from_backup_calls_get_file_size_with_expected_params(
        self,
        mocker,
        storage_archive_service,
        restore_job_manager,
        file_size_poller,
    ):
        mock_walking_to_downloads_folder(mocker, storage_archive_service)
        archive_accessor = ArchiveContentStreamer(
            TEST_DEVICE_GUID,
            TEST_SESSION_ID,
            TEST_DESTINATION_GUID_1,
            storage_archive_service,
            restore_job_manager,
            file_size_poller,
        )
        archive_accessor.stream_from_backup(
            TEST_BACKUP_SET_ID,
            TEST_PATH_TO_FILE_IN_DOWNLOADS_DIR,
            file_size_calc_timeout=10,
        )
        file_size_poller.get_file_sizes.assert_called_once_with(
            [TEST_DOWNLOADS_FILE_ID], timeout=10
        )

    def test_stream_from_backup_when_not_ignoring_file_size_calc_returns_size_sums_from_response(
        self, mocker, storage_archive_service, restore_job_manager, file_size_poller
    ):
        mock_walking_to_downloads_folder(mocker, storage_archive_service)
        archive_accessor = ArchiveContentStreamer(
            TEST_DEVICE_GUID,
            TEST_SESSION_ID,
            TEST_DESTINATION_GUID_1,
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
            TEST_BACKUP_SET_ID,
            [TEST_PATH_TO_FILE_IN_DOWNLOADS_DIR, TEST_DOWNLOADS_DIR],
        )
        expected_file_selection = [
            get_file_selection(
                FileType.FILE,
                TEST_PATH_TO_FILE_IN_DOWNLOADS_DIR,
                1,
                2,
                3,
            ),
            get_file_selection(
                FileType.DIRECTORY,
                TEST_DOWNLOADS_DIR,
                4,
                5,
                6,
            ),
        ]
        restore_job_manager.get_stream.assert_called_once_with(
            TEST_BACKUP_SET_ID,
            expected_file_selection,
            show_deleted=None,
        )

    def test_stream_from_backup_with_file_not_in_archive_raises_exception(
        self,
        mocker,
        storage_archive_service,
        restore_job_manager,
        file_size_poller,
    ):
        mock_walking_to_downloads_folder(mocker, storage_archive_service)
        archive_accessor = ArchiveContentStreamer(
            TEST_DEVICE_GUID,
            TEST_SESSION_ID,
            TEST_DESTINATION_GUID_1,
            storage_archive_service,
            restore_job_manager,
            file_size_poller,
        )
        invalid_path_in_downloads_folder = "/Users/qa/Downloads/file-not-in-archive.txt"
        with pytest.raises(Exception) as e:
            archive_accessor.stream_from_backup(
                TEST_BACKUP_SET_ID, invalid_path_in_downloads_folder
            )
        expected_message = f"File not found in archive for device device-guid at path {invalid_path_in_downloads_folder}"
        assert e.value.args[0] == expected_message
        restore_job_manager.get_stream.assert_not_called()

    def test_stream_from_backup_with_unicode_file_path_not_in_archive_raises_exception(
        self,
        mocker,
        storage_archive_service,
        restore_job_manager,
        file_size_poller,
    ):
        mock_walking_to_downloads_folder(mocker, storage_archive_service)
        archive_accessor = ArchiveContentStreamer(
            TEST_DEVICE_GUID,
            TEST_SESSION_ID,
            TEST_DESTINATION_GUID_1,
            storage_archive_service,
            restore_job_manager,
            file_size_poller,
        )
        invalid_path_in_downloads_folder = "/Users/qa/Downloads/吞"

        with pytest.raises(PycpgArchiveFileNotFoundError) as e:
            archive_accessor.stream_from_backup(
                TEST_BACKUP_SET_ID, invalid_path_in_downloads_folder
            )
        expected_message = f"File not found in archive for device device-guid at path {invalid_path_in_downloads_folder}"
        assert e.value.args[0] == expected_message
        restore_job_manager.get_stream.assert_not_called()

    def test_stream_from_backup_with_drive_not_in_archive_raises_exception(
        self,
        mocker,
        storage_archive_service,
        restore_job_manager,
        file_size_poller,
    ):
        mock_walking_to_downloads_folder(mocker, storage_archive_service)
        archive_accessor = ArchiveContentStreamer(
            TEST_DEVICE_GUID,
            TEST_SESSION_ID,
            TEST_DESTINATION_GUID_1,
            storage_archive_service,
            restore_job_manager,
            file_size_poller,
        )
        invalid_path_in_downloads_folder = (
            "C:/Users/qa/Downloads/file-not-in-archive.txt"
        )
        with pytest.raises(PycpgArchiveFileNotFoundError) as e:
            archive_accessor.stream_from_backup(
                TEST_BACKUP_SET_ID, invalid_path_in_downloads_folder
            )

        expected_message = f"File not found in archive for device device-guid at path {invalid_path_in_downloads_folder}"
        assert e.value.args[0] == expected_message
        restore_job_manager.get_stream.assert_not_called()

    def test_stream_from_backup_with_case_sensitive_drive_not_in_archive_raises_exception(
        self,
        mocker,
        storage_archive_service,
        restore_job_manager,
        file_size_poller,
    ):
        mock_walking_to_downloads_folder(mocker, storage_archive_service)
        archive_accessor = ArchiveContentStreamer(
            TEST_DEVICE_GUID,
            TEST_SESSION_ID,
            TEST_DESTINATION_GUID_1,
            storage_archive_service,
            restore_job_manager,
            file_size_poller,
        )
        invalid_path_in_downloads_folder = (
            "c:/Users/qa/Downloads/file-not-in-archive.txt"
        )
        with pytest.raises(PycpgArchiveFileNotFoundError) as e:
            archive_accessor.stream_from_backup(
                TEST_BACKUP_SET_ID, invalid_path_in_downloads_folder
            )

        expected_message = f"File not found in archive for device device-guid at path {invalid_path_in_downloads_folder}"
        assert e.value.args[0] == expected_message
        restore_job_manager.get_stream.assert_not_called()

    def test_stream_from_backup_uses_show_deleted_param_on_get_file_path_metadata(
        self,
        mocker,
        storage_archive_service,
        restore_job_manager,
        file_size_poller,
    ):
        mock_walking_to_downloads_folder(mocker, storage_archive_service)
        archive_accessor = ArchiveContentStreamer(
            TEST_DEVICE_GUID,
            TEST_SESSION_ID,
            TEST_DESTINATION_GUID_1,
            storage_archive_service,
            restore_job_manager,
            file_size_poller,
        )
        archive_accessor.stream_from_backup(TEST_BACKUP_SET_ID, TEST_DOWNLOADS_DIR)
        storage_archive_service.get_file_path_metadata.assert_called_with(
            TEST_SESSION_ID,
            TEST_DEVICE_GUID,
            TEST_BACKUP_SET_ID,
            file_id=mocker.ANY,
            show_deleted=True,
        )


class TestArchiveContentPusher:
    def test_stream_to_device_calls_restore_manager_with_expected_args(
        self, push_service, restore_job_manager, file_size_poller
    ):
        accessor = ArchiveContentPusher(
            TEST_DEVICE_GUID,
            TEST_DESTINATION_GUID_1,
            TEST_NODE_GUID,
            TEST_SESSION_ID,
            push_service,
            restore_job_manager,
            file_size_poller,
        )
        accessor.stream_to_device(
            TEST_RESTORE_PATH,
            TEST_ACCEPTING_GUID,
            TEST_DOWNLOADS_DIR,
            TEST_BACKUP_SET_ID,
            True,
            True,
        )
        restore_job_manager.send_stream.assert_called_once_with(
            TEST_RESTORE_PATH,
            TEST_NODE_GUID,
            TEST_ACCEPTING_GUID,
            TEST_DOWNLOADS_DIR,
            TEST_BACKUP_SET_ID,
            True,
            True,
        )
