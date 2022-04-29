import pytest
from tests.conftest import create_mock_response
from tests.conftest import get_file_selection
from tests.conftest import TEST_ACCEPTING_GUID
from tests.conftest import TEST_BACKUP_SET_ID
from tests.conftest import TEST_DESTINATION_GUID_1
from tests.conftest import TEST_DEVICE_GUID
from tests.conftest import TEST_ENCRYPTION_KEY
from tests.conftest import TEST_PASSWORD
from tests.conftest import TEST_RESTORE_PATH

from py42.clients._archiveaccess import ArchiveContentPusher
from py42.clients._archiveaccess import ArchiveContentStreamer
from py42.clients._archiveaccess import ArchiveExplorer
from py42.clients._archiveaccess import FileType
from py42.clients._archiveaccess.accessorfactory import ArchiveAccessorFactory
from py42.clients.archive import ArchiveClient
from py42.exceptions import Py42Error


TEST_ARCHIVE_GUID = "4224"
TEST_DAYS = 42
TEST_ORG_ID = 424242
TEST_PATHS = ["path/to/first/file", "path/to/second/file"]
TEST_FILE_SELECTIONS = [
    get_file_selection(TEST_PATHS[0], FileType.FILE),
    get_file_selection(TEST_PATHS[1], FileType.FILE),
]


@pytest.fixture
def archive_accessor_factory(mocker):
    return mocker.MagicMock(spec=ArchiveAccessorFactory)


@pytest.fixture
def archive_content_streamer(mocker):
    mock = mocker.MagicMock(spec=ArchiveContentStreamer)
    mock.destination_guid = TEST_DESTINATION_GUID_1
    return mock


@pytest.fixture
def archive_content_pusher(mocker):
    return mocker.MagicMock(spec=ArchiveContentPusher)


@pytest.fixture
def archive_explorer(mocker):
    mock = mocker.MagicMock(spec=ArchiveExplorer)
    mock.destination_guid = TEST_DESTINATION_GUID_1
    mock.create_file_selections.return_value = [
        get_file_selection(TEST_PATHS[0], FileType.FILE),
        get_file_selection(TEST_PATHS[1], FileType.FILE),
    ]
    return mock


class TestArchiveClient:
    def test_get_by_archive_guid_calls_get_single_archive_with_expected_params(
        self, archive_service, archive_accessor_factory
    ):
        archive = ArchiveClient(archive_accessor_factory, archive_service)
        archive.get_by_archive_guid(TEST_ARCHIVE_GUID)
        archive_service.get_single_archive.assert_called_once_with(TEST_ARCHIVE_GUID)

    def test_get_all_by_device_guid_calls_get_all_archives_from_value_with_expected_params(
        self, archive_service, archive_accessor_factory
    ):
        archive = ArchiveClient(archive_accessor_factory, archive_service)
        for _ in archive.get_all_by_device_guid(TEST_DEVICE_GUID):
            pass
        archive_service.get_all_archives_from_value.assert_called_once_with(
            TEST_DEVICE_GUID, "backupSourceGuid"
        )

    def test_stream_from_backup_calls_get_archive_accessor_with_expected_params(
        self, archive_accessor_factory, archive_service
    ):
        archive = ArchiveClient(archive_accessor_factory, archive_service)
        archive.stream_from_backup(
            TEST_PATHS[0],
            TEST_DEVICE_GUID,
            TEST_DESTINATION_GUID_1,
            TEST_PASSWORD,
            TEST_ENCRYPTION_KEY,
        )
        archive_accessor_factory.create_archive_accessor.assert_called_once_with(
            TEST_DEVICE_GUID,
            ArchiveContentStreamer,
            destination_guid=TEST_DESTINATION_GUID_1,
            private_password=TEST_PASSWORD,
            encryption_key=TEST_ENCRYPTION_KEY,
        )

    def test_stream_from_backup_when_given_multiple_paths_calls_archive_accessor_stream_from_backup_with_expected_params(
        self, archive_accessor_factory, archive_service, archive_content_streamer
    ):
        archive_accessor_factory.create_archive_accessor.return_value = (
            archive_content_streamer
        )
        archive = ArchiveClient(archive_accessor_factory, archive_service)
        archive.stream_from_backup(
            TEST_PATHS,
            TEST_DEVICE_GUID,
            TEST_DESTINATION_GUID_1,
            TEST_PASSWORD,
            TEST_ENCRYPTION_KEY,
            file_size_calc_timeout=10000,
            show_deleted=True,
        )
        archive_content_streamer.stream_from_backup.assert_called_once_with(
            TEST_BACKUP_SET_ID,
            TEST_PATHS,
            file_size_calc_timeout=10000,
            show_deleted=True,
        )

    def test_stream_from_backup_when_given_backup_set_id_calls_archive_accessor_stream_from_backup_with_expected_params(
        self,
        mocker,
        archive_accessor_factory,
        archive_service,
        archive_content_streamer,
    ):
        backup_set_text = f'{{"backupSets": [{{"backupSetId": "{TEST_BACKUP_SET_ID}"}}, {{"backupSetId": "1"}}]}}'
        backup_set_response = create_mock_response(mocker, backup_set_text)
        archive_service.get_backup_sets.return_value = backup_set_response
        archive_accessor_factory.create_archive_accessor.return_value = (
            archive_content_streamer
        )
        archive = ArchiveClient(archive_accessor_factory, archive_service)
        archive.stream_from_backup(
            TEST_PATHS,
            TEST_DEVICE_GUID,
            TEST_DESTINATION_GUID_1,
            TEST_PASSWORD,
            TEST_ENCRYPTION_KEY,
            file_size_calc_timeout=10000,
            backup_set_id=TEST_BACKUP_SET_ID,
            show_deleted=True,
        )
        archive_content_streamer.stream_from_backup.assert_called_once_with(
            TEST_BACKUP_SET_ID,
            TEST_PATHS,
            file_size_calc_timeout=10000,
            show_deleted=True,
        )

    def test_stream_from_backup_raises_error_when_given_invalid_backup_set_id(
        self,
        mocker,
        archive_accessor_factory,
        archive_service,
        archive_content_streamer,
    ):
        backup_set_text = f'{{"backupSets": [{{"backupSetId": "{TEST_BACKUP_SET_ID}"}}, {{"backupSetId": "1"}}]}}'
        backup_set_response = create_mock_response(mocker, backup_set_text)
        archive_service.get_backup_sets.return_value = backup_set_response
        archive_accessor_factory.create_archive_accessor.return_value = (
            archive_content_streamer
        )
        archive = ArchiveClient(archive_accessor_factory, archive_service)
        with pytest.raises(Py42Error) as err:
            archive.stream_from_backup(
                TEST_PATHS,
                TEST_DEVICE_GUID,
                TEST_DESTINATION_GUID_1,
                TEST_PASSWORD,
                TEST_ENCRYPTION_KEY,
                file_size_calc_timeout=10000,
                backup_set_id="100",
                show_deleted=True,
            )
        assert (
            "backup_set_id='100' not found in device backup sets: [{'backupSetId': 'backup-set-id'}, {'backupSetId': '1'}]"
            in str(err)
        )

    def test_stream_to_device_calls_accessor_stream_to_device(
        self,
        archive_accessor_factory,
        archive_service,
        archive_explorer,
        archive_content_pusher,
    ):
        archive_accessor_factory.create_archive_accessor.return_value = archive_explorer
        archive_accessor_factory.create_archive_content_pusher.return_value = (
            archive_content_pusher
        )
        archive = ArchiveClient(archive_accessor_factory, archive_service)
        archive.stream_to_device(
            TEST_PATHS,
            TEST_DEVICE_GUID,
            TEST_ACCEPTING_GUID,
            TEST_RESTORE_PATH,
            destination_guid=TEST_DESTINATION_GUID_1,
            archive_password=TEST_PASSWORD,
            encryption_key=TEST_ENCRYPTION_KEY,
            file_size_calc_timeout=100,
            show_deleted=True,
            overwrite_existing_files=True,
        )
        archive_content_pusher.stream_to_device.assert_called_once_with(
            TEST_RESTORE_PATH,
            TEST_ACCEPTING_GUID,
            TEST_FILE_SELECTIONS,
            TEST_BACKUP_SET_ID,
            True,
            True,
        )

    def test_stream_to_device_prefers_backup_set_id_of_1_if_no_backup_set_provided(
        self,
        mocker,
        archive_accessor_factory,
        archive_service,
        archive_explorer,
        archive_content_pusher,
    ):
        backup_set_text = f'{{"backupSets": [{{"backupSetId": "{TEST_BACKUP_SET_ID}"}}, {{"backupSetId": "1"}}]}}'
        backup_set_response = create_mock_response(mocker, backup_set_text)
        archive_service.get_backup_sets.return_value = backup_set_response
        archive_accessor_factory.create_archive_accessor.return_value = archive_explorer
        archive_accessor_factory.create_archive_content_pusher.return_value = (
            archive_content_pusher
        )
        archive = ArchiveClient(archive_accessor_factory, archive_service)
        archive.stream_to_device(
            TEST_PATHS,
            TEST_DEVICE_GUID,
            TEST_ACCEPTING_GUID,
            TEST_RESTORE_PATH,
            destination_guid=TEST_DESTINATION_GUID_1,
            archive_password=TEST_PASSWORD,
            encryption_key=TEST_ENCRYPTION_KEY,
            file_size_calc_timeout=100,
            show_deleted=True,
        )
        archive_content_pusher.stream_to_device.assert_called_once_with(
            TEST_RESTORE_PATH,
            TEST_ACCEPTING_GUID,
            TEST_FILE_SELECTIONS,
            "1",
            True,
            False,
        )

    def test_stream_to_device_uses_provided_backup_set_id(
        self,
        mocker,
        archive_accessor_factory,
        archive_service,
        archive_explorer,
        archive_content_pusher,
    ):
        backup_set_text = f'{{"backupSets": [{{"backupSetId": "{TEST_BACKUP_SET_ID}"}}, {{"backupSetId": "1"}}]}}'
        backup_set_response = create_mock_response(mocker, backup_set_text)
        archive_service.get_backup_sets.return_value = backup_set_response
        archive_accessor_factory.create_archive_accessor.return_value = archive_explorer
        archive_accessor_factory.create_archive_content_pusher.return_value = (
            archive_content_pusher
        )
        archive = ArchiveClient(archive_accessor_factory, archive_service)
        archive.stream_to_device(
            TEST_PATHS,
            TEST_DEVICE_GUID,
            TEST_ACCEPTING_GUID,
            TEST_RESTORE_PATH,
            destination_guid=TEST_DESTINATION_GUID_1,
            archive_password=TEST_PASSWORD,
            encryption_key=TEST_ENCRYPTION_KEY,
            file_size_calc_timeout=100,
            backup_set_id=TEST_BACKUP_SET_ID,
            show_deleted=True,
        )
        archive_content_pusher.stream_to_device.assert_called_once_with(
            TEST_RESTORE_PATH,
            TEST_ACCEPTING_GUID,
            TEST_FILE_SELECTIONS,
            TEST_BACKUP_SET_ID,
            True,
            False,
        )

    def test_stream_to_device_raises_error_if_provided_backup_set_id_invalid(
        self,
        mocker,
        archive_accessor_factory,
        archive_service,
        archive_explorer,
        archive_content_pusher,
    ):
        backup_set_text = f'{{"backupSets": [{{"backupSetId": "{TEST_BACKUP_SET_ID}"}}, {{"backupSetId": "1"}}]}}'
        backup_set_response = create_mock_response(mocker, backup_set_text)
        archive_service.get_backup_sets.return_value = backup_set_response
        archive_accessor_factory.create_archive_accessor.return_value = archive_explorer
        archive_accessor_factory.create_archive_content_pusher.return_value = (
            archive_content_pusher
        )
        archive = ArchiveClient(archive_accessor_factory, archive_service)
        with pytest.raises(Py42Error) as err:
            archive.stream_to_device(
                TEST_PATHS,
                TEST_DEVICE_GUID,
                TEST_ACCEPTING_GUID,
                TEST_RESTORE_PATH,
                destination_guid=TEST_DESTINATION_GUID_1,
                archive_password=TEST_PASSWORD,
                encryption_key=TEST_ENCRYPTION_KEY,
                file_size_calc_timeout=100,
                backup_set_id="100",
                show_deleted=True,
            )
        assert (
            "backup_set_id='100' not found in device backup sets: [{'backupSetId': 'backup-set-id'}, {'backupSetId': '1'}]"
            in str(err)
        )

    def test_get_backup_sets_calls_archive_service_get_backup_sets_with_expected_params(
        self, archive_accessor_factory, archive_service
    ):
        archive = ArchiveClient(archive_accessor_factory, archive_service)
        archive.get_backup_sets(TEST_DEVICE_GUID, TEST_DESTINATION_GUID_1)
        archive_service.get_backup_sets.assert_called_once_with(
            TEST_DEVICE_GUID, TEST_DESTINATION_GUID_1
        )

    def test_get_all_org_restore_history_calls_get_all_restore_history_with_expected_id(
        self, archive_accessor_factory, archive_service
    ):
        archive = ArchiveClient(archive_accessor_factory, archive_service)
        archive.get_all_org_restore_history(TEST_DAYS, TEST_ORG_ID)
        archive_service.get_all_restore_history.assert_called_once_with(
            TEST_DAYS, "orgId", TEST_ORG_ID
        )

    def test_get_all_user_restore_history_calls_get_all_restore_history_with_expected_id(
        self, archive_accessor_factory, archive_service
    ):
        archive = ArchiveClient(archive_accessor_factory, archive_service)
        archive.get_all_user_restore_history(TEST_DAYS, TEST_ORG_ID)
        archive_service.get_all_restore_history.assert_called_once_with(
            TEST_DAYS, "userId", TEST_ORG_ID
        )

    def test_get_all_device_restore_history_calls_get_all_restore_history_with_expected_id(
        self, archive_accessor_factory, archive_service
    ):
        archive = ArchiveClient(archive_accessor_factory, archive_service)
        archive.get_all_device_restore_history(TEST_DAYS, TEST_ORG_ID)
        archive_service.get_all_restore_history.assert_called_once_with(
            TEST_DAYS, "computerId", TEST_ORG_ID
        )

    def test_update_cold_storage_purge_date_calls_update_cold_storage_with_expected_data(
        self, archive_accessor_factory, archive_service
    ):
        archive = ArchiveClient(archive_accessor_factory, archive_service)
        archive.update_cold_storage_purge_date("123", "2020-04-24")
        archive_service.update_cold_storage_purge_date.assert_called_once_with(
            "123", "2020-04-24"
        )

    def test_get_all_org_cold_storage_archives_calls_client_with_expected_data(
        self, archive_accessor_factory, archive_service
    ):
        archive = ArchiveClient(archive_accessor_factory, archive_service)
        archive.get_all_org_cold_storage_archives(
            "TEST ORG ID", True, "sort_key", "sort_dir"
        )
        archive_service.get_all_org_cold_storage_archives.assert_called_once_with(
            org_id="TEST ORG ID",
            include_child_orgs=True,
            sort_key="sort_key",
            sort_dir="sort_dir",
        )
