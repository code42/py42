# -*- coding: utf-8 -*-

import pytest
import json
from requests import Response

from py42._internal.clients.employee_case_management.departing_employee import (
    DepartingEmployeeClient,
)
from py42._internal.clients.administration import AdministrationClient


class TestDepartingEmployeeClient(object):
    @pytest.fixture
    def administration_client(self, mocker):
        client = mocker.MagicMock(spec=AdministrationClient)
        response = mocker.MagicMock(spec=Response)
        response.text = (
            '{"data":{"name":"Some SaaS Cloud","registrationKey":"0000000000000000",'
            '"deploymentModel":"PUBLIC","maintenanceMode":false,'
            '"tenantUid":"00000000-0000-0000-0000-000000000000",'
            '"masterServicesAgreement":{"accepted":true,"acceptanceRequired":false}},'
            '"error":null,"warnings":null}'
        )
        response.status_code = 200
        client.get_current_tenant.return_value = response
        return client

    @pytest.fixture
    def mock_get_all_cases_function(self, mocker):
        # Useful for testing get_case_by_username, which first gets all cases.
        # Also useful in update_case, which checks current values of case
        mock = mocker.patch(
            "py42._internal.clients.employee_case_management.departing_employee.DepartingEmployeeClient.get_all_departing_employees"
        )
        response = mocker.MagicMock(spec=Response)
        response.text = (
            '{"type$":"DEPARTING_EMPLOYEE_SEARCH_RESPONSE","cases"'
            ':[{"type$":"DEPARTING_EMPLOYEE_CASE","tenantId":'
            '"00000000-0000-0000-0000-000000000000","caseId":"697",'
            '"userUid":"999999999999999999","userName":'
            '"test.testerson@example.com","displayName":'
            '"Test Testerson","notes":"These are notes","createdAt":'
            '"2020-02-11T20:43:58.3611040Z","status":"OPEN","alertsEnabled":true}'
            ',{"type$":"DEPARTING_EMPLOYEE_CASE","tenantId":'
            '"00000000-0000-0000-0000-000000000000","caseId":"20","userUid":'
            '"888888888888888888","userName":"test.example@example.com",'
            '"displayName":"Test Example","notes":"","createdAt":'
            '"2019-10-25T13:31:14.1199010Z","status":"OPEN","cloudUsernames"'
            ':["test.example@example.com"],"alertsEnabled":true}],'
            '"totalCount":2}'
        )
        response.status_code = 200
        mock.return_value = response
        return mock

    def test_create_departing_employee_gets_tenant_id_from_administration_client_if_needed(
        self, mock_session, administration_client
    ):
        client = DepartingEmployeeClient(mock_session, administration_client)
        client._tenant_id = None  # Not needed, but just for clarity
        client.create_departing_employee("test.employee@example.com")
        assert client._tenant_id == "00000000-0000-0000-0000-000000000000"

    def test_create_departing_employee_uses_current_tenant_id_over_one_from_administration_client(
        self, mock_session, administration_client
    ):
        client = DepartingEmployeeClient(mock_session, administration_client)
        client._tenant_id = "11111111-1111-1111-1111-111111111111"
        client.create_departing_employee("test.employee@example.com")
        assert client._tenant_id == "11111111-1111-1111-1111-111111111111"

    def test_create_departing_employee_uses_given_tenant_id_over_current_id(
        self, mock_session, administration_client
    ):
        client = DepartingEmployeeClient(mock_session, administration_client)
        client._tenant_id = "11111111-1111-1111-1111-111111111111"
        client.create_departing_employee(
            "test.employee@example.com", "22222222-2222-2222-2222-222222222222"
        )
        post_call_args = json.loads(mock_session.post.call_args[1]["data"])
        assert post_call_args["tenantId"] == "22222222-2222-2222-2222-222222222222"

    def test_create_departing_employee_posts_expected_data(
        self, mock_session, administration_client
    ):
        client = DepartingEmployeeClient(mock_session, administration_client)
        client.create_departing_employee(
            "test.employee@example.com",
            None,
            "These are notes",
            "12-08-2023",
            True,
            ["test.employee@microsoft.com"],
        )
        assert (
            mock_session.post.call_args[1]["data"]
            == '{"userName": "test.employee@example.com", "tenantId": '
            '"00000000-0000-0000-0000-000000000000", "notes": "These are notes", '
            '"departureDate": "12-08-2023", "alertsEnabled": true, "cloudUsernames": '
            '["test.employee@microsoft.com"]}'
        )

    def test_create_departing_employee_posts_to_expected_url(
        self, mock_session, administration_client
    ):
        client = DepartingEmployeeClient(mock_session, administration_client)
        client.create_departing_employee("test.employee@example.com")
        assert mock_session.post.call_args[0][0] == "/svc/api/v1/departingemployee/create"

    def test_resolve_departing_employee_gets_tenant_id_from_administration_client_if_needed(
        self, mock_session, administration_client
    ):
        client = DepartingEmployeeClient(mock_session, administration_client)
        client._tenant_id = None  # Not needed, but just for clarity
        client.resolve_departing_employee("999")
        assert client._tenant_id == "00000000-0000-0000-0000-000000000000"

    def test_resolve_departing_employee_uses_current_tenant_id_over_one_from_administration_client(
        self, mock_session, administration_client
    ):
        client = DepartingEmployeeClient(mock_session, administration_client)
        client._tenant_id = "11111111-1111-1111-1111-111111111111"
        client.resolve_departing_employee("999")
        assert client._tenant_id == "11111111-1111-1111-1111-111111111111"

    def test_resolve_departing_employee_uses_given_tenant_id_over_current_id(
        self, mock_session, administration_client
    ):
        client = DepartingEmployeeClient(mock_session, administration_client)
        client._tenant_id = "11111111-1111-1111-1111-111111111111"
        client.resolve_departing_employee("999", "22222222-2222-2222-2222-222222222222")
        post_call_args = json.loads(mock_session.post.call_args[1]["data"])
        assert post_call_args["tenantId"] == "22222222-2222-2222-2222-222222222222"

    def test_resolve_departing_employee_posts_expected_data(
        self, mock_session, administration_client
    ):
        client = DepartingEmployeeClient(mock_session, administration_client)
        client.resolve_departing_employee("999")
        assert (
            mock_session.post.call_args[1]["data"]
            == '{"caseId": "999", "tenantId": "00000000-0000-0000-0000-000000000000"}'
        )

    def test_resolve_departing_employee_posts_to_expected_url(
        self, mock_session, administration_client
    ):
        client = DepartingEmployeeClient(mock_session, administration_client)
        client.resolve_departing_employee("test.employee@example.com")
        assert mock_session.post.call_args[0][0] == "/svc/api/v1/departingemployee/resolve"

    def test_get_all_departing_employees_gets_tenant_id_from_administration_client_if_needed(
        self, mock_session, administration_client
    ):
        client = DepartingEmployeeClient(mock_session, administration_client)
        client._tenant_id = None  # Not needed, but just for clarity
        client.get_all_departing_employees()
        assert client._tenant_id == "00000000-0000-0000-0000-000000000000"

    def test_get_all_departing_employees_uses_current_tenant_id_over_one_from_administration_client(
        self, mock_session, administration_client
    ):
        client = DepartingEmployeeClient(mock_session, administration_client)
        client._tenant_id = "11111111-1111-1111-1111-111111111111"
        client.get_all_departing_employees()
        assert client._tenant_id == "11111111-1111-1111-1111-111111111111"

    def test_get_all_departing_employees_uses_given_tenant_id_over_current_id(
        self, mock_session, administration_client
    ):
        client = DepartingEmployeeClient(mock_session, administration_client)
        client._tenant_id = "11111111-1111-1111-1111-111111111111"
        client.get_all_departing_employees("22222222-2222-2222-2222-222222222222")
        post_call_args = json.loads(mock_session.post.call_args[1]["data"])
        assert post_call_args["tenantId"] == "22222222-2222-2222-2222-222222222222"

    def test_get_all_departing_employees_posts_expected_data(
        self, mock_session, administration_client
    ):
        client = DepartingEmployeeClient(mock_session, administration_client)
        client.get_all_departing_employees(None, 101, 2, "09-24-2023", "USERNAME", "ASC")
        assert (
            mock_session.post.call_args[1]["data"]
            == '{"tenantId": "00000000-0000-0000-0000-000000000000", "pgSize": 101, "pgNum": '
            '2, "departingOnOrAfter": "09-24-2023", "srtKey": "USERNAME", "srtDirection": '
            '"ASC"}'
        )

    def test_get_all_departing_employees_posts_to_expected_url(
        self, mock_session, administration_client
    ):
        client = DepartingEmployeeClient(mock_session, administration_client)
        client.get_all_departing_employees()
        assert mock_session.post.call_args[0][0] == "/svc/api/v1/departingemployee/search"

    def test_search_departing_employees_gets_tenant_id_from_administration_client_if_needed(
        self, mock_session, administration_client
    ):
        client = DepartingEmployeeClient(mock_session, administration_client)
        client._tenant_id = None  # Not needed, but just for clarity
        client.search_departing_employees("EXFILTRATION_24_HOURS")
        assert client._tenant_id == "00000000-0000-0000-0000-000000000000"

    def test_search_departing_employees_uses_current_tenant_id_over_one_from_administration_client(
        self, mock_session, administration_client
    ):
        client = DepartingEmployeeClient(mock_session, administration_client)
        client._tenant_id = "11111111-1111-1111-1111-111111111111"
        client.search_departing_employees("EXFILTRATION_24_HOURS")
        assert client._tenant_id == "11111111-1111-1111-1111-111111111111"

    def test_search_departing_employees_uses_given_tenant_id_over_current_id(
        self, mock_session, administration_client
    ):
        client = DepartingEmployeeClient(mock_session, administration_client)
        client._tenant_id = "11111111-1111-1111-1111-111111111111"
        client.search_departing_employees(
            "EXFILTRATION_24_HOURS", "22222222-2222-2222-2222-222222222222"
        )
        post_call_args = json.loads(mock_session.post.call_args[1]["data"])
        assert post_call_args["tenantId"] == "22222222-2222-2222-2222-222222222222"

    def test_search_departing_employees_posts_expected_data(
        self, mock_session, administration_client
    ):
        client = DepartingEmployeeClient(mock_session, administration_client)
        client.search_departing_employees("EXFILTRATION_24_HOURS")
        assert (
            mock_session.post.call_args[1]["data"]
            == '{"tenantId": "00000000-0000-0000-0000-000000000000", "filterType": '
            '"EXFILTRATION_24_HOURS", "pgSize": 1, "pgNum": 100, "departingOnOrAfter": '
            'null, "srtKey": "CREATED_AT", "srtDirection": "DESC"}'
        )

    def test_search_departing_employees_posts_to_expected_url(
        self, mock_session, administration_client
    ):
        client = DepartingEmployeeClient(mock_session, administration_client)
        client.search_departing_employees("EXFILTRATION_24_HOURS")
        assert mock_session.post.call_args[0][0] == "/svc/api/v1/departingemployee/filteredsearch"

    def test_toggle_alerts_gets_tenant_id_from_administration_client_if_needed(
        self, mock_session, administration_client
    ):
        client = DepartingEmployeeClient(mock_session, administration_client)
        client._tenant_id = None  # Not needed, but just for clarity
        client.toggle_alerts()
        assert client._tenant_id == "00000000-0000-0000-0000-000000000000"

    def test_toggle_alerts_uses_current_tenant_id_over_one_from_administration_client(
        self, mock_session, administration_client
    ):
        client = DepartingEmployeeClient(mock_session, administration_client)
        client._tenant_id = "11111111-1111-1111-1111-111111111111"
        client.toggle_alerts()
        assert client._tenant_id == "11111111-1111-1111-1111-111111111111"

    def test_toggle_alerts_uses_given_tenant_id_over_current_id(
        self, mock_session, administration_client
    ):
        client = DepartingEmployeeClient(mock_session, administration_client)
        client._tenant_id = "11111111-1111-1111-1111-111111111111"
        client.toggle_alerts("22222222-2222-2222-2222-222222222222")
        post_call_args = json.loads(mock_session.post.call_args[1]["data"])
        assert post_call_args["tenantId"] == "22222222-2222-2222-2222-222222222222"

    def test_toggle_alerts_posts_expected_data(self, mock_session, administration_client):
        client = DepartingEmployeeClient(mock_session, administration_client)
        client.toggle_alerts()
        assert (
            mock_session.post.call_args[1]["data"]
            == '{"tenantId": "00000000-0000-0000-0000-000000000000", "alertsEnabled": true}'
        )

    def test_toggle_alerts_posts_to_expected_url(self, mock_session, administration_client):
        client = DepartingEmployeeClient(mock_session, administration_client)
        client.toggle_alerts()
        assert mock_session.post.call_args[0][0] == "/svc/api/v1/departingemployee/togglealerts"

    def test_get_case_by_username_gets_tenant_id_from_administration_client_if_needed(
        self, mock_session, administration_client, mock_get_all_cases_function
    ):
        client = DepartingEmployeeClient(mock_session, administration_client)
        client._tenant_id = None  # Not needed, but just for clarity
        client.get_case_by_username("test.example@example.com")
        assert client._tenant_id == "00000000-0000-0000-0000-000000000000"

    def test_get_case_by_username_uses_current_tenant_id_over_one_from_administration_client(
        self, mock_session, administration_client, mock_get_all_cases_function
    ):
        client = DepartingEmployeeClient(mock_session, administration_client)
        client._tenant_id = "11111111-1111-1111-1111-111111111111"
        client.get_case_by_username("test.example@example.com")
        assert client._tenant_id == "11111111-1111-1111-1111-111111111111"

    def test_get_case_by_username_uses_given_tenant_id_over_current_id(
        self, mock_session, administration_client, mock_get_all_cases_function
    ):
        client = DepartingEmployeeClient(mock_session, administration_client)
        client._tenant_id = "11111111-1111-1111-1111-111111111111"
        client.get_case_by_username(
            "test.example@example.com", "22222222-2222-2222-2222-222222222222"
        )
        post_call_args = json.loads(mock_session.post.call_args[1]["data"])
        assert post_call_args["tenantId"] == "22222222-2222-2222-2222-222222222222"

    def test_get_case_by_username_posts_expected_data(
        self, mock_session, administration_client, mock_get_all_cases_function
    ):
        client = DepartingEmployeeClient(mock_session, administration_client)
        client.get_case_by_username("test.example@example.com")
        assert (
            mock_session.post.call_args[1]["data"]
            == '{"tenantId": "00000000-0000-0000-0000-000000000000", "caseId": "20"}'
        )

    def test_get_case_by_username_posts_to_expected_url(
        self, mock_session, administration_client, mock_get_all_cases_function
    ):
        client = DepartingEmployeeClient(mock_session, administration_client)
        client.get_case_by_username("test.example@example.com")
        assert mock_session.post.call_args[0][0] == "/svc/api/v1/departingemployee/details"

    def test_get_case_by_id_gets_tenant_id_from_administration_client_if_needed(
        self, mock_session, administration_client, mock_get_all_cases_function
    ):
        client = DepartingEmployeeClient(mock_session, administration_client)
        client._tenant_id = None  # Not needed, but just for clarity
        client.get_case_by_id("999")
        assert client._tenant_id == "00000000-0000-0000-0000-000000000000"

    def test_get_case_by_id_uses_current_tenant_id_over_one_from_administration_client(
        self, mock_session, administration_client, mock_get_all_cases_function
    ):
        client = DepartingEmployeeClient(mock_session, administration_client)
        client._tenant_id = "11111111-1111-1111-1111-111111111111"
        client.get_case_by_id("999")
        assert client._tenant_id == "11111111-1111-1111-1111-111111111111"

    def test_get_case_by_id_uses_given_tenant_id_over_current_id(
        self, mock_session, administration_client, mock_get_all_cases_function
    ):
        client = DepartingEmployeeClient(mock_session, administration_client)
        client._tenant_id = "11111111-1111-1111-1111-111111111111"
        client.get_case_by_id("999", "22222222-2222-2222-2222-222222222222")
        post_call_args = json.loads(mock_session.post.call_args[1]["data"])
        assert post_call_args["tenantId"] == "22222222-2222-2222-2222-222222222222"

    def test_get_case_by_id_posts_expected_data(
        self, mock_session, administration_client, mock_get_all_cases_function
    ):
        client = DepartingEmployeeClient(mock_session, administration_client)
        client.get_case_by_id("999")
        assert (
            mock_session.post.call_args[1]["data"]
            == '{"tenantId": "00000000-0000-0000-0000-000000000000", "caseId": "999"}'
        )

    def test_get_case_by_id_posts_to_expected_url(
        self, mock_session, administration_client, mock_get_all_cases_function
    ):
        client = DepartingEmployeeClient(mock_session, administration_client)
        client.get_case_by_id("999")
        assert mock_session.post.call_args[0][0] == "/svc/api/v1/departingemployee/details"

    def test_update_case_gets_tenant_id_from_administration_client_if_needed(
        self, mock_session, administration_client, mock_get_all_cases_function
    ):
        client = DepartingEmployeeClient(mock_session, administration_client)
        client._tenant_id = None  # Not needed, but just for clarity
        client.update_case("697")
        assert client._tenant_id == "00000000-0000-0000-0000-000000000000"

    def test_update_case_uses_current_tenant_id_over_one_from_administration_client(
        self, mock_session, administration_client, mock_get_all_cases_function
    ):
        client = DepartingEmployeeClient(mock_session, administration_client)
        client._tenant_id = "11111111-1111-1111-1111-111111111111"
        client.update_case("697")
        assert client._tenant_id == "11111111-1111-1111-1111-111111111111"

    def test_update_case_uses_given_tenant_id_over_current_id(
        self, mock_session, administration_client, mock_get_all_cases_function
    ):
        client = DepartingEmployeeClient(mock_session, administration_client)
        client._tenant_id = "11111111-1111-1111-1111-111111111111"
        client.update_case("697", "22222222-2222-2222-2222-222222222222")
        post_call_args = json.loads(mock_session.post.call_args[1]["data"])
        assert post_call_args["tenantId"] == "22222222-2222-2222-2222-222222222222"

    def test_update_case_posts_expected_data(
        self, mock_session, administration_client, mock_get_all_cases_function
    ):
        client = DepartingEmployeeClient(mock_session, administration_client)
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
        assert (
            mock_session.post.call_args[1]["data"]
            == '{"tenantId": "00000000-0000-0000-0000-000000000000", "caseId": "697", '
            '"displayName": "Display Name", "notes": "These are notes", "departureDate": '
            '"12-12-2023", "alertsEnabled": false, "status": "EXFILTRATION_24_HOURS", '
            '"cloudUsernames": ["test@test.com"]}'
        )

    def test_update_case_uses_current_data_when_not_provided_uses_excluding_departure_date(
        self, mock_session, administration_client, mock_get_all_cases_function
    ):
        client = DepartingEmployeeClient(mock_session, administration_client)
        client.update_case("20")
        assert (
            mock_session.post.call_args[1]["data"]
            == '{"tenantId": "00000000-0000-0000-0000-000000000000", "caseId": "20", '
            '"displayName": "Test Example", "notes": "", "departureDate": null, '
            '"alertsEnabled": true, "status": "OPEN", "cloudUsernames": '
            '["test.example@example.com"]}'
        )

    def test_update_case_posts_to_expected_url(
        self, mock_session, administration_client, mock_get_all_cases_function
    ):
        client = DepartingEmployeeClient(mock_session, administration_client)
        client.update_case("697")
        assert mock_session.post.call_args[0][0] == "/svc/api/v1/departingemployee/update"
