import pytest
from py42.clients.cases import CasesClient
from py42.services.cases import CasesService
from py42.services.casesfileevents import CasesFileEventsService


@pytest.fixture
def mock_cases_service(mocker):
    return mocker.MagicMock(spec=CasesService)


@pytest.fixture
def mock_cases_file_event_service(mocker):
    return mocker.MagicMock(spec=CasesFileEventsService)


class TestCasesClient():

    def test_file_events_returns_cases_file_events_service(
        self, mock_cases_service, mock_cases_file_event_service
    ):
        cases_client = CasesClient(mock_cases_service, mock_cases_file_event_service)
        assert cases_client.file_events is mock_cases_file_event_service

    def test_create_calls_cases_service_with_expected_params(
        self, mock_cases_service, mock_cases_file_event_service
    ):
        cases_client = CasesClient(mock_cases_service, mock_cases_file_event_service)
        cases_client.create("name", "subject", "assignee", "description", "observation")
        mock_cases_service.create.assert_called_once_with(
            "name", "subject", "assignee", "description", "observation"
        )

    def test_get_all_calls_cases_service_with_expected_params(
        self, mock_cases_service, mock_cases_file_event_service
    ):
        cases_client = CasesClient(mock_cases_service, mock_cases_file_event_service)
        cases_client.get_all()
        mock_cases_service.get_all.assert_called_once()

    def test_get_case_by_case_number_calls_cases_service_with_expected_params(
        self, mock_cases_service, mock_cases_file_event_service
    ):
        cases_client = CasesClient(mock_cases_service, mock_cases_file_event_service)
        cases_client.get_case_by_case_number(123456)
        mock_cases_service.get_case.assert_called_once_with(123456)

    def test_export_calls_cases_service_with_expected_params(
        self, mock_cases_service, mock_cases_file_event_service
    ):
        cases_client = CasesClient(mock_cases_service, mock_cases_file_event_service)
        cases_client.export_summary(123456)
        mock_cases_service.export_summary.assert_called_once_with(123456)

    def test_update_calls_cases_service_with_expected_params(
        self, mock_cases_service, mock_cases_file_event_service
    ):
        cases_client = CasesClient(mock_cases_service, mock_cases_file_event_service)
        cases_client.update(123456, name="new name")
        mock_cases_service.update.assert_called_once_with(123456, "new name", "", "", "", "")
