import pytest

from py42._internal.archive_access import ArchiveAccessor
from py42._internal.archive_access import ArchiveAccessorManager
from py42._internal.clients.archive import ArchiveClient
from py42.modules.archive import ArchiveModule


@pytest.fixture
def archive_client(mocker):
    return mocker.MagicMock(spec=ArchiveClient)


@pytest.fixture
def archive_accessor_manager(mocker):
    return mocker.MagicMock(spec=ArchiveAccessorManager)


@pytest.fixture
def archive_accessor(mocker, archive_accessor_manager):
    return mocker.MagicMock(spec=ArchiveAccessor)


class TestArchiveModule(object):

    _TEST_DAYS = 42
    _TEST_ID = 424242

    def test_get_by_archive_guid_calls_get_single_archive_with_expected_params(
        self, mocker
    ):
        archive_guid = 42
        archive = _get_module(mocker)
        archive.get_by_archive_guid(archive_guid)
        archive._archive_client.get_single_archive.assert_called_once_with(archive_guid)

    def test_get_all_by_device_guid_calls_get_all_archives_from_value_with_expected_params(
        self, mocker
    ):
        device_guid = 42
        archive = _get_module(mocker)
        for _ in archive.get_all_by_device_guid(device_guid):
            pass
        archive._archive_client.get_all_archives_from_value.assert_called_with(
            device_guid, u"backupSourceGuid"
        )

    def test_get_all_by_user_uid_calls_get_all_archives_from_value_with_expected_params(
        self, mocker
    ):
        user_uid = 42
        archive = _get_module(mocker)
        for _ in archive.get_all_by_user_uid(user_uid):
            pass
        archive._archive_client.get_all_archives_from_value.assert_called_with(
            user_uid, u"userUid"
        )

    def test_get_all_by_destination_guid_calls_get_all_archives_from_value_with_expected_params(
        self, mocker
    ):
        destination_guid = 42
        archive = _get_module(mocker)
        for _ in archive.get_all_by_destination_guid(destination_guid):
            pass
        archive._archive_client.get_all_archives_from_value.assert_called_with(
            destination_guid, u"destinationGuid"
        )

    def test_stream_from_backup_calls_get_archive_accessor_with_expected_params(
        self, archive_accessor_manager, archive_client
    ):
        archive = ArchiveModule(archive_accessor_manager, archive_client)
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
        self, archive_accessor_manager, archive_client, archive_accessor
    ):
        archive_accessor_manager.get_archive_accessor.return_value = archive_accessor
        archive = ArchiveModule(archive_accessor_manager, archive_client)
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

    def test_get_backup_sets_calls_archive_client_get_backup_sets_with_expected_params(
        self, archive_accessor_manager, archive_client, archive_accessor
    ):
        archive = ArchiveModule(archive_accessor_manager, archive_client)
        archive.get_backup_sets("device_guid", "dest_guid")
        archive_client.get_backup_sets.assert_called_once_with(
            "device_guid", "dest_guid"
        )

    def test_get_all_org_restore_history_calls_get_all_restore_history_with_expected_id(
        self, archive_accessor_manager, archive_client, archive_accessor
    ):
        archive = ArchiveModule(archive_accessor_manager, archive_client)
        archive.get_all_org_restore_history(self._TEST_DAYS, self._TEST_ID)
        archive_client.get_all_restore_history.assert_called_once_with(
            self._TEST_DAYS, "orgId", self._TEST_ID
        )

    def test_get_all_user_restore_history_calls_get_all_restore_history_with_expected_id(
        self, archive_accessor_manager, archive_client, archive_accessor
    ):
        archive = ArchiveModule(archive_accessor_manager, archive_client)
        archive.get_all_user_restore_history(self._TEST_DAYS, self._TEST_ID)
        archive_client.get_all_restore_history.assert_called_once_with(
            self._TEST_DAYS, "userId", self._TEST_ID
        )

    def test_get_all_device_restore_history_calls_get_all_restore_history_with_expected_id(
        self, archive_accessor_manager, archive_client, archive_accessor
    ):
        archive = ArchiveModule(archive_accessor_manager, archive_client)
        archive.get_all_device_restore_history(self._TEST_DAYS, self._TEST_ID)
        archive_client.get_all_restore_history.assert_called_once_with(
            self._TEST_DAYS, "computerId", self._TEST_ID
        )

    def test_update_cold_storage_purge_date_calls_update_cold_storage_with_expected_data(
        self, archive_accessor_manager, archive_client, archive_accessor
    ):
        archive = ArchiveModule(archive_accessor_manager, archive_client)
        archive.update_cold_storage_purge_date(u"123", u"2020-04-24")
        archive_client.update_cold_storage_purge_date.assert_called_once_with(
            u"123", u"2020-04-24"
        )

    def test_get_all_org_cold_storage_archives_calls_client_with_expected_data(
        self, archive_accessor_manager, archive_client, archive_accessor
    ):
        archive = ArchiveModule(archive_accessor_manager, archive_client)
        archive.get_all_org_cold_storage_archives(
            "TEST ORG ID", True, "sort_key", "sort_dir"
        )
        archive_client.get_all_org_cold_storage_archives.assert_called_once_with(
            org_id="TEST ORG ID",
            include_child_orgs=True,
            sort_key="sort_key",
            sort_dir="sort_dir",
        )
