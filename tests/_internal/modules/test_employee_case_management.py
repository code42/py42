import pytest

from py42._internal.modules.employee_case_management import EmployeeCaseManagementModule
from py42._internal.client_factories import EmployeeCaseManagementClientFactory
from py42._internal.clients.employee_case_management.departing_employee import (
    DepartingEmployeeClient,
)


class TestEmployeeCaseManagementModule(object):
    @pytest.fixture
    def client_factory(self, mocker):
        return mocker.MagicMock(spec=EmployeeCaseManagementClientFactory)

    @pytest.fixture
    def departing_employee_client(self, mocker):
        return mocker.MagicMock(spec=DepartingEmployeeClient)

    @staticmethod
    def return_departing_employee_client(departing_employee_client):
        def mock_get_departing_employee_client():
            return departing_employee_client

        return mock_get_departing_employee_client

    def test_departing_employee_calls_through_to_client(
        self, client_factory, departing_employee_client
    ):
        client_factory.get_departing_employee_client.side_effect = self.return_departing_employee_client(
            departing_employee_client
        )
        ecm_module = EmployeeCaseManagementModule(client_factory)
        ecm_module.departing_employee.get_case_by_username("Test")
        departing_employee_client.get_case_by_username.assert_called_once_with("Test")

    def test_departing_employee_creates_client_only_once(
        self, client_factory, departing_employee_client
    ):
        client_factory.get_departing_employee_client.side_effect = self.return_departing_employee_client(
            departing_employee_client
        )
        ecm_module = EmployeeCaseManagementModule(client_factory)
        _ = ecm_module.departing_employee
        _ = ecm_module.departing_employee
        assert client_factory.get_departing_employee_client.call_count == 1
