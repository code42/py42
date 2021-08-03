from tests.conftest import py42_response

from py42 import settings
from py42.services.fileevent import FileEventService
from py42.services.savedsearch import SavedSearchService

SAVED_SEARCH_GET_RESPONSE = """
    {"searches": [{"groups": [] }]}
"""


class TestSavedSearchService(object):
    def test_get_calls_get_with_expected_uri(self, mock_connection, mocker):
        mock_connection.get.return_value = py42_response(mocker, "{}")
        file_event_service = FileEventService(mock_connection)
        saved_search_service = SavedSearchService(mock_connection, file_event_service)
        saved_search_service.get()
        assert mock_connection.get.call_count == 1
        assert (
            mock_connection.get.call_args[0][0]
            == "/forensic-search/queryservice/api/v1/saved"
        )

    def test_get_by_id_calls_get_with_expected_uri(self, mock_connection, mocker):
        mock_connection.get.return_value = py42_response(mocker, "{}")
        file_event_service = FileEventService(mock_connection)
        saved_search_service = SavedSearchService(mock_connection, file_event_service)
        saved_search_service.get_by_id(u"TEst-id")
        assert (
            mock_connection.get.call_args[0][0]
            == "/forensic-search/queryservice/api/v1/saved/TEst-id"
        )

    def test_execute_calls_post_with_expected_uri(self, mock_connection, mocker):
        response = py42_response(mocker, '{"searches": [{"groups": []}]}')
        mock_connection.post.return_value = response
        file_event_service = FileEventService(mock_connection)
        saved_search_service = SavedSearchService(mock_connection, file_event_service)
        saved_search_service.execute(u"test-id")
        assert (
            mock_connection.post.call_args[0][0]
            == "/forensic-search/queryservice/api/v1/fileevent"
        )

    def test_execute_calls_post_with_expected_query(self, mock_connection, mocker):
        response = py42_response(mocker, SAVED_SEARCH_GET_RESPONSE)
        mock_connection.get.return_value = response
        file_event_service = FileEventService(mock_connection)
        saved_search_service = SavedSearchService(mock_connection, file_event_service)
        saved_search_service.execute(u"test-id")
        assert mock_connection.post.call_count == 1
        posted_data = mock_connection.post.call_args[1]["json"]
        assert (
            posted_data["pgSize"] == 10000
            and posted_data[u"pgNum"] == 1
            and posted_data[u"groups"] == []
        )

    def test_execute_calls_post_with_expected_setting_page_param(
        self, mock_connection, mocker
    ):
        test_custom_page_num = 2
        settings.security_events_per_page = 5000

        response = py42_response(mocker, SAVED_SEARCH_GET_RESPONSE)
        mock_connection.get.return_value = response
        file_event_client = FileEventService(mock_connection)
        saved_search_client = SavedSearchService(mock_connection, file_event_client)
        saved_search_client.execute(
            u"test-id", page_number=test_custom_page_num,
        )
        assert mock_connection.post.call_count == 1
        posted_data = mock_connection.post.call_args[1]["json"]
        settings.security_events_per_page = 10000
        assert (
            posted_data[u"pgSize"] == 5000
            and posted_data[u"pgNum"] == 2
            and posted_data[u"groups"] == []
        )

    def test_execute_calls_post_with_expected_page_params(
        self, mock_connection, mocker
    ):
        test_custom_page_num = 2
        settings.security_events_per_page = 6000
        test_custom_page_size = 5000

        response = py42_response(mocker, SAVED_SEARCH_GET_RESPONSE)
        mock_connection.get.return_value = response
        file_event_client = FileEventService(mock_connection)
        saved_search_client = SavedSearchService(mock_connection, file_event_client)
        saved_search_client.execute(
            u"test-id",
            page_number=test_custom_page_num,
            page_size=test_custom_page_size,
        )
        assert mock_connection.post.call_count == 1
        posted_data = mock_connection.post.call_args[1]["json"]
        settings.security_events_per_page = 10000
        assert (
            posted_data[u"pgSize"] == 5000
            and posted_data[u"pgNum"] == 2
            and posted_data[u"groups"] == []
        )

    def test_get_query_calls_get_with_expected_uri(self, mock_connection, mocker):
        response = py42_response(mocker, '{"searches": [{"groups": []}]}')
        mock_connection.post.return_value = response
        file_event_service = FileEventService(mock_connection)
        saved_search_service = SavedSearchService(mock_connection, file_event_service)
        saved_search_service.get_query(u"test-id")
        assert (
            mock_connection.get.call_args[0][0]
            == "/forensic-search/queryservice/api/v1/saved/test-id"
        )
