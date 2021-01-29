import pytest
from requests import HTTPError

from py42.exceptions import Py42BadRequestError
from py42.exceptions import Py42CaseAlreadyHasEventError
from py42.exceptions import Py42UpdateClosedCaseError
from py42.services.casesfileevents import CasesFileEventsService

_TEST_CASE_NUMBER = 123456
UPDATE_ERROR_RESPONSE = """{"problem":"CASE_IS_CLOSED"}"""
ADDED_SAME_EVENT_AGAIN_ERROR = """{"problem":"CASE_ALREADY_HAS_EVENT"}"""
UNKNOWN_ERROR = """{"problem":"SURPRISE!"}"""


class TestCasesFileEventService:
    @pytest.fixture
    def mock_update_failed_response(self, mock_error_response):
        http_error = HTTPError(UPDATE_ERROR_RESPONSE)
        http_error.response = mock_error_response
        http_error.response.text = UPDATE_ERROR_RESPONSE
        return http_error

    @pytest.fixture
    def mock_add_same_event_multiple_times(self, mock_error_response):
        http_error = HTTPError(ADDED_SAME_EVENT_AGAIN_ERROR)
        http_error.response = mock_error_response
        http_error.response.text = ADDED_SAME_EVENT_AGAIN_ERROR
        return http_error

    @pytest.fixture
    def mock_unknown_error(self, mock_error_response):
        http_error = HTTPError(UNKNOWN_ERROR)
        http_error.response = mock_error_response
        http_error.response.text = UNKNOWN_ERROR
        return http_error

    def test_add_called_with_expected_url_and_params(self, mock_connection):
        case_file_event_service = CasesFileEventsService(mock_connection)
        case_file_event_service.add(_TEST_CASE_NUMBER, "event-id")
        assert mock_connection.post.call_args[0][
            0
        ] == u"/api/v1/case/{}/fileevent/event-id".format(_TEST_CASE_NUMBER)

    def test_delete_called_with_expected_url_and_params(self, mock_connection):
        case_file_event_service = CasesFileEventsService(mock_connection)
        case_file_event_service.delete(_TEST_CASE_NUMBER, "event-id")
        assert mock_connection.delete.call_args[0][
            0
        ] == u"/api/v1/case/{}/fileevent/event-id".format(_TEST_CASE_NUMBER)

    def test_get_called_with_expected_url_and_params(self, mock_connection):
        case_file_event_service = CasesFileEventsService(mock_connection)
        case_file_event_service.get(_TEST_CASE_NUMBER, "event-id")
        assert mock_connection.get.call_args[0][
            0
        ] == u"/api/v1/case/{}/fileevent/event-id".format(_TEST_CASE_NUMBER)

    def test_get_all_called_with_expected_url_and_params(self, mock_connection):
        case_file_event_service = CasesFileEventsService(mock_connection)
        case_file_event_service.get_all(_TEST_CASE_NUMBER)
        assert mock_connection.get.call_args[0][
            0
        ] == u"/api/v1/case/{}/fileevent".format(_TEST_CASE_NUMBER)

    def test_add_on_a_closed_case_raises_error(
        self, mock_connection, mock_update_failed_response
    ):
        case_file_event_service = CasesFileEventsService(mock_connection)
        mock_connection.post.side_effect = Py42BadRequestError(
            mock_update_failed_response
        )
        with pytest.raises(Py42UpdateClosedCaseError) as e:
            case_file_event_service.add(_TEST_CASE_NUMBER, event_id=u"x")

        assert e.value.args[0] == u"Cannot update a closed case."

    def test_delete_on_a_closed_case_raises_error(
        self, mock_connection, mock_update_failed_response
    ):
        case_file_event_service = CasesFileEventsService(mock_connection)
        mock_connection.delete.side_effect = Py42BadRequestError(
            mock_update_failed_response
        )
        with pytest.raises(Py42UpdateClosedCaseError) as e:
            case_file_event_service.delete(_TEST_CASE_NUMBER, event_id=u"x")

        assert e.value.args[0] == u"Cannot update a closed case."

    def test_add_when_same_event_is_added_multiple_times_raises_error(
        self, mock_connection, mock_add_same_event_multiple_times
    ):
        case_file_event_service = CasesFileEventsService(mock_connection)
        mock_connection.post.side_effect = Py42BadRequestError(
            mock_add_same_event_multiple_times
        )
        with pytest.raises(Py42CaseAlreadyHasEventError) as e:
            case_file_event_service.add(_TEST_CASE_NUMBER, event_id=u"x")

        assert e.value.args[0] == u"Event is already associated to the case."

    def test_add_when_unknown_error_raises_error(
        self, mock_connection, mock_unknown_error
    ):
        case_file_event_service = CasesFileEventsService(mock_connection)
        mock_connection.post.side_effect = Py42BadRequestError(mock_unknown_error)
        with pytest.raises(Py42BadRequestError) as e:
            case_file_event_service.add(_TEST_CASE_NUMBER, event_id=u"x")
        assert e.value.response.status_code == 400

    def test_delete_when_unknown_error_raises_error(
        self, mock_connection, mock_unknown_error
    ):
        case_file_event_service = CasesFileEventsService(mock_connection)
        mock_connection.post.side_effect = Py42BadRequestError(mock_unknown_error)
        with pytest.raises(Py42BadRequestError) as e:
            case_file_event_service.add(_TEST_CASE_NUMBER, event_id=u"x")
        assert e.value.response.status_code == 400
