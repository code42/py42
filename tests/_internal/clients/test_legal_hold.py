import pytest
from requests import Response

import py42
from py42._internal.clients.legal_hold import LegalHoldClient

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

MOCK_GET_LEGAL_HOLDS_RESPONSE = """{
  "data": {"legalHolds":["foo"]} 
}"""

MOCK_EMPTY_GET_LEGAL_HOLDS_RESPONSE = """{
  "data": {"legalHolds":[]} 
}"""

MOCK_GET_LEGAL_HOLD_MEMBERSHIP_RESPONSE = """{
  "data": {"legalHoldMemberships":["foo"]} 
}"""

MOCK_EMPTY_GET_LEGAL_HOLD_MEMBERSHIP_RESPONSE = """{
  "data": {"legalHoldMemberships":[]} 
}"""


class TestLegalHoldClient(object):
    @pytest.fixture
    def mock_get_legal_holds_response(self, mocker):
        response = mocker.MagicMock(spec=Response)
        response.status_code = 200
        response.text = MOCK_GET_LEGAL_HOLDS_RESPONSE
        return response

    @pytest.fixture
    def mock_get_legal_holds_empty_response(self, mocker):
        response = mocker.MagicMock(spec=Response)
        response.status_code = 200
        response.text = MOCK_EMPTY_GET_LEGAL_HOLDS_RESPONSE
        return response

    @pytest.fixture
    def mock_get_legal_hold_memberships_response(self, mocker):
        response = mocker.MagicMock(spec=Response)
        response.status_code = 200
        response.text = MOCK_GET_LEGAL_HOLD_MEMBERSHIP_RESPONSE
        return response

    @pytest.fixture
    def mock_get_legal_hold_memberships_empty_response(self, mocker):
        response = mocker.MagicMock(spec=Response)
        response.status_code = 200
        response.text = MOCK_EMPTY_GET_LEGAL_HOLD_MEMBERSHIP_RESPONSE
        return response

    def test_get_legal_hold_by_uid_calls_get_with_uri_and_params(
        self, session, v3_required_session
    ):
        client = LegalHoldClient(session, v3_required_session)
        client.get_legal_hold_by_uid("LEGAL_HOLD_UID")
        uri = "{0}/{1}".format(LEGAL_HOLD_URI, "LEGAL_HOLD_UID")
        session.get.assert_called_once_with(uri)

    def test_get_legal_holds_calls_get_expected_number_of_times(
        self,
        session,
        v3_required_session,
        mock_get_legal_holds_response,
        mock_get_legal_holds_empty_response,
    ):
        py42.settings.items_per_page = 1
        client = LegalHoldClient(session, v3_required_session)
        session.get.side_effect = [
            mock_get_legal_holds_response,
            mock_get_legal_holds_response,
            mock_get_legal_holds_empty_response,
        ]
        for page in client.get_legal_holds():
            pass
        py42.settings.items_per_page = 1000
        assert session.get.call_count == 3

    def test_get_legal_hold_memberships_calls_get_expected_number_of_times(
        self,
        session,
        v3_required_session,
        mock_get_legal_hold_memberships_response,
        mock_get_legal_hold_memberships_empty_response,
    ):
        py42.settings.items_per_page = 1
        client = LegalHoldClient(session, v3_required_session)
        session.get.side_effect = [
            mock_get_legal_hold_memberships_response,
            mock_get_legal_hold_memberships_response,
            mock_get_legal_hold_memberships_empty_response,
        ]
        for page in client.get_legal_hold_memberships():
            pass
        py42.settings.items_per_page = 1000
        assert session.get.call_count == 3
