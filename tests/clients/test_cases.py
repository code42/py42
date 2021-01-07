from datetime import datetime

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
        cases_client.create(
            "name",
            subject="subject",
            assignee="assignee",
            description="description",
            findings="observation",
        )
        mock_cases_service.create.assert_called_once_with(
            "name",
            subject="subject",
            assignee="assignee",
            description="description",
            findings="observation",
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
            _TEST_CASE_NUMBER,
            name="new name",
            assignee=None,
            subject=None,
            status=None,
            description=None,
            findings=None,
        )

    def test_get_all_converts_datetime_to_ranges_and_calls_service_with_expected_params(
        self, mock_cases_service, mock_cases_file_event_service
    ):
        cases_client = CasesClient(mock_cases_service, mock_cases_file_event_service)
        cases_client.get_all(
            created_at_begin_time="2021-01-01 00:00:00",
            updated_at_begin_time="2021-02-01 00:00:00",
            created_at_end_time="2021-01-31 00:00:00",
            updated_at_end_time="2021-02-20 00:00:00",
        )
        created_at_range = "2021-01-01T00:00:00.000Z/2021-01-31T00:00:00.000Z"
        updated_at_range = "2021-02-01T00:00:00.000Z/2021-02-20T00:00:00.000Z"

        mock_cases_service.get_all.assert_called_once_with(
            name=None,
            status=None,
            created_at=created_at_range,
            updated_at=updated_at_range,
            subject=None,
            assignee=None,
            page_number=1,
            page_size=100,
            sort_direction="asc",
            sort_key="number",
        )

    def test_get_all_converts_diff_types_to_ranges_and_calls_service_with_expected_params(
        self, mock_cases_service, mock_cases_file_event_service
    ):
        cases_client = CasesClient(mock_cases_service, mock_cases_file_event_service)
        cases_client.get_all(
            created_at_begin_time=1609439400,
            updated_at_begin_time="2021-02-01 00:00:00",
            created_at_end_time=1612117800.0,
            updated_at_end_time=datetime.strptime(
                "2021-02-20 00:00:00", u"%Y-%m-%d %H:%M:%S"
            ),
            subject="subject",
            assignee="a",
            name="test",
            status="closed",
        )
        created_at_range = "2020-12-31T18:30:00.000Z/2021-01-31T18:30:00.000Z"
        updated_at_range = "2021-02-01T00:00:00.000Z/2021-02-20T00:00:00.000Z"

        mock_cases_service.get_all.assert_called_once_with(
            name="test",
            status="closed",
            created_at=created_at_range,
            updated_at=updated_at_range,
            subject="subject",
            assignee="a",
            page_number=1,
            page_size=100,
            sort_direction="asc",
            sort_key="number",
        )

    def test_get_all_send_not_in_ranges_when_only_begin_or_end_time_is_specified(
        self, mock_cases_service, mock_cases_file_event_service
    ):
        cases_client = CasesClient(mock_cases_service, mock_cases_file_event_service)
        cases_client.get_all(
            created_at_begin_time=1609439400,
            updated_at_begin_time=None,
            created_at_end_time=None,
            updated_at_end_time=datetime.strptime(
                "2021-02-20 00:00:00", u"%Y-%m-%d %H:%M:%S"
            ),
            subject="subject",
            assignee="a",
            name="test",
            status="closed",
        )

        mock_cases_service.get_all.assert_called_once_with(
            name="test",
            status="closed",
            created_at=None,
            updated_at=None,
            subject="subject",
            assignee="a",
            page_number=1,
            page_size=100,
            sort_direction="asc",
            sort_key="number",
        )
