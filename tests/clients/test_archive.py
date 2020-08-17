import pytest

from py42.clients._archive_access import ArchiveAccessor
from py42.clients._archive_access import ArchiveAccessorManager
from py42.clients.archive import ArchiveClient
from py42.services.archive import ArchiveService


@pytest.fixture
def archive_service(mocker):
    return mocker.MagicMock(spec=ArchiveService)


@pytest.fixture
def archive_accessor_manager(mocker):
    return mocker.MagicMock(spec=ArchiveAccessorManager)


@pytest.fixture
def archive_accessor(mocker):
    return mocker.MagicMock(spec=ArchiveAccessor)


class TestArchiveClient(object):

    _TEST_DAYS = 42
    _TEST_ID = 424242

    def test_stream_from_backup_calls_get_archive_accessor_with_expected_params(
        self, archive_accessor_manager, archive_service
    ):
        archive = ArchiveClient(archive_accessor_manager, archive_service)
        archive.stream_from_backup(
            "path", "device_guid", "dest_guid", "password", "encryption_key"
        )
        archive._archive_accessor_manager.get_archive_accessor.assert_called_once_with(
            "device_guid",
            destination_guid="dest_guid",
            private_password="password",
            encryption_key="encryption_key",
        )

    def test_stream_from_backup_when_given_multiple_paths_calls_archive_accessor_stream_from_backup_with_expected_params(
        self, archive_accessor_manager, archive_service, archive_accessor
    ):
        archive_accessor_manager.get_archive_accessor.return_value = archive_accessor
        archive = ArchiveClient(archive_accessor_manager, archive_service)
        archive.stream_from_backup(
            ["path/to/first/file", "path/to/second/file"],
            "device_guid",
            "dest_guid",
            "password",
            "encryption_key",
        )
        archive_accessor.stream_from_backup.assert_called_once_with(
            ["path/to/first/file", "path/to/second/file"], file_size_calc_timeout=10
        )

    def test_get_backup_sets_calls_archive_service_get_backup_sets_with_expected_params(
        self, archive_accessor_manager, archive_service, archive_accessor
    ):
        archive = ArchiveClient(archive_accessor_manager, archive_service)
        archive.get_backup_sets("device_guid", "dest_guid")
        archive_service.get_backup_sets.assert_called_once_with(
            "device_guid", "dest_guid"
        )

    def test_get_all_org_restore_history_calls_get_all_restore_history_with_expected_id(
        self, archive_accessor_manager, archive_service, archive_accessor
    ):
        archive = ArchiveClient(archive_accessor_manager, archive_service)
        archive.get_all_org_restore_history(self._TEST_DAYS, self._TEST_ID)
        archive_service.get_all_restore_history.assert_called_once_with(
            self._TEST_DAYS, "orgId", self._TEST_ID
        )

    def test_get_all_user_restore_history_calls_get_all_restore_history_with_expected_id(
        self, archive_accessor_manager, archive_service, archive_accessor
    ):
        archive = ArchiveClient(archive_accessor_manager, archive_service)
        archive.get_all_user_restore_history(self._TEST_DAYS, self._TEST_ID)
        archive_service.get_all_restore_history.assert_called_once_with(
            self._TEST_DAYS, "userId", self._TEST_ID
        )

    def test_get_all_device_restore_history_calls_get_all_restore_history_with_expected_id(
        self, archive_accessor_manager, archive_service, archive_accessor
    ):
        archive = ArchiveClient(archive_accessor_manager, archive_service)
        archive.get_all_device_restore_history(self._TEST_DAYS, self._TEST_ID)
        archive_service.get_all_restore_history.assert_called_once_with(
            self._TEST_DAYS, "computerId", self._TEST_ID
        )

    def test_update_cold_storage_purge_date_calls_update_cold_storage_with_expected_data(
        self, archive_accessor_manager, archive_service, archive_accessor
    ):
        archive = ArchiveClient(archive_accessor_manager, archive_service)
        archive.update_cold_storage_purge_date(u"123", u"2020-04-24")
        archive_service.update_cold_storage_purge_date.assert_called_once_with(
            u"123", u"2020-04-24"
        )

    def test_get_all_org_cold_storage_archives_calls_client_with_expected_data(
        self, archive_accessor_manager, archive_service, archive_accessor
    ):
        archive = ArchiveClient(archive_accessor_manager, archive_service)
        archive.get_all_org_cold_storage_archives(
            "TEST ORG ID", True, "sort_key", "sort_dir"
        )
        archive_service.get_all_org_cold_storage_archives.assert_called_once_with(
            org_id="TEST ORG ID",
            include_child_orgs=True,
            sort_key="sort_key",
            sort_dir="sort_dir",
        )
