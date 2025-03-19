import pytest
from tests.conftest import create_mock_error
from tests.conftest import create_mock_response

import pycpg
from pycpg.exceptions import PycpgBadRequestError
from pycpg.exceptions import PycpgForbiddenError
from pycpg.exceptions import PycpgLegalHoldAlreadyActiveError
from pycpg.exceptions import PycpgLegalHoldAlreadyDeactivatedError
from pycpg.exceptions import PycpgLegalHoldCriteriaMissingError
from pycpg.exceptions import PycpgLegalHoldNotFoundOrPermissionDeniedError
from pycpg.exceptions import PycpgUserAlreadyAddedError
from pycpg.services.legalholdapiclient import LegalHoldApiClientService

BASE_URI = "/api/v27"

TEST_POLICY_UID = "123"
TEST_MATTER_UID = "456"
TEST_MEMBERSHIP_UID = "789"

DEFAULT_GET_LEGAL_HOLDS_PARAMS = {
    "active": None,
    "blocked": None,
    "orgUid": None,
    "userUid": None,
    "targetComputerGuid": None,
    "incBackupUsage": None,
    "incCounts": True,
    "page": 1,
    "pageSize": 500,
    "q": None,
}

MOCK_GET_ALL_MATTERS_RESPONSE = """["foo"]"""

MOCK_EMPTY_GET_ALL_MATTERS_RESPONSE = """[]"""

MOCK_GET_ALL_MATTER_CUSTODIANS_RESPONSE = """["foo"]"""

MOCK_EMPTY_GET_ALL_MATTER_CUSTODIANS_RESPONSE = """[]"""


class TestLegalHoldApiClientService:
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

    def test_create_policy_calls_post_with_expected_url_and_params(
        self, mock_connection
    ):
        service = LegalHoldApiClientService(mock_connection)
        uri = f"{BASE_URI}/legal-hold-policy/create"
        service.create_policy("POLICY_NAME")
        assert mock_connection.post.call_args[0][0] == uri
        data = {
            "name": "POLICY_NAME",
        }
        mock_connection.post.assert_called_once_with(uri, json=data)

    def test_get_policy_by_uid_calls_get_with_expected_url_and_params(
        self, mock_connection
    ):
        service = LegalHoldApiClientService(mock_connection)
        uri = f"{BASE_URI}/legal-hold-policy/view"
        service.get_policy_by_uid(TEST_POLICY_UID)
        assert mock_connection.get.call_args[0][0] == uri
        data = {
            "legalHoldPolicyUid": TEST_POLICY_UID,
        }
        mock_connection.get.assert_called_once_with(uri, params=data)

    def test_get_policy_by_uid_raises_pycpg_error_if_policy_uid_not_found_or_forbidden(
        self, mocker, mock_connection
    ):
        service = LegalHoldApiClientService(mock_connection)
        mock_connection.get.side_effect = create_mock_error(
            PycpgForbiddenError, mocker, ""
        )
        with pytest.raises(PycpgLegalHoldNotFoundOrPermissionDeniedError) as err:
            service.get_policy_by_uid(TEST_POLICY_UID)

        assert (
            err.value.args[0]
            == f"Policy with UID '{TEST_POLICY_UID}' can not be found. Your account may not have permission to view the policy."
        )

    def test_get_policy_list_calls_get_with_expected_url(self, mock_connection):
        service = LegalHoldApiClientService(mock_connection)
        uri = f"{BASE_URI}/legal-hold-policy/list"
        service.get_policy_list()
        assert mock_connection.get.call_args[0][0] == uri
        assert mock_connection.get.call_count == 1

    def test_create_matter_calls_post_with_expected_url_and_params(
        self, mock_connection
    ):
        service = LegalHoldApiClientService(mock_connection)
        uri = f"{BASE_URI}/legal-hold-matter/create"
        service.create_matter("MATTER_NAME", TEST_POLICY_UID)
        assert mock_connection.post.call_args[0][0] == uri
        data = {
            "name": "MATTER_NAME",
            "policyId": TEST_POLICY_UID,
            "description": None,
            "notes": None,
            "externalReference": None,
        }
        mock_connection.post.assert_called_once_with(uri, json=data)

    def test_create_matter_calls_post_with_optional_params(self, mock_connection):
        service = LegalHoldApiClientService(mock_connection)
        uri = f"{BASE_URI}/legal-hold-matter/create"
        service.create_matter(
            "MATTER_NAME",
            TEST_POLICY_UID,
            description="description",
            notes="note",
            hold_ext_ref="ext_ref",
        )
        data = {
            "name": "MATTER_NAME",
            "policyId": TEST_POLICY_UID,
            "description": "description",
            "notes": "note",
            "externalReference": "ext_ref",
        }
        mock_connection.post.assert_called_once_with(uri, json=data)

    def test_get_matter_by_uid_calls_get_with_uri_and_params(
        self, mock_connection, successful_response
    ):
        service = LegalHoldApiClientService(mock_connection)
        uri = f"{BASE_URI}/legal-hold-matter/view"
        service.get_matter_by_uid(TEST_MATTER_UID)
        data = {
            "legalHoldUid": TEST_MATTER_UID,
        }
        mock_connection.get.assert_called_once_with(uri, params=data)

    def test_get_matter_by_uid_when_forbidden_raises_legal_hold_permission_denied_error(
        self, mocker, mock_connection, successful_response
    ):
        mock_connection.get.side_effect = create_mock_error(
            PycpgForbiddenError, mocker, ""
        )
        service = LegalHoldApiClientService(mock_connection)
        with pytest.raises(PycpgLegalHoldNotFoundOrPermissionDeniedError) as err:
            service.get_matter_by_uid(TEST_MATTER_UID)

        expected = f"Matter with UID '{TEST_MATTER_UID}' can not be found. Your account may not have permission to view the matter."
        assert expected in str(err.value)

    def test_get_all_matters_calls_get_expected_number_of_times(
        self,
        mock_connection,
        mock_get_all_matters_response,
        mock_get_all_matters_empty_response,
    ):
        pycpg.settings.items_per_page = 1
        service = LegalHoldApiClientService(mock_connection)
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
        service = LegalHoldApiClientService(mock_connection)
        mock_connection.get.side_effect = [
            mock_get_all_matter_custodians_response,
            mock_get_all_matter_custodians_response,
            mock_get_all_matter_custodians_empty_response,
        ]
        for _ in service.get_all_matter_custodians(user="test"):
            pass
        pycpg.settings.items_per_page = 500
        assert mock_connection.get.call_count == 3

    def test_get_matters_page_calls_get_with_expected_url_and_params(
        self, mock_connection
    ):
        service = LegalHoldApiClientService(mock_connection)
        uri = f"{BASE_URI}/legal-hold-matter/list"
        service.get_matters_page(10, "creator", True, "name", "ref", 100)
        mock_connection.get.assert_called_once_with(
            uri,
            params={
                "creatorPrincipalId": "creator",
                "active": "true",
                "name": "name",
                "externalReference": "ref",
                "page": 10,
                "pageSize": 100,
            },
        )

    def test_get_custodians_page_calls_get_with_expected_url_and_params(
        self, mock_connection
    ):
        service = LegalHoldApiClientService(mock_connection)
        uri = f"{BASE_URI}/legal-hold-membership/list"
        service.get_custodians_page(20, "legalhold", "user ID", "username", True, 200)
        mock_connection.get.assert_called_once_with(
            uri,
            params={
                "legalHoldUid": "legalhold",
                "userUid": "user ID",
                "user": "username",
                "active": "ACTIVE",
                "page": 20,
                "pageSize": 200,
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
        service = LegalHoldApiClientService(mock_connection)
        with pytest.raises(PycpgLegalHoldCriteriaMissingError) as err:
            service.get_custodians_page(1)

        assert (
            str(err.value) == "At least one criteria must be specified: "
            "legal_hold_membership_uid, legal_hold_matter_uid, user_uid, or user."
        )

    def test_add_to_matter_calls_post_with_expected_url_and_params(
        self, mock_connection
    ):
        service = LegalHoldApiClientService(mock_connection)
        uri = f"{BASE_URI}/legal-hold-membership/create"
        service.add_to_matter("user", "legal")
        data = {"legalHoldUid": "legal", "userUid": "user"}
        mock_connection.post.assert_called_once_with(uri, json=data)

    def test_add_to_matter_when_post_raises_bad_request_error_indicating_user_already_added_raises_user_already_added(
        self, mocker, mock_connection
    ):
        mock_connection.post.side_effect = create_mock_error(
            PycpgBadRequestError, mocker, "USER_ALREADY_IN_HOLD"
        )
        mock_connection.get.return_value = {"name": "NAME"}
        service = LegalHoldApiClientService(mock_connection)
        with pytest.raises(PycpgUserAlreadyAddedError) as err:
            service.add_to_matter("user", "legal")

        expected = (
            "User with ID user is already on the legal hold matter id=legal, name=NAME."
        )
        assert expected in str(err.value)

    def test_add_to_matter_raises_pycpg_error_if_membership_uid_not_found_or_forbidden(
        self, mocker, mock_connection
    ):
        service = LegalHoldApiClientService(mock_connection)
        mock_connection.post.side_effect = create_mock_error(
            PycpgForbiddenError, mocker, ""
        )
        with pytest.raises(PycpgLegalHoldNotFoundOrPermissionDeniedError) as err:
            service.add_to_matter("user_uid", TEST_MATTER_UID)

        assert (
            err.value.args[0]
            == f"Matter with UID '{TEST_MATTER_UID}' can not be found. Your account may not have permission to view the matter."
        )

    def test_remove_from_matter_calls_post_with_expected_url_and_params(
        self, mock_connection
    ):
        service = LegalHoldApiClientService(mock_connection)
        uri = f"{BASE_URI}/legal-hold-membership/deactivate"
        service.remove_from_matter(TEST_MEMBERSHIP_UID)
        assert mock_connection.post.call_args[0][0] == uri
        data = {
            "legalHoldMembershipUid": TEST_MEMBERSHIP_UID,
        }
        mock_connection.post.assert_called_once_with(uri, json=data)

    def test_remove_from_matter_raises_pycpg_error_if_membership_uid_not_found_or_forbidden(
        self, mocker, mock_connection
    ):
        service = LegalHoldApiClientService(mock_connection)
        mock_connection.post.side_effect = create_mock_error(
            PycpgForbiddenError, mocker, ""
        )
        with pytest.raises(PycpgLegalHoldNotFoundOrPermissionDeniedError) as err:
            service.remove_from_matter(TEST_MEMBERSHIP_UID)

        assert (
            err.value.args[0]
            == f"Membership with UID '{TEST_MEMBERSHIP_UID}' can not be found. Your account may not have permission to view the membership."
        )

    def test_deactivate_matter_calls_post_with_expected_url_and_params(
        self, mock_connection
    ):
        service = LegalHoldApiClientService(mock_connection)
        uri = f"{BASE_URI}/legal-hold-matter/deactivate"
        service.deactivate_matter(TEST_MATTER_UID)
        assert mock_connection.post.call_args[0][0] == uri
        data = {
            "legalHoldUid": TEST_MATTER_UID,
        }
        mock_connection.post.assert_called_once_with(uri, json=data)

    def test_deactivate_matter_raises_pycpg_error_if_matter_already_deactivated(
        self, mocker, mock_connection
    ):
        service = LegalHoldApiClientService(mock_connection)
        mock_connection.post.side_effect = create_mock_error(
            PycpgBadRequestError, mocker, '"problem":"ALREADY_DEACTIVATED'
        )
        with pytest.raises(PycpgLegalHoldAlreadyDeactivatedError) as err:
            service.deactivate_matter(TEST_MATTER_UID)

        assert (
            err.value.args[0]
            == f"Legal Hold Matter with UID '{TEST_MATTER_UID}' has already been deactivated."
        )

    def test_deactivate_matter_raises_pycpg_error_if_matter_uid_not_found_or_forbidden(
        self, mocker, mock_connection
    ):
        service = LegalHoldApiClientService(mock_connection)
        mock_connection.post.side_effect = create_mock_error(
            PycpgForbiddenError, mocker, ""
        )
        with pytest.raises(PycpgLegalHoldNotFoundOrPermissionDeniedError) as err:
            service.deactivate_matter(TEST_MATTER_UID)

        assert (
            err.value.args[0]
            == f"Matter with UID '{TEST_MATTER_UID}' can not be found. Your account may not have permission to view the matter."
        )

    def test_reactivate_matter_calls_post_with_expected_url_and_params(
        self, mock_connection
    ):
        service = LegalHoldApiClientService(mock_connection)
        uri = f"{BASE_URI}/legal-hold-matter/activate"
        service.reactivate_matter(TEST_MATTER_UID)
        assert mock_connection.post.call_args[0][0] == uri
        data = {
            "legalHoldUid": TEST_MATTER_UID,
        }
        mock_connection.post.assert_called_once_with(uri, json=data)

    def test_reactivate_matter_raises_pycpg_error_if_matter_already_active(
        self, mocker, mock_connection
    ):
        service = LegalHoldApiClientService(mock_connection)
        mock_connection.post.side_effect = create_mock_error(
            PycpgBadRequestError, mocker, '"problem":"ALREADY_ACTIVE'
        )
        with pytest.raises(PycpgLegalHoldAlreadyActiveError) as err:
            service.reactivate_matter(TEST_MATTER_UID)

        assert (
            err.value.args[0]
            == f"Legal Hold Matter with UID '{TEST_MATTER_UID}' is already active."
        )

    def test_reactivate_matter_raises_pycpg_error_if_matter_uid_not_found_or_forbidden(
        self, mocker, mock_connection
    ):
        service = LegalHoldApiClientService(mock_connection)
        mock_connection.post.side_effect = create_mock_error(
            PycpgForbiddenError, mocker, ""
        )
        with pytest.raises(PycpgLegalHoldNotFoundOrPermissionDeniedError) as err:
            service.reactivate_matter(TEST_MATTER_UID)

        assert (
            err.value.args[0]
            == f"Matter with UID '{TEST_MATTER_UID}' can not be found. Your account may not have permission to view the matter."
        )
