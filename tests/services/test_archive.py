import pytest
from tests.conftest import create_mock_response

import pycpg.settings
from pycpg.services.archive import ArchiveService

ARCHIVE_URI = "/api/v1/Archive"
DEFAULT_GET_ARCHIVES_PARAMS = {
    "pgNum": 1,
    "pgSize": 100,
}
MOCK_GET_ARCHIVE_RESPONSE = """{"totalCount": 3000, "archives": ["foo"]}"""
MOCK_EMPTY_GET_ARCHIVE_RESPONSE = """{"totalCount": 3000, "archives": []}"""
MOCK_GET_ORG_RESTORE_HISTORY_RESPONSE = """{
    "totalCount": 3000,
    "restoreEvents": [
        {
            "eventName": "foo",
            "eventUid": "123"
        }
    ]
}"""
MOCK_EMPTY_GET_ORG_RESTORE_HISTORY_RESPONSE = (
    """{"totalCount": 3000, "restoreEvents": []}"""
)
MOCK_GET_ORG_COLD_STORAGE_RESPONSE = (
    """{"coldStorageRows": [{"archiveGuid": "fakeguid"}]}"""
)
MOCK_EMPTY_GET_ORG_COLD_STORAGE_RESPONSE = """{"coldStorageRows": []}"""


class TestArchiveService:
    @pytest.fixture
    def mock_get_archives_response(self, mocker):
        return create_mock_response(mocker, MOCK_GET_ARCHIVE_RESPONSE)

    @pytest.fixture
    def mock_get_archives_empty_response(self, mocker):
        return create_mock_response(mocker, MOCK_EMPTY_GET_ARCHIVE_RESPONSE)

    @pytest.fixture
    def mock_get_all_restore_history_response(self, mocker):
        return create_mock_response(mocker, MOCK_GET_ORG_RESTORE_HISTORY_RESPONSE)

    @pytest.fixture
    def mock_get_all_restore_history_empty_response(self, mocker):
        return create_mock_response(mocker, MOCK_EMPTY_GET_ORG_RESTORE_HISTORY_RESPONSE)

    @pytest.fixture
    def mock_get_all_org_cold_storage_response(self, mocker):
        return create_mock_response(mocker, MOCK_GET_ORG_COLD_STORAGE_RESPONSE)

    @pytest.fixture
    def mock_get_all_org_cold_storage_empty_response(self, mocker):
        return create_mock_response(mocker, MOCK_EMPTY_GET_ORG_COLD_STORAGE_RESPONSE)

    def test_get_single_archive_calls_get_with_expected_uri(
        self, mock_connection, successful_response
    ):
        mock_connection.get.return_value = successful_response
        service = ArchiveService(mock_connection)
        service.get_single_archive("ARCHIVE_GUID")
        uri = f"{ARCHIVE_URI}/ARCHIVE_GUID"
        mock_connection.get.assert_called_once_with(uri)

    def test_get_all_archives_from_value_calls_get_expected_number_of_times(
        self,
        mock_connection,
        mock_get_archives_response,
        mock_get_archives_empty_response,
    ):
        device_guid = "42"
        pycpg.settings.items_per_page = 1
        service = ArchiveService(mock_connection)
        mock_connection.get.side_effect = [
            mock_get_archives_response,
            mock_get_archives_response,
            mock_get_archives_empty_response,
        ]
        for _ in service.get_all_archives_from_value(device_guid, "backupSourceGuid"):
            pass
        pycpg.settings.items_per_page = 500
        assert mock_connection.get.call_count == 3

    def test_get_by_value_calls_get_with_expected_uri_and_params(self, mock_connection):
        device_guid = "42"
        service = ArchiveService(mock_connection)
        for _ in service.get_all_archives_from_value(device_guid, "backupSourceGuid"):
            pass
        expected_params = {"pgNum": 1, "pgSize": 500, "backupSourceGuid": "42"}
        mock_connection.get.assert_called_once_with(ARCHIVE_URI, params=expected_params)

    def test_get_all_restore_history_calls_get_expected_number_of_times(
        self,
        mock_connection,
        mock_get_all_restore_history_response,
        mock_get_all_restore_history_empty_response,
    ):
        pycpg.settings.items_per_page = 1
        service = ArchiveService(mock_connection)
        mock_connection.get.side_effect = [
            mock_get_all_restore_history_response,
            mock_get_all_restore_history_response,
            mock_get_all_restore_history_empty_response,
        ]
        for _ in service.get_all_restore_history(10, "orgId", "123"):
            pass
        pycpg.settings.items_per_page = 500
        assert mock_connection.get.call_count == 3

    def test_get_web_restore_info_calls_get_with_expected_url_and_params(
        self, mock_connection
    ):
        service = ArchiveService(mock_connection)
        service.get_web_restore_info("src", "dest")
        expected_params = {"srcGuid": "src", "destGuid": "dest"}
        mock_connection.get.assert_called_once_with(
            "/api/v1/WebRestoreInfo", params=expected_params
        )

    def test_update_cold_storage_purge_date_calls_coldstorage_with_expected_data(
        self, mock_connection
    ):
        service = ArchiveService(mock_connection)
        service.update_cold_storage_purge_date("123", "2020-04-24")
        mock_connection.put.assert_called_once_with(
            "/api/v1/coldStorage/123",
            params={"idType": "guid"},
            json={"archiveHoldExpireDate": "2020-04-24"},
        )

    def test_get_all_org_cold_storage_archives_calls_get_expected_number_of_times(
        self,
        mock_connection,
        mock_get_all_org_cold_storage_response,
        mock_get_all_org_cold_storage_empty_response,
    ):
        pycpg.settings.items_per_page = 1
        service = ArchiveService(mock_connection)
        mock_connection.get.side_effect = [
            mock_get_all_org_cold_storage_response,
            mock_get_all_org_cold_storage_response,
            mock_get_all_org_cold_storage_empty_response,
        ]
        for _ in service.get_all_org_cold_storage_archives("orgId"):
            pass
        pycpg.settings.items_per_page = 500
        assert mock_connection.get.call_count == 3

    def test_get_all_org_cold_storage_archives_calls_get_with_expected_uri_and_params(
        self, mock_connection, mock_get_all_org_cold_storage_empty_response
    ):
        service = ArchiveService(mock_connection)
        mock_connection.get.side_effect = [mock_get_all_org_cold_storage_empty_response]
        for _ in service.get_all_org_cold_storage_archives("orgId"):
            break

        params = {
            "orgId": "orgId",
            "incChildOrgs": True,
            "pgNum": 1,
            "pgSize": 500,
            "srtDir": "asc",
            "srtKey": "archiveHoldExpireDate",
        }
        mock_connection.get.assert_called_once_with(
            "/api/v1/ColdStorage", params=params
        )
