from py42.services.casesfileevents import CasesFileEventsService


class TestCasesFileEventService:
    def test_add_event_called_with_expected_url_and_params(self, mock_connection):
        case_file_event_service = CasesFileEventsService(mock_connection)
        case_file_event_service.add_event(123456, "event-id")
        assert (
            mock_connection.post.call_args[0][0]
            == u"/api/v1/case/123456/fileevent/event-id"
        )

    def test_delete_event_called_with_expected_url_and_params(self, mock_connection):
        case_file_event_service = CasesFileEventsService(mock_connection)
        case_file_event_service.delete_event(123456, "event-id")
        assert (
            mock_connection.delete.call_args[0][0]
            == u"/api/v1/case/123456/fileevent/event-id"
        )

    def test_get_event_called_with_expected_url_and_params(self, mock_connection):
        case_file_event_service = CasesFileEventsService(mock_connection)
        case_file_event_service.get_event(123456, "event-id")
        assert (
            mock_connection.get.call_args[0][0]
            == u"/api/v1/case/123456/fileevent/event-id"
        )

    def test_get_all_events_called_with_expected_url_and_params(self, mock_connection):
        case_file_event_service = CasesFileEventsService(mock_connection)
        case_file_event_service.get_all_events(123456)
        assert mock_connection.get.call_args[0][0] == u"/api/v1/case/123456/fileevent/"
