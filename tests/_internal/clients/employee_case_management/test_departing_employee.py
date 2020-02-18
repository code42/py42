# -*- coding: utf-8 -*-

import pytest
import json
from requests import Response

from py42._internal.clients.employee_case_management.departing_employee import (
    DepartingEmployeeClient,
)


GET_CASE_DETAILS_RESPONSE = """
{
    "type$":"DEPARTING_EMPLOYEE_CASE",
    "tenantId":"00000000-0000-0000-0000-000000000000",
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
}
"""


GET_ALL_CASES_RESPONSE = """
{
    "type$":"DEPARTING_EMPLOYEE_SEARCH_RESPONSE",
    "cases":
        [
            {
                "type$":"DEPARTING_EMPLOYEE_CASE",
                "tenantId":"00000000-0000-0000-0000-000000000000",
                "caseId":"697",
                "userUid":"999999999999999999","userName":
                "test.testerson@example.com",
                "displayName":"Test Testerson",
                "notes":"These are notes",
                "createdAt":"2020-02-11T20:43:58.3611040Z",
                "status":"OPEN",
                "alertsEnabled":true
            },
            {
                "type$":"DEPARTING_EMPLOYEE_CASE",
                "tenantId":"00000000-0000-0000-0000-000000000000",
                "caseId":"20",
                "userUid":"888888888888888888",
                "userName":"test.example@example.com",
                "displayName":"Test Example",
                "notes":"",
                "createdAt":"2019-10-25T13:31:14.1199010Z",
                "status":"OPEN",
                "cloudUsernames":["test.example@example.com"],
                "alertsEnabled":true
            }
        ],
    "totalCount":2
}
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
        response.text = GET_CASE_DETAILS_RESPONSE
        response.status_code = 200
        mock.return_value = response
        return mock

    @pytest.fixture
    def mock_get_all_cases_function(self, mocker):
        # Useful for testing get_case_by_username, which first gets all cases.
        # Also useful in update_case, which checks current values of case
        mock = mocker.patch(
            "py42._internal.clients.employee_case_management.departing_employee.DepartingEmployeeClient.get_all_departing_employees"
        )
        response = mocker.MagicMock(spec=Response)
        response.text = GET_ALL_CASES_RESPONSE
        response.status_code = 200
        mock.return_value = response
        return mock

    def test_create_departing_employee_uses_given_tenant_id_over_current_id(
        self, mock_session, customer
    ):
        client = DepartingEmployeeClient(mock_session, customer)
        client.create_departing_employee(
            "test.employee@example.com", "22222222-2222-2222-2222-222222222222"
        )
        post_call_args = json.loads(mock_session.post.call_args[1]["data"])
        assert post_call_args["tenantId"] == "22222222-2222-2222-2222-222222222222"

    def test_create_departing_employee_posts_expected_data(self, mock_session, customer):
        client = DepartingEmployeeClient(mock_session, customer)
        client.create_departing_employee(
            "test.employee@example.com",
            None,
            "These are notes",
            "12-08-2023",
            True,
            ["test.employee@microsoft.com"],
        )

        # Have to convert the request data to a dict because
        # older versions of Python don't have deterministic order.
        posted_data = json.loads(mock_session.post.call_args[1]["data"])
        assert (
            posted_data["userName"] == "test.employee@example.com"
            and posted_data["tenantId"] == "00000000-0000-0000-0000-000000000000"
            and posted_data["notes"] == "These are notes"
            and posted_data["departureDate"] == "12-08-2023"
            and posted_data["alertsEnabled"] == True
            and posted_data["cloudUsernames"] == ["test.employee@microsoft.com"]
        )

    def test_create_departing_employee_posts_to_expected_url(self, mock_session, customer):
        client = DepartingEmployeeClient(mock_session, customer)
        client.create_departing_employee("test.employee@example.com")
        assert mock_session.post.call_args[0][0] == "/svc/api/v1/departingemployee/create"

    def test_resolve_departing_employee_uses_given_tenant_id_over_current_id(
        self, mock_session, customer
    ):
        client = DepartingEmployeeClient(mock_session, customer)
        client.resolve_departing_employee("999", "22222222-2222-2222-2222-222222222222")
        post_call_args = json.loads(mock_session.post.call_args[1]["data"])
        assert post_call_args["tenantId"] == "22222222-2222-2222-2222-222222222222"

    def test_resolve_departing_employee_posts_expected_data(self, mock_session, customer):
        client = DepartingEmployeeClient(mock_session, customer)
        client.resolve_departing_employee("999")

        # Have to convert the request data to a dict because
        # older versions of Python don't have deterministic order.
        posted_data = json.loads(mock_session.post.call_args[1]["data"])
        assert (
            posted_data["caseId"] == "999"
            and posted_data["tenantId"] == "00000000-0000-0000-0000-000000000000"
        )

    def test_resolve_departing_employee_posts_to_expected_url(self, mock_session, customer):
        client = DepartingEmployeeClient(mock_session, customer)
        client.resolve_departing_employee("test.employee@example.com")
        assert mock_session.post.call_args[0][0] == "/svc/api/v1/departingemployee/resolve"

    def test_get_all_departing_employees_uses_given_tenant_id_over_current_id(
        self, mock_session, customer
    ):
        client = DepartingEmployeeClient(mock_session, customer)
        client.get_all_departing_employees("22222222-2222-2222-2222-222222222222")
        post_call_args = json.loads(mock_session.post.call_args[1]["data"])
        assert post_call_args["tenantId"] == "22222222-2222-2222-2222-222222222222"

    def test_get_all_departing_employees_posts_expected_data(self, mock_session, customer):
        client = DepartingEmployeeClient(mock_session, customer)
        client.get_all_departing_employees(None, 101, 2, "09-24-2023", "USERNAME", "ASC")

        # Have to convert the request data to a dict because
        # older versions of Python don't have deterministic order.
        posted_data = json.loads(mock_session.post.call_args[1]["data"])
        assert (
            posted_data["tenantId"] == "00000000-0000-0000-0000-000000000000"
            and posted_data["pgSize"] == 101
            and posted_data["pgNum"] == 2
            and posted_data["departingOnOrAfter"] == "09-24-2023"
            and posted_data["srtKey"] == "USERNAME"
            and posted_data["srtDirection"] == "ASC"
        )

    def test_get_all_departing_employees_posts_to_expected_url(self, mock_session, customer):
        client = DepartingEmployeeClient(mock_session, customer)
        client.get_all_departing_employees()
        assert mock_session.post.call_args[0][0] == "/svc/api/v1/departingemployee/search"

    def test_toggle_alerts_uses_given_tenant_id_over_current_id(self, mock_session, customer):
        client = DepartingEmployeeClient(mock_session, customer)
        client.toggle_alerts("22222222-2222-2222-2222-222222222222")
        post_call_args = json.loads(mock_session.post.call_args[1]["data"])
        assert post_call_args["tenantId"] == "22222222-2222-2222-2222-222222222222"

    def test_toggle_alerts_posts_expected_data(self, mock_session, customer):
        client = DepartingEmployeeClient(mock_session, customer)
        client.toggle_alerts()

        # Have to convert the request data to a dict because
        # older versions of Python don't have deterministic order.
        posted_data = json.loads(mock_session.post.call_args[1]["data"])
        assert (
            posted_data["tenantId"] == "00000000-0000-0000-0000-000000000000"
            and posted_data["alertsEnabled"] == True
        )

    def test_toggle_alerts_posts_to_expected_url(self, mock_session, customer):
        client = DepartingEmployeeClient(mock_session, customer)
        client.toggle_alerts()
        assert mock_session.post.call_args[0][0] == "/svc/api/v1/departingemployee/togglealerts"

    def test_get_case_by_username_uses_given_tenant_id_over_current_id(
        self, mock_session, customer, mock_get_all_cases_function
    ):
        client = DepartingEmployeeClient(mock_session, customer)
        client.get_case_by_username(
            "test.example@example.com", "22222222-2222-2222-2222-222222222222"
        )
        post_call_args = json.loads(mock_session.post.call_args[1]["data"])
        assert post_call_args["tenantId"] == "22222222-2222-2222-2222-222222222222"

    def test_get_case_by_username_posts_expected_data(
        self, mock_session, customer, mock_get_all_cases_function
    ):
        client = DepartingEmployeeClient(mock_session, customer)
        client.get_case_by_username("test.example@example.com")

        # Have to convert the request data to a dict because
        # older versions of Python don't have deterministic order.
        posted_data = json.loads(mock_session.post.call_args[1]["data"])
        assert (
            posted_data["tenantId"] == "00000000-0000-0000-0000-000000000000"
            and posted_data["caseId"] == "20"
        )

    def test_get_case_by_username_posts_to_expected_url(
        self, mock_session, customer, mock_get_all_cases_function
    ):
        client = DepartingEmployeeClient(mock_session, customer)
        client.get_case_by_username("test.example@example.com")
        assert mock_session.post.call_args[0][0] == "/svc/api/v1/departingemployee/details"

    def test_get_case_by_id_uses_given_tenant_id_over_current_id(self, mock_session, customer):
        client = DepartingEmployeeClient(mock_session, customer)
        client.get_case_by_id("999", "22222222-2222-2222-2222-222222222222")
        post_call_args = json.loads(mock_session.post.call_args[1]["data"])
        assert post_call_args["tenantId"] == "22222222-2222-2222-2222-222222222222"

    def test_get_case_by_id_posts_expected_data(self, mock_session, customer):
        client = DepartingEmployeeClient(mock_session, customer)
        client.get_case_by_id("999")

        # Have to convert the request data to a dict because
        # older versions of Python don't have deterministic order.
        posted_data = json.loads(mock_session.post.call_args[1]["data"])
        assert (
            posted_data["tenantId"] == "00000000-0000-0000-0000-000000000000"
            and posted_data["caseId"] == "999"
        )

    def test_get_case_by_id_posts_to_expected_url(self, mock_session, customer):
        client = DepartingEmployeeClient(mock_session, customer)
        client.get_case_by_id("999")
        assert mock_session.post.call_args[0][0] == "/svc/api/v1/departingemployee/details"

    def test_update_case_uses_given_tenant_id_over_current_id(
        self, mock_session, customer, mock_get_case_details_function
    ):
        client = DepartingEmployeeClient(mock_session, customer)
        client.update_case("697", "22222222-2222-2222-2222-222222222222")
        post_call_args = json.loads(mock_session.post.call_args[1]["data"])
        assert post_call_args["tenantId"] == "22222222-2222-2222-2222-222222222222"

    def test_update_case_posts_expected_data(
        self, mock_session, customer, mock_get_case_details_function
    ):
        client = DepartingEmployeeClient(mock_session, customer)
        client.update_case(
            "697",
            None,
            "Display Name",
            "These are notes",
            "12-12-2023",
            False,
            "EXFILTRATION_24_HOURS",
            ["test@test.com"],
        )

        # Have to convert the request data to a dict because
        # older versions of Python don't have deterministic order.
        posted_data = json.loads(mock_session.post.call_args[1]["data"])
        assert (
            posted_data["tenantId"] == "00000000-0000-0000-0000-000000000000"
            and posted_data["caseId"] == "697"
            and posted_data["displayName"] == "Display Name"
            and posted_data["notes"] == "These are notes"
            and posted_data["departureDate"] == "12-12-2023"
            and posted_data["alertsEnabled"] == False
            and posted_data["status"] == "EXFILTRATION_24_HOURS"
            and posted_data["cloudUsernames"] == ["test@test.com"]
        )

    def test_update_case_uses_current_data_when_not_provided_uses_excluding_departure_date(
        self, mock_session, customer, mock_get_case_details_function
    ):
        client = DepartingEmployeeClient(mock_session, customer)
        client.update_case("20")

        # Have to convert the request data to a dict because
        # older versions of Python don't have deterministic order.
        posted_data = json.loads(mock_session.post.call_args[1]["data"])
        assert (
            posted_data["tenantId"] == "00000000-0000-0000-0000-000000000000"
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
        self, mock_session, customer, mock_get_case_details_function
    ):
        client = DepartingEmployeeClient(mock_session, customer)
        client.update_case("697")
        assert mock_session.post.call_args[0][0] == "/svc/api/v1/departingemployee/update"
