import pytest

from py42.clients.cases import CasesClient
from py42.services.cases import CasesService
from py42.services.casesfileevents import CasesFileEventsService

_TEST_CASE_NUMBER = 123456


@pytest.fixture
def mock_cases_service(mocker):
    return mocker.MagicMock(spec=CasesService)


@pytest.fixture
def mock_cases_file_event_service(mocker):
    return mocker.MagicMock(spec=CasesFileEventsService)


class TestCasesClient:
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
        assert mock_cases_service.get_all.call_count == 1

    def test_get_case_calls_cases_service_with_expected_params(
        self, mock_cases_service, mock_cases_file_event_service
    ):
        cases_client = CasesClient(mock_cases_service, mock_cases_file_event_service)
        cases_client.get_case(_TEST_CASE_NUMBER)
        mock_cases_service.get_case.assert_called_once_with(_TEST_CASE_NUMBER)

    def test_export_calls_cases_service_with_expected_params(
        self, mock_cases_service, mock_cases_file_event_service
    ):
        cases_client = CasesClient(mock_cases_service, mock_cases_file_event_service)
        cases_client.export_summary(_TEST_CASE_NUMBER)
        mock_cases_service.export_summary.assert_called_once_with(_TEST_CASE_NUMBER)

    def test_update_calls_cases_service_with_expected_params(
        self, mock_cases_service, mock_cases_file_event_service
    ):
        cases_client = CasesClient(mock_cases_service, mock_cases_file_event_service)
        cases_client.update(_TEST_CASE_NUMBER, name="new name")
        mock_cases_service.update.assert_called_once_with(
            _TEST_CASE_NUMBER, "new name", "", "", "", ""
        )
