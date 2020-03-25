import pytest
from requests import Response

import py42.sdk.settings
from py42.clients.archive import ArchiveClient
from py42.sdk.response import Py42Response


MOCK_GET_ORG_RESPONSE = """{"totalCount": 3000, "restoreEvents": [{"eventName": "foo", "eventUid": "123"}]}"""

MOCK_EMPTY_GET_ORGS_RESPONSE = """{"totalCount": 3000, "restoreEvents": []}"""


class TestArchiveClient(object):
    @pytest.fixture
    def mock_get_all_response(self, mocker):
        response = mocker.MagicMock(spec=Response)
        response.status_code = 200
        response.encoding = "utf-8"
        response.text = MOCK_GET_ORG_RESPONSE
        return Py42Response(response)

    @pytest.fixture
    def mock_get_all_empty_response(self, mocker):
        response = mocker.MagicMock(spec=Response)
        response.status_code = 200
        response.encoding = "utf-8"
        response.text = MOCK_EMPTY_GET_ORGS_RESPONSE
        return Py42Response(response)

    def test_get_all_calls_get_expected_number_of_times(
        self, mock_session, mock_get_all_response, mock_get_all_empty_response
    ):
        py42.sdk.settings.items_per_page = 1
        client = ArchiveClient(mock_session)
        mock_session.get.side_effect = [
            mock_get_all_response,
            mock_get_all_response,
            mock_get_all_empty_response,
        ]
        for _ in client.get_all_restore_history(10, "orgId", "123"):
            pass
        py42.sdk.settings.items_per_page = 1000
        assert mock_session.get.call_count == 3
