from tests.conftest import create_mock_response

from py42 import settings
from py42.sdk.queries.fileevents.file_event_query import FileEventQuery
from py42.services.fileevent import FileEventService
from py42.services.savedsearch import SavedSearchService

SAVED_SEARCH_GET_RESPONSE = """
    {"searches": [{"groups": [] }]}
"""
FILE_EVENT_URI = "/forensic-search/queryservice/api/v1/fileevent"


class TestSavedSearchService:
    def test_get_calls_get_with_expected_uri(self, mock_connection, mocker):
        mock_connection.get.return_value = create_mock_response(mocker, "{}")
        file_event_service = FileEventService(mock_connection)
        saved_search_service = SavedSearchService(mock_connection, file_event_service)
        saved_search_service.get()
        assert mock_connection.get.call_count == 1
        assert (
            mock_connection.get.call_args[0][0]
            == "/forensic-search/queryservice/api/v1/saved"
        )

    def test_get_by_id_calls_get_with_expected_uri(self, mock_connection, mocker):
        mock_connection.get.return_value = create_mock_response(mocker, "{}")
        file_event_service = FileEventService(mock_connection)
        saved_search_service = SavedSearchService(mock_connection, file_event_service)
        saved_search_service.get_by_id("test-id")
        assert (
            mock_connection.get.call_args[0][0]
            == "/forensic-search/queryservice/api/v1/saved/test-id"
        )

    def test_execute_calls_post_with_expected_uri(self, mock_connection, mocker):
        response = create_mock_response(mocker, SAVED_SEARCH_GET_RESPONSE)
        mock_connection.post.return_value = response
        file_event_service = FileEventService(mock_connection)
        saved_search_service = SavedSearchService(mock_connection, file_event_service)
        saved_search_service.execute("test-id")
        assert (
            mock_connection.post.call_args[0][0]
            == "/forensic-search/queryservice/api/v1/fileevent"
        )

    def test_execute_calls_post_with_expected_query(self, mock_connection, mocker):
        response = create_mock_response(mocker, SAVED_SEARCH_GET_RESPONSE)
        mock_connection.get.return_value = response
        file_event_service = FileEventService(mock_connection)
        saved_search_service = SavedSearchService(mock_connection, file_event_service)
        saved_search_service.execute("test-id")
        assert mock_connection.post.call_count == 1
        posted_data = mock_connection.post.call_args[1]["json"]
        assert (
            posted_data["pgSize"] == 10000
            and posted_data["pgNum"] == 1
            and posted_data["groups"] == []
        )

    def test_execute_calls_post_with_expected_setting_page_param(
        self, mock_connection, mocker
    ):
        test_custom_page_num = 2
        settings.security_events_per_page = 5000

        response = create_mock_response(mocker, SAVED_SEARCH_GET_RESPONSE)
        mock_connection.get.return_value = response
        file_event_service = FileEventService(mock_connection)
        saved_search_client = SavedSearchService(mock_connection, file_event_service)
        saved_search_client.execute(
            "test-id",
            page_number=test_custom_page_num,
        )
        assert mock_connection.post.call_count == 1
        posted_data = mock_connection.post.call_args[1]["json"]
        settings.security_events_per_page = 10000
        assert (
            posted_data["pgSize"] == 5000
            and posted_data["pgNum"] == 2
            and posted_data["groups"] == []
        )

    def test_execute_calls_post_with_expected_page_params(
        self, mock_connection, mocker
    ):
        test_custom_page_num = 2
        settings.security_events_per_page = 6000
        test_custom_page_size = 5000

        response = create_mock_response(mocker, SAVED_SEARCH_GET_RESPONSE)
        mock_connection.get.return_value = response
        file_event_service = FileEventService(mock_connection)
        saved_search_client = SavedSearchService(mock_connection, file_event_service)
        saved_search_client.execute(
            "test-id",
            page_number=test_custom_page_num,
            page_size=test_custom_page_size,
        )
        assert mock_connection.post.call_count == 1
        posted_data = mock_connection.post.call_args[1]["json"]
        settings.security_events_per_page = 10000
        assert (
            posted_data["pgSize"] == 5000
            and posted_data["pgNum"] == 2
            and posted_data["groups"] == []
        )

    def test_get_query_calls_get_with_expected_uri(self, mock_connection, mocker):
        response = create_mock_response(mocker, SAVED_SEARCH_GET_RESPONSE)
        mock_connection.post.return_value = response
        file_event_service = FileEventService(mock_connection)
        saved_search_service = SavedSearchService(mock_connection, file_event_service)
        saved_search_service.get_query("test-id")
        assert (
            mock_connection.get.call_args[0][0]
            == "/forensic-search/queryservice/api/v1/saved/test-id"
        )

    # V2 TESTS
    def test_get_calls_with_v2_uri_if_v2_settings_enabled(
        self, mock_connection, mocker
    ):
        import py42.settings

        py42.settings.use_v2_file_event_data = True
        file_event_service = FileEventService(mock_connection)
        saved_search_service = SavedSearchService(mock_connection, file_event_service)
        saved_search_service.get()
        py42.settings.use_v2_file_event_data = False
        mock_connection.get.assert_called_once_with(
            "/forensic-search/queryservice/api/v2/saved"
        )

    def test_get_by_id_calls_v2_uri_if_v2_settings_enabled(self, mock_connection):
        import py42.settings

        py42.settings.use_v2_file_event_data = True
        file_event_service = FileEventService(mock_connection)
        saved_search_service = SavedSearchService(mock_connection, file_event_service)
        saved_search_service.get_by_id("test-id")
        py42.settings.use_v2_file_event_data = False
        mock_connection.get.assert_called_once_with(
            "/forensic-search/queryservice/api/v2/saved/test-id"
        )

    def test_get_query_builds_v2_query_if_v2_settings_enabled(
        self, mock_connection, mocker
    ):
        import py42.settings

        py42.settings.use_v2_file_event_data = True
        response = create_mock_response(mocker, SAVED_SEARCH_GET_RESPONSE)
        mock_connection.post.return_value = response
        file_event_service = FileEventService(mock_connection)
        saved_search_service = SavedSearchService(mock_connection, file_event_service)
        query = saved_search_service.get_query("test-id")
        py42.settings.use_v2_file_event_data = False
        assert query.sort_key == "event.id"

    def test_execute_calls_search_with_v2_uri_if_v2_settings_enabled(
        self, mock_connection, mocker
    ):
        import py42.settings

        py42.settings.use_v2_file_event_data = True

        response = create_mock_response(mocker, SAVED_SEARCH_GET_RESPONSE)
        mock_connection.post.return_value = response

        file_event_service = FileEventService(mock_connection)
        saved_search_service = SavedSearchService(mock_connection, file_event_service)
        saved_search_service.execute("test-id")
        expected_query = FileEventQuery.from_dict({"groups": []})
        py42.settings.use_v2_file_event_data = False
        mock_connection.post.assert_called_once_with(
            "/forensic-search/queryservice/api/v2/fileevent", json=dict(expected_query)
        )
