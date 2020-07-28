import json

import pytest
from requests import Response

import py42.settings
from py42._internal.clients.archive import ArchiveClient
from py42.response import Py42Response

MOCK_GET_ORG_RESTORE_HISTORY_RESPONSE = """{"totalCount": 3000, "restoreEvents": [{"eventName": "foo", "eventUid": "123"}]}"""

MOCK_EMPTY_GET_ORG_RESTORE_HISTORY_RESPONSE = (
    """{"totalCount": 3000, "restoreEvents": []}"""
)

MOCK_GET_ORG_COLD_STORAGE_RESPONSE = (
    """{"coldStorageRows": [{"archiveGuid": "fakeguid"}]}"""
)

MOCK_EMPTY_GET_ORG_COLD_STORAGE_RESPONSE = """{"coldStorageRows": []}"""


class TestArchiveClient(object):
    @pytest.fixture
    def mock_get_all_restore_history_response(self, mocker):
        response = mocker.MagicMock(spec=Response)
        response.status_code = 200
        response.encoding = "utf-8"
        response.text = MOCK_GET_ORG_RESTORE_HISTORY_RESPONSE
        return Py42Response(response)

    @pytest.fixture
    def mock_get_all_restore_history_empty_response(self, mocker):
        response = mocker.MagicMock(spec=Response)
        response.status_code = 200
        response.encoding = "utf-8"
        response.text = MOCK_EMPTY_GET_ORG_RESTORE_HISTORY_RESPONSE
        return Py42Response(response)

    @pytest.fixture
    def mock_get_all_org_cold_storage_response(self, mocker):
        response = mocker.MagicMock(spec=Response)
        response.status_code = 200
        response.encoding = "utf-8"
        response.text = MOCK_GET_ORG_COLD_STORAGE_RESPONSE
        return Py42Response(response)

    @pytest.fixture
    def mock_get_all_org_cold_storage_empty_response(self, mocker):
        response = mocker.MagicMock(spec=Response)
        response.status_code = 200
        response.encoding = "utf-8"
        response.text = MOCK_EMPTY_GET_ORG_COLD_STORAGE_RESPONSE
        return Py42Response(response)

    def test_get_all_restore_history_calls_get_expected_number_of_times(
        self,
        mock_session,
        mock_get_all_restore_history_response,
        mock_get_all_restore_history_empty_response,
    ):
        py42.settings.items_per_page = 1
        client = ArchiveClient(mock_session)
        mock_session.get.side_effect = [
            mock_get_all_restore_history_response,
            mock_get_all_restore_history_response,
            mock_get_all_restore_history_empty_response,
        ]
        for _ in client.get_all_restore_history(10, "orgId", "123"):
            pass
        py42.settings.items_per_page = 500
        assert mock_session.get.call_count == 3

    def test_update_cold_storage_purge_date_calls_coldstorage_with_expected_data(
        self, mock_session
    ):
        client = ArchiveClient(mock_session)
        client.update_cold_storage_purge_date(u"123", u"2020-04-24")
        mock_session.put.assert_called_once_with(
            u"/api/coldStorage/123",
            params={u"idType": u"guid"},
            data=json.dumps({u"archiveHoldExpireDate": u"2020-04-24"}),
        )

    def test_get_all_org_cold_storage_archives_calls_get_expected_number_of_times(
        self,
        mock_session,
        mock_get_all_org_cold_storage_response,
        mock_get_all_org_cold_storage_empty_response,
    ):
        py42.settings.items_per_page = 1
        client = ArchiveClient(mock_session)
        mock_session.get.side_effect = [
            mock_get_all_org_cold_storage_response,
            mock_get_all_org_cold_storage_response,
            mock_get_all_org_cold_storage_empty_response,
        ]
        for _ in client.get_all_org_cold_storage_archives("orgId"):
            pass
        py42.settings.items_per_page = 500
        assert mock_session.get.call_count == 3

    def test_get_all_org_cold_storage_archives_calls_get_with_expected_uri_and_params(
        self, mock_session, mock_get_all_org_cold_storage_empty_response
    ):
        client = ArchiveClient(mock_session)
        mock_session.get.side_effect = [mock_get_all_org_cold_storage_empty_response]
        for _ in client.get_all_org_cold_storage_archives("orgId"):
            break

        params = {
            "orgId": "orgId",
            "incChildOrgs": True,
            "pgNum": 1,
            "pgSize": 500,
            "srtDir": "asc",
            "srtKey": "archiveHoldExpireDate",
        }
        mock_session.get.assert_called_once_with("/api/ColdStorage", params=params)
