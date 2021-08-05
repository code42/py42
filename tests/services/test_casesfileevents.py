import pytest
from tests.conftest import create_mock_error

from py42.exceptions import Py42BadRequestError
from py42.exceptions import Py42CaseAlreadyHasEventError
from py42.exceptions import Py42UpdateClosedCaseError
from py42.services.casesfileevents import CasesFileEventsService

_TEST_CASE_NUMBER = 123456
UPDATE_ERROR_RESPONSE = '{"problem":"CASE_IS_CLOSED"}'
ADDED_SAME_EVENT_AGAIN_ERROR = '{"problem":"CASE_ALREADY_HAS_EVENT"}'
UNKNOWN_ERROR = '{"problem":"SURPRISE!"}'


class TestCasesFileEventService:
    def test_add_called_with_expected_url_and_params(self, mock_connection):
        case_file_event_service = CasesFileEventsService(mock_connection)
        case_file_event_service.add(_TEST_CASE_NUMBER, "event-id")
        assert (
            mock_connection.post.call_args[0][0]
            == f"/api/v1/case/{_TEST_CASE_NUMBER}/fileevent/event-id"
        )

    def test_delete_called_with_expected_url_and_params(self, mock_connection):
        case_file_event_service = CasesFileEventsService(mock_connection)
        case_file_event_service.delete(_TEST_CASE_NUMBER, "event-id")
        assert (
            mock_connection.delete.call_args[0][0]
            == f"/api/v1/case/{_TEST_CASE_NUMBER}/fileevent/event-id"
        )

    def test_get_called_with_expected_url_and_params(self, mock_connection):
        case_file_event_service = CasesFileEventsService(mock_connection)
        case_file_event_service.get(_TEST_CASE_NUMBER, "event-id")
        assert (
            mock_connection.get.call_args[0][0]
            == f"/api/v1/case/{_TEST_CASE_NUMBER}/fileevent/event-id"
        )

    def test_get_all_called_with_expected_url_and_params(self, mock_connection):
        case_file_event_service = CasesFileEventsService(mock_connection)
        case_file_event_service.get_all(_TEST_CASE_NUMBER)
        assert (
            mock_connection.get.call_args[0][0]
            == f"/api/v1/case/{_TEST_CASE_NUMBER}/fileevent"
        )

    def test_add_on_a_closed_case_raises_error(self, mocker, mock_connection):
        mock_connection.post.side_effect = create_mock_error(
            Py42BadRequestError, mocker, UPDATE_ERROR_RESPONSE
        )
        case_file_event_service = CasesFileEventsService(mock_connection)
        with pytest.raises(Py42UpdateClosedCaseError) as err:
            case_file_event_service.add(_TEST_CASE_NUMBER, event_id="x")

        assert err.value.args[0] == "Cannot update a closed case."

    def test_delete_on_a_closed_case_raises_error(self, mocker, mock_connection):
        case_file_event_service = CasesFileEventsService(mock_connection)
        mock_connection.delete.side_effect = create_mock_error(
            Py42BadRequestError, mocker, UPDATE_ERROR_RESPONSE
        )
        with pytest.raises(Py42UpdateClosedCaseError) as err:
            case_file_event_service.delete(_TEST_CASE_NUMBER, event_id="x")

        assert err.value.args[0] == "Cannot update a closed case."

    def test_add_when_same_event_is_added_multiple_times_raises_error(
        self, mocker, mock_connection
    ):
        case_file_event_service = CasesFileEventsService(mock_connection)
        mock_connection.post.side_effect = create_mock_error(
            Py42BadRequestError, mocker, ADDED_SAME_EVENT_AGAIN_ERROR
        )
        with pytest.raises(Py42CaseAlreadyHasEventError) as err:
            case_file_event_service.add(_TEST_CASE_NUMBER, event_id="x")

        assert err.value.args[0] == "Event is already associated to the case."

    def test_add_when_unknown_error_raises_error(self, mocker, mock_connection):
        case_file_event_service = CasesFileEventsService(mock_connection)
        mock_connection.post.side_effect = create_mock_error(
            Py42BadRequestError, mocker, UNKNOWN_ERROR
        )
        with pytest.raises(Py42BadRequestError):
            case_file_event_service.add(_TEST_CASE_NUMBER, event_id="x")

    def test_delete_when_unknown_error_raises_error(self, mocker, mock_connection):
        case_file_event_service = CasesFileEventsService(mock_connection)
        mock_connection.post.side_effect = create_mock_error(
            Py42BadRequestError, mocker, UNKNOWN_ERROR
        )
        with pytest.raises(Py42BadRequestError):
            case_file_event_service.add(_TEST_CASE_NUMBER, event_id="x")
