# -*- coding: utf-8 -*-
import pytest
from requests import Response

import py42
from py42.clients.archives import ArchiveClient
from py42.response import Py42Response

ARCHIVE_URI = "/api/Archive"

DEFAULT_GET_ARCHIVES_PARAMS = {
    "pgNum": 1,
    "pgSize": 100,
}

MOCK_GET_ARCHIVE_RESPONSE = """{"totalCount": 3000, "archives": ["foo"]}"""

MOCK_EMPTY_GET_ARCHIVE_RESPONSE = """{"totalCount": 3000, "archives": []}"""

class TestArchiveClient(object):
    @pytest.fixture
    def mock_get_archives_response(self, mocker):
        response = mocker.MagicMock(spec=Response)
        response.status_code = 200
        response.encoding = "utf-8"
        response.text = MOCK_GET_ARCHIVE_RESPONSE
        return Py42Response(response)

    @pytest.fixture
    def mock_get_archives_empty_response(self, mocker):
        response = mocker.MagicMock(spec=Response)
        response.status_code = 200
        response.encoding = "utf-8"
        response.text = MOCK_EMPTY_GET_ARCHIVE_RESPONSE
        return Py42Response(response)

    def test_get_by_archive_guid_calls_get_with_expected_uri(
        self, mock_session, successful_response
    ):
        mock_session.get.return_value = successful_response
        client = ArchiveClient(mock_session)
        client.get_by_archive_guid("ARCHIVE_GUID")
        uri = "{}/{}".format(ARCHIVE_URI, "ARCHIVE_GUID")
        mock_session.get.assert_called_once_with(uri)

    def test_get_by_device_guid_calls_get_with_expected_uri_and_data(
        self, mock_session,
    ):
        device_guid = 42
        client = ArchiveClient(mock_session)
        client.get_by_device_guid(device_guid)
        mock_session.get.assert_called_once_with(ARCHIVE_URI,
                                                params={"backupSourceGuid": device_guid})

    def test_get_by_user_uid_calls_get_with_expected_uri_and_data(
        self, mock_session,
    ):
        user_uid = 42
        client = ArchiveClient(mock_session)
        client.get_by_user_uid(user_uid)
        mock_session.get.assert_called_once_with(ARCHIVE_URI,
                                                 params={"userUid": user_uid})

    def test_get_by_user_uid_list_calls_get_expected_number_of_times(
        self, mock_session, mock_get_archives_response, mock_get_archives_empty_response
    ):
        user_uid_list = [1, 2, 3, 4, 5]
        py42.settings.items_per_page = 1
        client = ArchiveClient(mock_session)
        mock_session.get.side_effect = [
            mock_get_archives_response,
            mock_get_archives_response,
            mock_get_archives_empty_response,
        ]
        for _ in client.get_by_user_uid_list(user_uid_list):
            pass
        py42.settings.items_per_page = 500
        assert mock_session.get.call_count == 3

    def test_get_by_user_uid_list_calls_get_with_expect_uri_and_params(
        self, mock_session
    ):
        user_uid_list = [1, 2, 3, 4, 5]
        client = ArchiveClient(mock_session)
        for _ in client.get_by_user_uid_list(user_uid_list):
            pass
        expected_params = {"pgNum": 1, "pgSize": 500, "userUid": "1,2,3,4,5"}
        mock_session.get.assert_called_once_with(ARCHIVE_URI, params=expected_params)








