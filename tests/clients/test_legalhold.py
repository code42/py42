import json

import pytest
from requests import Response

import py42
from py42.clients.legalhold import LegalHoldClient
from py42.sdk.response import Py42Response

LEGAL_HOLD_URI = "/api/LegalHold"

DEFAULT_GET_LEGAL_HOLDS_PARAMS = {
    "active": None,
    "blocked": None,
    "orgUid": None,
    "userUid": None,
    "targetComputerGuid": None,
    "incBackupUsage": None,
    "incCounts": True,
    "pgNum": 1,
    "pgSize": 1000,
    "q": None,
}

MOCK_GET_ALL_MATTERS_RESPONSE = """{"legalHolds":["foo"]}"""

MOCK_EMPTY_GET_ALL_MATTERS_RESPONSE = """{"legalHolds": []}"""

MOCK_GET_ALL_MATTER_CUSTODIANS_RESPONSE = """{"legalHoldMemberships": ["foo"]}"""

MOCK_EMPTY_GET_ALL_MATTER_CUSTODIANS_RESPONSE = """{"legalHoldMemberships": []}"""


class TestLegalHoldClient(object):
    @pytest.fixture
    def mock_get_all_matters_response(self, mocker):
        response = mocker.MagicMock(spec=Response)
        response.status_code = 200
        response.encoding = "utf-8"
        response.text = MOCK_GET_ALL_MATTERS_RESPONSE
        return Py42Response(response)

    @pytest.fixture
    def mock_get_all_matters_empty_response(self, mocker):
        response = mocker.MagicMock(spec=Response)
        response.status_code = 200
        response.encoding = "utf-8"
        response.text = MOCK_EMPTY_GET_ALL_MATTERS_RESPONSE
        return Py42Response(response)

    @pytest.fixture
    def mock_get_all_matter_custodians_response(self, mocker):
        response = mocker.MagicMock(spec=Response)
        response.status_code = 200
        response.encoding = "utf-8"
        response.text = MOCK_GET_ALL_MATTER_CUSTODIANS_RESPONSE
        return Py42Response(response)

    @pytest.fixture
    def mock_get_all_matter_custodians_empty_response(self, mocker):
        response = mocker.MagicMock(spec=Response)
        response.status_code = 200
        response.encoding = "utf-8"
        response.text = MOCK_EMPTY_GET_ALL_MATTER_CUSTODIANS_RESPONSE
        return Py42Response(response)

    def test_get_legal_hold_by_uid_calls_get_with_uri_and_params(
        self, mock_session, successful_response
    ):
        mock_session.get.return_value = successful_response
        client = LegalHoldClient(mock_session)
        client.get_matter_by_uid("LEGAL_HOLD_UID")
        uri = "{0}/{1}".format(LEGAL_HOLD_URI, "LEGAL_HOLD_UID")
        mock_session.get.assert_called_once_with(uri)

    def test_get_all_matters_calls_get_expected_number_of_times(
        self, mock_session, mock_get_all_matters_response, mock_get_all_matters_empty_response
    ):
        py42.sdk.settings.items_per_page = 1
        client = LegalHoldClient(mock_session)
        mock_session.get.side_effect = [
            mock_get_all_matters_response,
            mock_get_all_matters_response,
            mock_get_all_matters_empty_response,
        ]
        for _ in client.get_all_matters():
            pass
        py42.sdk.settings.items_per_page = 1000
        assert mock_session.get.call_count == 3

    def test_get_all_matter_custodians_calls_get_expected_number_of_times(
        self,
        mock_session,
        mock_get_all_matter_custodians_response,
        mock_get_all_matter_custodians_empty_response,
    ):
        py42.sdk.settings.items_per_page = 1
        client = LegalHoldClient(mock_session)
        mock_session.get.side_effect = [
            mock_get_all_matter_custodians_response,
            mock_get_all_matter_custodians_response,
            mock_get_all_matter_custodians_empty_response,
        ]
        for _ in client.get_all_matter_custodians():
            pass
        py42.sdk.settings.items_per_page = 1000
        assert mock_session.get.call_count == 3
