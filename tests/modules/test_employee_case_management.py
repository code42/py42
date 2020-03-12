import pytest

from py42._internal.client_factories import MicroserviceClientFactory
from py42.clients.detection_lists.departing_employee import DepartingEmployeeClient
from py42.modules.detection_lists import DetectionListsModule


class TestDetectionListsModule(object):
    @pytest.fixture
    def client_factory(self, mocker):
        return mocker.MagicMock(spec=MicroserviceClientFactory)

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
        ecm_module = DetectionListsModule(client_factory)
        ecm_module.departing_employee.get_by_username("Test")
        departing_employee_client.get_by_username.assert_called_once_with("Test")

    def test_departing_employee_creates_client_only_once(
        self, client_factory, departing_employee_client
    ):
        client_factory.get_departing_employee_client.side_effect = self.return_departing_employee_client(
            departing_employee_client
        )
        ecm_module = DetectionListsModule(client_factory)
        first = ecm_module.departing_employee
        second = ecm_module.departing_employee
        assert first is second
