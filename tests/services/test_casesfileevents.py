from py42.services.casesfileevents import CasesFileEventsService

_TEST_CASE_NUMBER = 123456


class TestCasesFileEventService:
    def test_add_event_called_with_expected_url_and_params(self, mock_connection):
        case_file_event_service = CasesFileEventsService(mock_connection)
        case_file_event_service.add_event(_TEST_CASE_NUMBER, "event-id")
        assert mock_connection.post.call_args[0][
            0
        ] == u"/api/v1/case/{}/fileevent/event-id".format(_TEST_CASE_NUMBER)

    def test_delete_event_called_with_expected_url_and_params(self, mock_connection):
        case_file_event_service = CasesFileEventsService(mock_connection)
        case_file_event_service.delete_event(_TEST_CASE_NUMBER, "event-id")
        assert mock_connection.delete.call_args[0][
            0
        ] == u"/api/v1/case/{}/fileevent/event-id".format(_TEST_CASE_NUMBER)

    def test_get_event_called_with_expected_url_and_params(self, mock_connection):
        case_file_event_service = CasesFileEventsService(mock_connection)
        case_file_event_service.get_event(_TEST_CASE_NUMBER, "event-id")
        assert mock_connection.get.call_args[0][
            0
        ] == u"/api/v1/case/{}/fileevent/event-id".format(_TEST_CASE_NUMBER)

    def test_get_all_called_with_expected_url_and_params(self, mock_connection):
        case_file_event_service = CasesFileEventsService(mock_connection)
        case_file_event_service.get_all(_TEST_CASE_NUMBER)
        assert mock_connection.get.call_args[0][
            0
        ] == u"/api/v1/case/{}/fileevent/".format(_TEST_CASE_NUMBER)
