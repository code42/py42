# -*- coding: utf-8 -*-

import pytest
import json
from requests import Response

from ..conftest import TENANT_ID_FROM_RESPONSE

import py42
from py42._internal.clients.employee_case_management.departing_employee import (
    DepartingEmployeeClient,
)

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
    def mock_get_case_details_function(self, mocker):
        # Useful for testing get_case_by_username, which first gets all cases.
        # Also useful in update_case, which checks current values of case
        mock = mocker.patch(
            "py42._internal.clients.employee_case_management.departing_employee.DepartingEmployeeClient.get_case_by_id"
        )
        response = mocker.MagicMock(spec=Response)
        response.text = _GET_CASE_DETAILS_RESPONSE
        response.status_code = 200
        mock.return_value = response
        return mock

    @pytest.fixture
    def mock_get_all_cases_response(self, mocker):
        response = mocker.MagicMock(spec=Response)
        response.text = _GET_ALL_CASES_RESPONSE
        response.status_code = 200
        return response

    @pytest.fixture
    def mock_get_all_cases_response_empty(self, mocker):
        response = mocker.MagicMock(spec=Response)
        response.text = _GET_ALL_CASES_EMPTY_RESPONSE
        response.status_code = 200
        return response

    def test_create_departing_employee_uses_given_tenant_id_over_current_id(
        self, mock_session, user_context
    ):
        client = DepartingEmployeeClient(mock_session, user_context)
        client.create_departing_employee("test.employee@example.com", _TENANT_ID_PARAM)
        post_call_args = json.loads(mock_session.post.call_args[1]["data"])
        assert post_call_args["tenantId"] == _TENANT_ID_PARAM

    def test_create_departing_employee_posts_expected_data(self, mock_session, user_context):
        client = DepartingEmployeeClient(mock_session, user_context)
        client.create_departing_employee(
            "test.employee@example.com",
            None,
            "These are notes",
            2352463246,
            True,
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
            and posted_data["alertsEnabled"] == True
            and posted_data["cloudUsernames"] == ["test.employee@microsoft.com"]
        )

    def test_create_departing_employee_posts_to_expected_url(self, mock_session, user_context):
        client = DepartingEmployeeClient(mock_session, user_context)
        client.create_departing_employee("test.employee@example.com")
        assert mock_session.post.call_args[0][0] == "/svc/api/v1/departingemployee/create"

    def test_resolve_departing_employee_uses_given_tenant_id_over_current_id(
        self, mock_session, user_context
    ):
        client = DepartingEmployeeClient(mock_session, user_context)
        client.resolve_departing_employee("999", _TENANT_ID_PARAM)
        post_call_args = json.loads(mock_session.post.call_args[1]["data"])
        assert post_call_args["tenantId"] == _TENANT_ID_PARAM

    def test_resolve_departing_employee_posts_expected_data(self, mock_session, user_context):
        client = DepartingEmployeeClient(mock_session, user_context)
        client.resolve_departing_employee("999")

        # Have to convert the request data to a dict because
        # older versions of Python don't have deterministic order.
        posted_data = json.loads(mock_session.post.call_args[1]["data"])
        assert posted_data["caseId"] == "999" and posted_data["tenantId"] == TENANT_ID_FROM_RESPONSE

    def test_resolve_departing_employee_posts_to_expected_url(self, mock_session, user_context):
        client = DepartingEmployeeClient(mock_session, user_context)
        client.resolve_departing_employee("test.employee@example.com")
        assert mock_session.post.call_args[0][0] == "/svc/api/v1/departingemployee/resolve"

    def test_get_all_departing_employees_uses_given_tenant_id_over_current_id(
        self, mock_session, user_context, mock_get_all_cases_response
    ):
        client = DepartingEmployeeClient(mock_session, user_context)
        for page in client.get_all_departing_employees(_TENANT_ID_PARAM):
            break
        first_call = mock_session.post.call_args_list[0]
        post_call_args = json.loads(first_call[1]["data"])
        assert post_call_args["tenantId"] == _TENANT_ID_PARAM

    def test_get_all_departing_employees_posts_expected_data(
        self, mock_session, user_context, mock_get_all_cases_response
    ):
        client = DepartingEmployeeClient(mock_session, user_context)
        for page in client.get_all_departing_employees(None, 235234626, "USERNAME", "ASC"):
            break

        # Have to convert the request data to a dict because
        # older versions of Python don't have deterministic order.
        first_call = mock_session.post.call_args_list[0]
        posted_data = json.loads(first_call[1]["data"])
        assert (
            posted_data["tenantId"] == TENANT_ID_FROM_RESPONSE
            and posted_data["pgSize"] == 1000
            and posted_data["pgNum"] == 1
            and posted_data["departingOnOrAfter"] == "1977-06-15T14:57:06.000Z"
            and posted_data["srtKey"] == "USERNAME"
            and posted_data["srtDirection"] == "ASC"
        )

    def test_get_all_departing_employees_posts_to_expected_url(
        self, mock_session, user_context, mock_get_all_cases_response
    ):
        client = DepartingEmployeeClient(mock_session, user_context)
        for page in client.get_all_departing_employees():
            break
        assert mock_session.post.call_args[0][0] == "/svc/api/v1/departingemployee/search"

    def test_get_all_departing_employees_calls_post_expected_number_of_times(
        self,
        mock_session,
        user_context,
        mock_get_all_cases_response,
        mock_get_all_cases_response_empty,
    ):
        py42.settings.items_per_page = 1
        mock_session.post.side_effect = [
            mock_get_all_cases_response,
            mock_get_all_cases_response,
            mock_get_all_cases_response_empty,
        ]
        client = DepartingEmployeeClient(mock_session, user_context)
        for page in client.get_all_departing_employees():
            pass
        py42.settings.items_per_page = 1000
        assert mock_session.post.call_count == 3

    def test_toggle_alerts_uses_given_tenant_id_over_current_id(self, mock_session, user_context):
        client = DepartingEmployeeClient(mock_session, user_context)
        client.toggle_alerts(_TENANT_ID_PARAM)
        post_call_args = json.loads(mock_session.post.call_args[1]["data"])
        assert post_call_args["tenantId"] == _TENANT_ID_PARAM

    def test_toggle_alerts_posts_expected_data(self, mock_session, user_context):
        client = DepartingEmployeeClient(mock_session, user_context)
        client.toggle_alerts()

        # Have to convert the request data to a dict because
        # older versions of Python don't have deterministic order.
        posted_data = json.loads(mock_session.post.call_args[1]["data"])
        assert (
            posted_data["tenantId"] == TENANT_ID_FROM_RESPONSE
            and posted_data["alertsEnabled"] == True
        )

    def test_toggle_alerts_posts_to_expected_url(self, mock_session, user_context):
        client = DepartingEmployeeClient(mock_session, user_context)
        client.toggle_alerts()
        assert mock_session.post.call_args[0][0] == "/svc/api/v1/departingemployee/togglealerts"

    def test_get_case_by_username_uses_given_tenant_id_over_current_id(
        self, mock_session, user_context, mock_get_all_cases_response
    ):
        mock_session.post.return_value = mock_get_all_cases_response
        client = DepartingEmployeeClient(mock_session, user_context)
        client.get_case_by_username("test.example@example.com", _TENANT_ID_PARAM)
        first_call = mock_session.post.call_args_list[0]
        post_call_args = json.loads(first_call[1]["data"])
        assert post_call_args["tenantId"] == _TENANT_ID_PARAM

    def test_get_case_by_username_posts_expected_data(
        self, mock_session, user_context, mock_get_all_cases_response
    ):
        mock_session.post.return_value = mock_get_all_cases_response
        client = DepartingEmployeeClient(mock_session, user_context)
        client.get_case_by_username("test.example@example.com")

        # Have to convert the request data to a dict because
        # older versions of Python don't have deterministic order.
        posted_data = json.loads(mock_session.post.call_args[1]["data"])
        assert posted_data["tenantId"] == TENANT_ID_FROM_RESPONSE and posted_data["caseId"] == "20"

    def test_get_case_by_username_posts_to_expected_url(
        self, mock_session, user_context, mock_get_all_cases_response
    ):
        mock_session.post.return_value = mock_get_all_cases_response
        client = DepartingEmployeeClient(mock_session, user_context)
        client.get_case_by_username("test.example@example.com")
        assert mock_session.post.call_args[0][0] == "/svc/api/v1/departingemployee/details"

    def test_get_case_by_id_uses_given_tenant_id_over_current_id(
        self, mock_session, user_context, mock_get_all_cases_response
    ):
        mock_session.post.return_value = mock_get_all_cases_response
        client = DepartingEmployeeClient(mock_session, user_context)
        client.get_case_by_id("999", _TENANT_ID_PARAM)
        post_call_args = json.loads(mock_session.post.call_args[1]["data"])
        assert post_call_args["tenantId"] == _TENANT_ID_PARAM

    def test_get_case_by_id_posts_expected_data(self, mock_session, user_context):
        client = DepartingEmployeeClient(mock_session, user_context)
        client.get_case_by_id("999")

        # Have to convert the request data to a dict because
        # older versions of Python don't have deterministic order.
        posted_data = json.loads(mock_session.post.call_args[1]["data"])
        assert posted_data["tenantId"] == TENANT_ID_FROM_RESPONSE and posted_data["caseId"] == "999"

    def test_get_case_by_id_posts_to_expected_url(self, mock_session, user_context):
        client = DepartingEmployeeClient(mock_session, user_context)
        client.get_case_by_id("999")
        assert mock_session.post.call_args[0][0] == "/svc/api/v1/departingemployee/details"

    def test_update_case_uses_given_tenant_id_over_current_id(
        self, mock_session, user_context, mock_get_case_details_function
    ):
        client = DepartingEmployeeClient(mock_session, user_context)
        client.update_case("697", _TENANT_ID_PARAM)
        post_call_args = json.loads(mock_session.post.call_args[1]["data"])
        assert post_call_args["tenantId"] == _TENANT_ID_PARAM

    def test_update_case_posts_expected_data(
        self, mock_session, user_context, mock_get_case_details_function
    ):
        client = DepartingEmployeeClient(mock_session, user_context)
        client.update_case(
            "697",
            None,
            "Display Name",
            "These are notes",
            24642747257,
            False,
            "EXFILTRATION_24_HOURS",
            ["test@test.com"],
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
            and posted_data["alertsEnabled"] == False
            and posted_data["status"] == "EXFILTRATION_24_HOURS"
            and posted_data["cloudUsernames"] == ["test@test.com"]
        )

    def test_update_case_uses_current_data_when_not_provided(
        self, mock_session, user_context, mock_get_case_details_function
    ):
        client = DepartingEmployeeClient(mock_session, user_context)
        client.update_case("20")

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

    def test_update_case_posts_to_expected_url(
        self, mock_session, user_context, mock_get_case_details_function
    ):
        client = DepartingEmployeeClient(mock_session, user_context)
        client.update_case("697")
        assert mock_session.post.call_args[0][0] == "/svc/api/v1/departingemployee/update"
