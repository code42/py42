from py42._internal.archive_access import ArchiveAccessorManager
from py42._internal.clients.archive import ArchiveClient
from py42.modules.archive import ArchiveModule


def _get_module(mocker):
    client = mocker.MagicMock(spec=ArchiveClient)
    accessor = mocker.MagicMock(spec=ArchiveAccessorManager)
    return ArchiveModule(accessor, client)


class TestArchiveModule(object):

    _TEST_DAYS = 42
    _TEST_ID = 424242

    def test_get_all_org_restore_history_calls_get_all_restore_history_with_expected_id(
        self, mocker
    ):
        archive = _get_module(mocker)
        archive.get_all_org_restore_history(self._TEST_DAYS, self._TEST_ID)
        archive._archive_client.get_all_restore_history.assert_called_once_with(
            self._TEST_DAYS, "orgId", self._TEST_ID
        )

    def test_get_all_user_restore_history_calls_get_all_restore_history_with_expected_id(
        self, mocker
    ):
        archive = _get_module(mocker)
        archive.get_all_user_restore_history(self._TEST_DAYS, self._TEST_ID)
        archive._archive_client.get_all_restore_history.assert_called_once_with(
            self._TEST_DAYS, "userId", self._TEST_ID
        )

    def test_get_all_device_restore_history_calls_get_all_restore_history_with_expected_id(
        self, mocker
    ):
        archive = _get_module(mocker)
        archive.get_all_device_restore_history(self._TEST_DAYS, self._TEST_ID)
        archive._archive_client.get_all_restore_history.assert_called_once_with(
            self._TEST_DAYS, "computerId", self._TEST_ID
        )

    def test_update_cold_storage_purge_date_calls_update_cold_storage_with_expected_data(
        self, mocker
    ):
        archive = _get_module(mocker)
        archive.update_cold_storage_purge_date(u"123", u"2020-04-24")
        archive._archive_client.update_cold_storage_purge_date.assert_called_once_with(
            u"123", u"2020-04-24"
        )
