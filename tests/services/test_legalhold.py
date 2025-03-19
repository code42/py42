import pytest
from tests.conftest import create_mock_error
from tests.conftest import create_mock_response

import pycpg
from pycpg.exceptions import PycpgBadRequestError
from pycpg.exceptions import PycpgForbiddenError
from pycpg.exceptions import PycpgLegalHoldCriteriaMissingError
from pycpg.exceptions import PycpgLegalHoldNotFoundOrPermissionDeniedError
from pycpg.exceptions import PycpgUserAlreadyAddedError
from pycpg.services.legalhold import LegalHoldService

LEGAL_HOLD_URI = "/api/v1/LegalHold"

DEFAULT_GET_LEGAL_HOLDS_PARAMS = {
    "active": None,
    "blocked": None,
    "orgUid": None,
    "userUid": None,
    "targetComputerGuid": None,
    "incBackupUsage": None,
    "incCounts": True,
    "pgNum": 1,
    "pgSize": 500,
    "q": None,
}

MOCK_GET_ALL_MATTERS_RESPONSE = """{"legalHolds":["foo"]}"""

MOCK_EMPTY_GET_ALL_MATTERS_RESPONSE = """{"legalHolds": []}"""

MOCK_GET_ALL_MATTER_CUSTODIANS_RESPONSE = """{"legalHoldMemberships": ["foo"]}"""

MOCK_EMPTY_GET_ALL_MATTER_CUSTODIANS_RESPONSE = """{"legalHoldMemberships": []}"""

MOCK_GET_ALL_EVENTS_RESPONSE = """{"legalHoldEvents":["foo"]}"""

MOCK_EMPTY_GET_ALL_EVENTS_RESPONSE = """{"legalHoldEvents": []}"""


class TestLegalHoldService:
    @pytest.fixture
    def mock_get_all_matters_response(self, mocker):
        return create_mock_response(mocker, MOCK_GET_ALL_MATTERS_RESPONSE)

    @pytest.fixture
    def mock_get_all_matters_empty_response(self, mocker):
        return create_mock_response(mocker, MOCK_EMPTY_GET_ALL_MATTERS_RESPONSE)

    @pytest.fixture
    def mock_get_all_matter_custodians_response(self, mocker):
        return create_mock_response(mocker, MOCK_GET_ALL_MATTER_CUSTODIANS_RESPONSE)

    @pytest.fixture
    def mock_get_all_matter_custodians_empty_response(self, mocker):
        return create_mock_response(
            mocker, MOCK_EMPTY_GET_ALL_MATTER_CUSTODIANS_RESPONSE
        )

    @pytest.fixture
    def mock_get_all_events_response(self, mocker):
        return create_mock_response(mocker, MOCK_GET_ALL_EVENTS_RESPONSE)

    @pytest.fixture
    def mock_get_all_events_empty_response(self, mocker):
        return create_mock_response(mocker, MOCK_EMPTY_GET_ALL_EVENTS_RESPONSE)

    def test_get_matter_by_uid_calls_get_with_uri_and_params(
        self, mock_connection, successful_response
    ):
        mock_connection.get.return_value = successful_response
        service = LegalHoldService(mock_connection)
        service.get_matter_by_uid("LEGAL_HOLD_UID")
        uri = f"{LEGAL_HOLD_URI}/LEGAL_HOLD_UID"
        mock_connection.get.assert_called_once_with(uri)

    def test_get_matter_by_uid_when_forbidden_raises_legal_hold_permission_denied_error(
        self, mocker, mock_connection, successful_response
    ):
        mock_connection.get.side_effect = create_mock_error(
            PycpgForbiddenError, mocker, ""
        )
        service = LegalHoldService(mock_connection)
        with pytest.raises(PycpgLegalHoldNotFoundOrPermissionDeniedError) as err:
            service.get_matter_by_uid("matter")

        expected = "Matter with UID 'matter' can not be found. Your account may not have permission to view the matter."
        assert expected in str(err.value)
        assert err.value.uid == "matter"

    def test_get_all_matters_calls_get_expected_number_of_times(
        self,
        mock_connection,
        mock_get_all_matters_response,
        mock_get_all_matters_empty_response,
    ):
        pycpg.settings.items_per_page = 1
        service = LegalHoldService(mock_connection)
        mock_connection.get.side_effect = [
            mock_get_all_matters_response,
            mock_get_all_matters_response,
            mock_get_all_matters_empty_response,
        ]
        for _ in service.get_all_matters():
            pass
        pycpg.settings.items_per_page = 500
        assert mock_connection.get.call_count == 3

    def test_get_all_matter_custodians_calls_get_expected_number_of_times(
        self,
        mock_connection,
        mock_get_all_matter_custodians_response,
        mock_get_all_matter_custodians_empty_response,
    ):
        pycpg.settings.items_per_page = 1
        service = LegalHoldService(mock_connection)
        mock_connection.get.side_effect = [
            mock_get_all_matter_custodians_response,
            mock_get_all_matter_custodians_response,
            mock_get_all_matter_custodians_empty_response,
        ]
        for _ in service.get_all_matter_custodians(user="test"):
            pass
        pycpg.settings.items_per_page = 500
        assert mock_connection.get.call_count == 3

    def test_get_all_events_calls_get_expected_number_of_times(
        self,
        mock_connection,
        mock_get_all_events_response,
        mock_get_all_events_empty_response,
    ):
        pycpg.settings.items_per_page = 1
        service = LegalHoldService(mock_connection)
        mock_connection.get.side_effect = [
            mock_get_all_events_response,
            mock_get_all_events_response,
            mock_get_all_events_empty_response,
        ]
        for _ in service.get_all_events():
            pass
        pycpg.settings.items_per_page = 500
        assert mock_connection.get.call_count == 3

    def test_get_matters_page_calls_get_with_expected_url_and_params(
        self, mock_connection
    ):
        service = LegalHoldService(mock_connection)
        service.get_matters_page(10, "creator", True, "name", "ref", 100)
        mock_connection.get.assert_called_once_with(
            "/api/v1/LegalHold",
            params={
                "creatorUserUid": "creator",
                "activeState": "ACTIVE",
                "name": "name",
                "holdExtRef": "ref",
                "pgNum": 10,
                "pgSize": 100,
            },
        )

    def test_get_custodians_page_calls_get_with_expected_url_and_params(
        self, mock_connection
    ):
        service = LegalHoldService(mock_connection)
        service.get_custodians_page(
            20, "membership", "legalhold", "user ID", "username", True, 200
        )
        mock_connection.get.assert_called_once_with(
            "/api/v1/LegalHoldMembership",
            params={
                "legalHoldMembershipUid": "membership",
                "legalHoldUid": "legalhold",
                "userUid": "user ID",
                "user": "username",
                "activeState": "ACTIVE",
                "pgNum": 20,
                "pgSize": 200,
            },
        )

    def test_get_events_page_calls_get_with_expected_url_and_params(
        self, mock_connection
    ):
        service = LegalHoldService(mock_connection)
        service.get_events_page("legalhold", None, None, 20, 200)
        mock_connection.get.assert_called_once_with(
            "/api/v1/LegalHoldEventReport",
            params={
                "legalHoldUid": "legalhold",
                "minEventDate": None,
                "maxEventDate": None,
                "pgNum": 20,
                "pgSize": 200,
            },
        )

    def test_get_custodians_page_raises_error_when_required_option_missing(
        self, mocker, mock_connection
    ):
        text = (
            "At least one criteria must be specified; holdMembershipUid, holdUid, "
            "userUid, or userSearch"
        )
        mock_connection.get.side_effect = create_mock_error(
            PycpgBadRequestError, mocker, text
        )
        service = LegalHoldService(mock_connection)
        with pytest.raises(PycpgLegalHoldCriteriaMissingError) as err:
            service.get_custodians_page(1)

        assert (
            str(err.value) == "At least one criteria must be specified: "
            "legal_hold_membership_uid, legal_hold_matter_uid, user_uid, or user."
        )

    def test_add_to_matter_calls_post_with_expected_url_and_params(
        self, mock_connection
    ):
        service = LegalHoldService(mock_connection)
        service.add_to_matter("user", "legal")
        expected_data = {"legalHoldUid": "legal", "userUid": "user"}
        mock_connection.post.assert_called_once_with(
            "/api/v1/LegalHoldMembership", json=expected_data
        )

    def test_add_to_matter_when_post_raises_bad_request_error_indicating_user_already_added_raises_user_already_added(
        self, mocker, mock_connection
    ):
        mock_connection.post.side_effect = create_mock_error(
            PycpgBadRequestError, mocker, "USER_ALREADY_IN_HOLD"
        )
        mock_connection.get.return_value = {"name": "NAME"}
        service = LegalHoldService(mock_connection)
        with pytest.raises(PycpgUserAlreadyAddedError) as err:
            service.add_to_matter("user", "legal")

        expected = (
            "User with ID user is already on the legal hold matter id=legal, name=NAME."
        )
        assert expected in str(err.value)
        assert err.value.user_id == "user"
