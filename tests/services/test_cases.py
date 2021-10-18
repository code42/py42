import pytest
from tests.conftest import create_mock_error
from tests.conftest import create_mock_response

import py42.settings
from py42.exceptions import Py42BadRequestError
from py42.exceptions import Py42CaseNameExistsError
from py42.exceptions import Py42DescriptionLimitExceededError
from py42.exceptions import Py42InvalidCaseUserError
from py42.exceptions import Py42UpdateClosedCaseError
from py42.services.cases import CasesService

GET_ALL_TEST_RESPONSE = '{"cases":["test"], "totalCount":1}'
EMPTY_GET_ALL_TEST_RESPONSE = '{"cases": [], "totalCount":0}'
UPDATE_ERROR_RESPONSE = """{
    "timestamp": "2021-01-06T16:54:44.668+00:00",
    "status": 400,
    "error": "Bad Request",
    "message": "NO_EDITS_ONCE_CLOSED",
    "path": "/api/v1/case"
}
"""
GET_CASE_RESPONSE = """
{
    "assignee": "string",
    "assigneeUsername": "string",
    "createdAt": "2021-01-04T08:09:58.832Z",
    "createdByUserUid": "string",
    "createdByUsername": "string",
    "lastModifiedByUserUid": "string",
    "lastModifiedByUsername": "string",
    "name": "string",
    "number": 0,
    "status": "OPEN",
    "subject": "string",
    "subjectUsername": "string",
    "updatedAt": "2021-01-04T08:09:58.832Z"
}
"""
NAME_EXISTS_ERROR_MSG = '{"problem":"NAME_EXISTS","description":null}'
DESCRIPTION_TOO_LONG_ERROR_MSG = '{"problem":"DESCRIPTION_TOO_LONG","description":null}'
UNKNOWN_ERROR_MSG = '{"problem":"SURPRISE!"}'
_TEST_CASE_NUMBER = 123456
_BASE_URI = "/api/v1/cases"


def _get_invalid_user_text(user_type):
    return f'{{"problem":"INVALID_USER","description":"{user_type} validation failed"}}'


class TestCasesService:
    @pytest.fixture
    def mock_case_response(self, mocker):
        return create_mock_response(mocker, GET_ALL_TEST_RESPONSE)

    @pytest.fixture
    def mock_get_response(self, mocker):
        return create_mock_response(mocker, GET_CASE_RESPONSE)

    @pytest.fixture
    def mock_case_empty_response(self, mocker):
        return create_mock_response(mocker, EMPTY_GET_ALL_TEST_RESPONSE)

    def test_create_called_with_expected_url_and_params(self, mock_connection):
        cases_service = CasesService(mock_connection)
        cases_service.create("name", "subject", "user uid", "description", "findings")
        assert mock_connection.post.call_args[0][0] == "/api/v1/cases"
        data = {
            "name": "name",
            "subject": "subject",
            "assignee": "user uid",
            "description": "description",
            "findings": "findings",
        }
        mock_connection.post.assert_called_once_with(_BASE_URI, json=data)

    def test_create_when_fails_with_name_exists_error_raises_custom_exception(
        self, mocker, mock_connection
    ):
        cases_service = CasesService(mock_connection)
        mock_connection.post.side_effect = create_mock_error(
            Py42BadRequestError, mocker, NAME_EXISTS_ERROR_MSG
        )
        with pytest.raises(Py42CaseNameExistsError) as err:
            cases_service.create("Duplicate")

        assert (
            err.value.args[0]
            == "Case name 'Duplicate' already exists, please set another name."
        )

    def test_create_when_fails_with_description_too_long_error_raises_custom_exception(
        self, mocker, mock_connection
    ):
        cases_service = CasesService(mock_connection)
        mock_connection.post.side_effect = create_mock_error(
            Py42BadRequestError, mocker, DESCRIPTION_TOO_LONG_ERROR_MSG
        )
        with pytest.raises(Py42DescriptionLimitExceededError) as err:
            cases_service.create("test", description="supposedly too long")

        assert (
            err.value.args[0]
            == "Description limit exceeded, max 250 characters allowed."
        )

    def test_create_when_fails_with_invalid_subject_raises_custom_exception(
        self, mocker, mock_connection
    ):
        cases_service = CasesService(mock_connection)
        mock_connection.post.side_effect = create_mock_error(
            Py42BadRequestError, mocker, _get_invalid_user_text("subject")
        )
        with pytest.raises(Py42InvalidCaseUserError) as err:
            cases_service.create("test", subject="Not a person")

        assert err.value.args[0] == "The provided subject is not a valid user."

    def test_create_when_fails_with_invalid_assignee_raises_custom_exception(
        self, mocker, mock_connection
    ):
        cases_service = CasesService(mock_connection)
        mock_connection.post.side_effect = create_mock_error(
            Py42BadRequestError, mocker, _get_invalid_user_text("assignee")
        )
        with pytest.raises(Py42InvalidCaseUserError) as err:
            cases_service.create("test", assignee="Not a person")

        assert err.value.args[0] == "The provided assignee is not a valid user."

    def test_create_when_fails_with_unknown_error_raises_exception(
        self, mocker, mock_connection
    ):
        cases_service = CasesService(mock_connection)
        mock_connection.post.side_effect = create_mock_error(
            Py42BadRequestError, mocker, UNKNOWN_ERROR_MSG
        )
        with pytest.raises(Py42BadRequestError):
            cases_service.create("Case")

    def test_get_all_called_expected_number_of_times(
        self, mock_connection, mock_case_response, mock_case_empty_response
    ):
        cases_service = CasesService(mock_connection)
        py42.settings.items_per_page = 1
        items = [mock_case_response, mock_case_empty_response]

        mock_connection.get.side_effect = items
        for _ in cases_service.get_all():
            pass

        assert mock_connection.get.call_count == 2
        py42.settings.items_per_page = 500

    def test_get_all_called_with_expected_url_and_default_params(
        self, mock_connection, mock_case_response, mock_case_empty_response
    ):
        cases_service = CasesService(mock_connection)
        items = [
            mock_case_response,
        ]

        mock_connection.get.side_effect = items
        for _ in cases_service.get_all():
            pass

        expected_params = {
            "name": None,
            "subject": None,
            "assignee": None,
            "createdAt": None,
            "updatedAt": None,
            "status": None,
            "pgNum": 1,
            "pgSize": 500,
            "srtDir": "asc",
            "srtKey": "number",
        }
        mock_connection.get.assert_called_once_with(_BASE_URI, params=expected_params)

    def test_get_all_called_with_expected_url_and_params(
        self, mock_connection, mock_case_response
    ):
        cases_service = CasesService(mock_connection)
        mock_connection.get.side_effect = [
            mock_case_response,
            mock_case_response,
        ]
        for _ in cases_service.get_all(name="test-case"):
            continue

        expected_params = {
            "name": "test-case",
            "subject": None,
            "assignee": None,
            "createdAt": None,
            "updatedAt": None,
            "status": None,
            "pgNum": 1,
            "pgSize": 500,
            "srtDir": "asc",
            "srtKey": "number",
        }
        mock_connection.get.assert_called_once_with(_BASE_URI, params=expected_params)

    def test_get_all_called_with_expected_url_and_all_optional_params(
        self, mock_connection, mock_case_response
    ):
        cases_service = CasesService(mock_connection)
        mock_connection.get.side_effect = [
            mock_case_response,
            mock_case_response,
        ]
        for _ in cases_service.get_all(
            name="test-case",
            subject="test",
            assignee="user-uid",
            updated_at="2010-04-30T001",
            created_at="2010-01-03T002",
            status="open",
        ):
            continue

        expected_params = {
            "name": "test-case",
            "subject": "test",
            "assignee": "user-uid",
            "createdAt": "2010-01-03T002",
            "updatedAt": "2010-04-30T001",
            "status": "open",
            "pgNum": 1,
            "pgSize": 500,
            "srtDir": "asc",
            "srtKey": "number",
        }
        mock_connection.get.assert_called_once_with(_BASE_URI, params=expected_params)

    def test_export_called_with_expected_url_and_params(self, mock_connection):
        cases_service = CasesService(mock_connection)
        cases_service.export_summary(_TEST_CASE_NUMBER)
        assert (
            mock_connection.get.call_args[0][0]
            == f"/api/v1/cases/{_TEST_CASE_NUMBER}/export"
        )

    def test_get_called_with_expected_url_and_params(self, mock_connection):
        cases_service = CasesService(mock_connection)
        cases_service.get(_TEST_CASE_NUMBER)
        assert (
            mock_connection.get.call_args[0][0] == f"/api/v1/cases/{_TEST_CASE_NUMBER}"
        )

    def test_update_called_with_expected_url_and_params(
        self, mock_connection, mock_get_response
    ):
        cases_service = CasesService(mock_connection)
        mock_connection.get.return_value = mock_get_response
        cases_service.update(_TEST_CASE_NUMBER, findings="x")
        data = {
            "name": "string",
            "subject": "string",
            "assignee": "string",
            "description": None,
            "status": "OPEN",
            "findings": "x",
        }
        mock_connection.put.assert_called_once_with(
            f"/api/v1/cases/{_TEST_CASE_NUMBER}", json=data
        )

    def test_update_when_fails_with_name_exists_error_raises_custom_exception(
        self, mocker, mock_connection
    ):
        cases_service = CasesService(mock_connection)
        mock_connection.put.side_effect = create_mock_error(
            Py42BadRequestError, mocker, NAME_EXISTS_ERROR_MSG
        )
        with pytest.raises(Py42CaseNameExistsError) as err:
            cases_service.update(_TEST_CASE_NUMBER, "Duplicate")

        assert (
            err.value.args[0]
            == "Case name 'Duplicate' already exists, please set another name."
        )

    def test_update_when_case_is_closed_raises_custom_exception(
        self, mocker, mock_connection, mock_get_response
    ):
        cases_service = CasesService(mock_connection)
        mock_connection.get.return_value = mock_get_response
        mock_connection.put.side_effect = create_mock_error(
            Py42BadRequestError, mocker, UPDATE_ERROR_RESPONSE
        )
        with pytest.raises(Py42UpdateClosedCaseError) as err:
            cases_service.update(_TEST_CASE_NUMBER, findings="x")

        assert err.value.args[0] == "Cannot update a closed case."

    def test_update_when_fails_with_description_too_long_error_raises_custom_exception(
        self, mocker, mock_connection, mock_get_response
    ):
        cases_service = CasesService(mock_connection)
        mock_connection.get.return_value = mock_get_response
        mock_connection.put.side_effect = create_mock_error(
            Py42BadRequestError, mocker, DESCRIPTION_TOO_LONG_ERROR_MSG
        )
        with pytest.raises(Py42DescriptionLimitExceededError) as err:
            cases_service.update(_TEST_CASE_NUMBER, description="supposedly too long")

        assert (
            err.value.args[0]
            == "Description limit exceeded, max 250 characters allowed."
        )

    def test_update_when_fails_with_invalid_subject_raises_custom_exception(
        self, mocker, mock_connection
    ):
        cases_service = CasesService(mock_connection)
        mock_connection.put.side_effect = create_mock_error(
            Py42BadRequestError, mocker, _get_invalid_user_text("subject")
        )
        with pytest.raises(Py42InvalidCaseUserError) as err:
            cases_service.update(_TEST_CASE_NUMBER, subject="Not a person")

        assert err.value.args[0] == "The provided subject is not a valid user."

    def test_update_when_fails_with_invalid_assignee_raises_custom_exception(
        self, mocker, mock_connection
    ):
        cases_service = CasesService(mock_connection)
        mock_connection.put.side_effect = create_mock_error(
            Py42BadRequestError, mocker, _get_invalid_user_text("assignee")
        )
        with pytest.raises(Py42InvalidCaseUserError) as err:
            cases_service.update(_TEST_CASE_NUMBER, assignee="Not a person")

        assert err.value.args[0] == "The provided assignee is not a valid user."
