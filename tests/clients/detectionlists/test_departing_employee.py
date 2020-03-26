# -*- coding: utf-8 -*-

import json

import pytest

from py42.clients.detectionlists.departing_employee import DepartingEmployeeClient
from py42.sdk.response import Py42Response

from tests.conftest import TENANT_ID_FROM_RESPONSE

_TENANT_ID_PARAM = "22222222-2222-2222-2222-222222222222"


_GET_CASE_DETAILS_RESPONSE = """
{{
    "type$":"DEPARTING_EMPLOYEE_CASE",
    "tenantId":"{0}",
    "caseId":"697",
    "userUid":"921286907298179098",
    "userName":"test.example@example.com",
    "displayName":"Test Testerson",
    "notes":"notes notes notes",
    "createdAt":"2020-02-14T20:11:29.5563480Z",
    "status":"OPEN",
    "cloudUsernames":["test.testerson+partners@code42.com","test.s@c42fc.com"],
    "departureDate":"2020-02-13",
    "alertsEnabled":true
}}
""".format(
    TENANT_ID_FROM_RESPONSE
)


_GET_ALL_CASES_RESPONSE = """
{{
    "type$":"DEPARTING_EMPLOYEE_SEARCH_RESPONSE",
    "cases":
        [
            {{
                "type$":"DEPARTING_EMPLOYEE_CASE",
                "tenantId":"{0}",
                "caseId":"697",
                "userUid":"999999999999999999","userName":
                "test.testerson@example.com",
                "displayName":"Test Testerson",
                "notes":"These are notes",
                "createdAt":"2020-02-11T20:43:58.3611040Z",
                "status":"OPEN",
                "alertsEnabled":true
            }},
            {{
                "type$":"DEPARTING_EMPLOYEE_CASE",
                "tenantId":"{1}",
                "caseId":"20",
                "userUid":"888888888888888888",
                "userName":"test.example@example.com",
                "displayName":"Test Example",
                "notes":"",
                "createdAt":"2019-10-25T13:31:14.1199010Z",
                "status":"OPEN",
                "cloudUsernames":["test.example@example.com"],
                "alertsEnabled":true
            }}
        ],
    "totalCount":2
}}
""".format(
    TENANT_ID_FROM_RESPONSE, TENANT_ID_FROM_RESPONSE
)

_GET_ALL_CASES_EMPTY_RESPONSE = """
{"type$":"DEPARTING_EMPLOYEE_SEARCH_RESPONSE","cases":[],"totalCount":0}
"""


class TestDepartingEmployeeClient(object):
    @pytest.fixture
    def mock_get_case_details_function(self, mocker, py42_response):
        # Useful for testing get_by_username, which first gets all cases.
        # Also useful in update, which checks current values of case
        mock = mocker.patch(
            "py42.clients.detectionlists.departing_employee.DepartingEmployeeClient.get_by_id"
        )
        py42_response.text = _GET_CASE_DETAILS_RESPONSE
        return py42_response

    @pytest.fixture
    def mock_get_all_cases_response(self, mocker, py42_response):
        py42_response.text = _GET_ALL_CASES_RESPONSE

        return py42_response

    @pytest.fixture
    def mock_get_all_cases_response_empty(self, mocker, py42_response):
        py42_response.text = _GET_ALL_CASES_EMPTY_RESPONSE

        return py42_response

    @pytest.fixture
    def mock_py42_response(self, mocker, mock_get_case_details_function, py42_response):
        py42_response.test = mock_get_case_details_function.text

        return py42_response

    def test_create_uses_given_tenant_id_over_current_id(
        self, mock_session, user_context, mock_get_all_cases_response
    ):
        client = DepartingEmployeeClient(mock_session, user_context)
        mock_session.post.return_value = mock_get_all_cases_response
        client.create("test.employee@example.com", _TENANT_ID_PARAM)
        post_call_args = json.loads(mock_session.post.call_args[1]["data"])
        assert post_call_args["tenantId"] == _TENANT_ID_PARAM

    def test_create_posts_expected_data(
        self, mock_session, user_context, mock_get_all_cases_response
    ):
        client = DepartingEmployeeClient(mock_session, user_context)
        # Return value should have been set based on the arguments passed
        # in create, here however as we are mocking it, it doesn't matter. Can be refactored
        mock_session.post.return_value = mock_get_all_cases_response
        client.create(
            "test.employee@example.com",
            None,
            "These are notes",
            2352463246,
            ["test.employee@microsoft.com"],
        )

        # Have to convert the request data to a dict because
        # older versions of Python don't have deterministic order.
        posted_data = json.loads(mock_session.post.call_args[1]["data"])
        assert (
            posted_data["userName"] == "test.employee@example.com"
            and posted_data["tenantId"] == TENANT_ID_FROM_RESPONSE
            and posted_data["notes"] == "These are notes"
            and posted_data["departureDate"] == "2044-07-18T14:00:46.000Z"
            and posted_data["cloudUsernames"] == ["test.employee@microsoft.com"]
        )

    def test_create_posts_to_expected_url(
        self, mock_session, user_context, mock_get_all_cases_response_empty
    ):
        client = DepartingEmployeeClient(mock_session, user_context)
        mock_session.post.return_value = mock_get_all_cases_response_empty
        client.create("test.employee@example.com")
        assert mock_session.post.call_args[0][0] == "/svc/api/v1/departingemployee/create"

    def test_resolve_uses_given_tenant_id_over_current_id(
        self, mock_session, user_context, mock_get_all_cases_response_empty
    ):
        client = DepartingEmployeeClient(mock_session, user_context)
        mock_session.post.return_value = mock_get_all_cases_response_empty
        client.resolve("999", _TENANT_ID_PARAM)
        post_call_args = json.loads(mock_session.post.call_args[1]["data"])
        assert post_call_args["tenantId"] == _TENANT_ID_PARAM

    def test_resolve_posts_expected_data(
        self, mock_session, user_context, mock_get_all_cases_response_empty
    ):
        client = DepartingEmployeeClient(mock_session, user_context)
        mock_session.post.return_value = mock_get_all_cases_response_empty
        client.resolve("999")

        # Have to convert the request data to a dict because
        # older versions of Python don't have deterministic order.
        posted_data = json.loads(mock_session.post.call_args[1]["data"])
        assert posted_data["caseId"] == "999" and posted_data["tenantId"] == TENANT_ID_FROM_RESPONSE

    def test_resolve_posts_to_expected_url(
        self, mock_session, user_context, mock_get_all_cases_response_empty
    ):
        client = DepartingEmployeeClient(mock_session, user_context)
        mock_session.post.return_value = mock_get_all_cases_response_empty
        client.resolve("test.employee@example.com")
        assert mock_session.post.call_args[0][0] == "/svc/api/v1/departingemployee/resolve"

    def test_get_all_uses_given_tenant_id_over_current_id(
        self, mock_session, user_context, mock_get_all_cases_response
    ):
        client = DepartingEmployeeClient(mock_session, user_context)
        mock_session.post.return_value = mock_get_all_cases_response
        for _ in client.get_all(_TENANT_ID_PARAM):
            break
        first_call = mock_session.post.call_args_list[0]
        post_call_args = json.loads(first_call[1]["data"])
        assert post_call_args["tenantId"] == _TENANT_ID_PARAM

    def test_get_all_posts_expected_data(
        self, mock_session, user_context, mock_get_all_cases_response
    ):
        client = DepartingEmployeeClient(mock_session, user_context)
        mock_session.post.return_value = mock_get_all_cases_response
        for _ in client.get_all(None, 235234626, "USERNAME", "ASC"):
            break

        # Have to convert the request data to a dict because
        # older versions of Python don't have deterministic order.
        first_call = mock_session.post.call_args_list[0]
        posted_data = json.loads(first_call[1]["data"])
        assert (
            posted_data["tenantId"] == TENANT_ID_FROM_RESPONSE
            and posted_data["pgSize"] == 100
            and posted_data["pgNum"] == 1
            and posted_data["departingOnOrAfter"] == "1977-06-15T14:57:06.000Z"
            and posted_data["srtKey"] == "USERNAME"
            and posted_data["srtDirection"] == "ASC"
        )

    def test_get_all_posts_to_expected_url(
        self, mock_session, user_context, mock_get_all_cases_response
    ):
        client = DepartingEmployeeClient(mock_session, user_context)
        mock_session.post.return_value = mock_get_all_cases_response
        for _ in client.get_all():
            break
        assert mock_session.post.call_args[0][0] == "/svc/api/v1/departingemployee/search"

    def test_get_all_calls_post_expected_number_of_times(
        self,
        mock_session,
        user_context,
        mock_get_all_cases_response,
        mock_get_all_cases_response_empty,
    ):
        mock_session.post.side_effect = [
            mock_get_all_cases_response,
            mock_get_all_cases_response,
            mock_get_all_cases_response_empty,
        ]
        client = DepartingEmployeeClient(mock_session, user_context)
        mock_session.get.return_value = mock_get_all_cases_response_empty
        for _ in client.get_all():
            pass
        assert mock_session.post.call_count == 1

    def test_toggle_alerts_uses_given_tenant_id_over_current_id(
        self, mock_session, user_context, mock_get_all_cases_response_empty
    ):
        client = DepartingEmployeeClient(mock_session, user_context)
        mock_session.post.return_value = mock_get_all_cases_response_empty
        client.toggle_alerts(_TENANT_ID_PARAM)
        post_call_args = json.loads(mock_session.post.call_args[1]["data"])
        assert post_call_args["tenantId"] == _TENANT_ID_PARAM

    def test_toggle_alerts_posts_expected_data(
        self, mock_session, user_context, mock_get_all_cases_response_empty
    ):
        client = DepartingEmployeeClient(mock_session, user_context)
        mock_session.post.return_value = mock_get_all_cases_response_empty
        client.toggle_alerts()

        # Have to convert the request data to a dict because
        # older versions of Python don't have deterministic order.
        posted_data = json.loads(mock_session.post.call_args[1]["data"])
        assert (
            posted_data["tenantId"] == TENANT_ID_FROM_RESPONSE
            and posted_data["alertsEnabled"] == True
        )

    def test_toggle_alerts_posts_to_expected_url(
        self, mock_session, user_context, mock_get_all_cases_response_empty
    ):
        client = DepartingEmployeeClient(mock_session, user_context)
        mock_session.post.return_value = mock_get_all_cases_response_empty
        client.toggle_alerts()
        assert mock_session.post.call_args[0][0] == "/svc/api/v1/departingemployee/togglealerts"

    def test_get_by_username_uses_given_tenant_id_over_current_id(
        self, mock_session, user_context, mock_get_all_cases_response
    ):
        mock_session.post.return_value = mock_get_all_cases_response
        client = DepartingEmployeeClient(mock_session, user_context)
        mock_session.get.return_value = mock_get_all_cases_response
        client.get_by_username("test.example@example.com", _TENANT_ID_PARAM)
        first_call = mock_session.post.call_args_list[0]
        post_call_args = json.loads(first_call[1]["data"])
        assert post_call_args["tenantId"] == _TENANT_ID_PARAM

    def test_get_by_username_posts_expected_data(
        self, mock_session, user_context, mock_get_all_cases_response
    ):
        mock_session.post.return_value = mock_get_all_cases_response
        client = DepartingEmployeeClient(mock_session, user_context)
        client.get_by_username("test.example@example.com")

        # Have to convert the request data to a dict because
        # older versions of Python don't have deterministic order.
        posted_data = json.loads(mock_session.post.call_args[1]["data"])
        assert posted_data["tenantId"] == TENANT_ID_FROM_RESPONSE and posted_data["caseId"] == "20"

    def test_get_by_username_posts_to_expected_url(
        self, mock_session, user_context, mock_get_all_cases_response
    ):
        mock_session.post.return_value = mock_get_all_cases_response
        client = DepartingEmployeeClient(mock_session, user_context)
        client.get_by_username("test.example@example.com")
        assert mock_session.post.call_args[0][0] == "/svc/api/v1/departingemployee/details"

    def test_get_by_id_uses_given_tenant_id_over_current_id(
        self, mock_session, user_context, mock_get_all_cases_response
    ):
        mock_session.post.return_value = mock_get_all_cases_response
        client = DepartingEmployeeClient(mock_session, user_context)
        client.get_by_id("999", _TENANT_ID_PARAM)
        post_call_args = json.loads(mock_session.post.call_args[1]["data"])
        assert post_call_args["tenantId"] == _TENANT_ID_PARAM

    def test_get_by_id_posts_expected_data(
        self, mock_session, user_context, mock_get_all_cases_response_empty
    ):
        client = DepartingEmployeeClient(mock_session, user_context)
        mock_session.post.return_value = mock_get_all_cases_response_empty
        client.get_by_id("999")

        # Have to convert the request data to a dict because
        # older versions of Python don't have deterministic order.
        posted_data = json.loads(mock_session.post.call_args[1]["data"])
        assert posted_data["tenantId"] == TENANT_ID_FROM_RESPONSE and posted_data["caseId"] == "999"

    def test_get_by_id_posts_to_expected_url(
        self, mock_session, user_context, mock_get_all_cases_response_empty
    ):
        client = DepartingEmployeeClient(mock_session, user_context)
        mock_session.post.return_value = mock_get_all_cases_response_empty
        client.get_by_id("999")
        assert mock_session.post.call_args[0][0] == "/svc/api/v1/departingemployee/details"

    def test_update_uses_given_tenant_id_over_current_id(
        self, mock_session, user_context, mock_get_case_details_function, mock_py42_response
    ):
        client = DepartingEmployeeClient(mock_session, user_context)
        client.get_by_id.return_value = mock_py42_response
        mock_session.post.return_value = mock_get_case_details_function
        client.update("697", _TENANT_ID_PARAM)
        post_call_args = json.loads(mock_session.post.call_args[1]["data"])
        assert post_call_args["tenantId"] == _TENANT_ID_PARAM

    def test_update_posts_expected_data(
        self, mock_session, user_context, mock_get_case_details_function, mock_py42_response
    ):
        client = DepartingEmployeeClient(mock_session, user_context)
        client.get_by_id.return_value = mock_py42_response
        mock_session.post.return_value = mock_get_case_details_function
        client.update(
            "697", None, "Display Name", "These are notes", 24642747257, ["test@test.com"]
        )

        # Have to convert the request data to a dict because
        # older versions of Python don't have deterministic order.
        posted_data = json.loads(mock_session.post.call_args[1]["data"])
        assert (
            posted_data["tenantId"] == TENANT_ID_FROM_RESPONSE
            and posted_data["caseId"] == "697"
            and posted_data["displayName"] == "Display Name"
            and posted_data["notes"] == "These are notes"
            and posted_data["departureDate"] == "2750-11-24T23:34:17.000Z"
            and posted_data["alertsEnabled"] == True
            and posted_data["status"] == "OPEN"
            and posted_data["cloudUsernames"] == ["test@test.com"]
        )

    def test_update_uses_current_data_when_not_provided(
        self, mock_session, user_context, mock_get_case_details_function, mock_py42_response
    ):
        client = DepartingEmployeeClient(mock_session, user_context)
        client.get_by_id.return_value = mock_py42_response
        mock_session.post.return_value = mock_get_case_details_function
        client.update("20")

        # Have to convert the request data to a dict because
        # older versions of Python don't have deterministic order.
        posted_data = json.loads(mock_session.post.call_args[1]["data"])
        assert (
            posted_data["tenantId"] == TENANT_ID_FROM_RESPONSE
            and posted_data["caseId"] == "20"
            and posted_data["displayName"] == "Test Testerson"
            and posted_data["notes"] == "notes notes notes"
            and posted_data["departureDate"] == "2020-02-13"
            and posted_data["alertsEnabled"] == True
            and posted_data["status"] == "OPEN"
            and posted_data["cloudUsernames"]
            == ["test.testerson+partners@code42.com", "test.s@c42fc.com"]
        )

    def test_update_posts_to_expected_url(
        self, mock_session, user_context, mock_get_case_details_function, mock_py42_response
    ):
        client = DepartingEmployeeClient(mock_session, user_context)
        client.get_by_id.return_value = mock_py42_response
        mock_session.post.return_value = mock_get_case_details_function
        client.update("697")
        assert mock_session.post.call_args[0][0] == "/svc/api/v1/departingemployee/update"
