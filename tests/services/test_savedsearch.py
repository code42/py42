import json

from py42.services.fileevent import FileEventService
from py42.services.savedsearch import SavedSearchService

SAVED_SEARCH_GET_RESPONSE = """
    {"searches": [{"groups": [] }]}
"""


class TestSavedSearchClient(object):
    def test_get_calls_get_with_expected_uri(self, mock_connection, py42_response):
        mock_connection.get.return_value = py42_response
        file_event_client = FileEventService(mock_connection)
        saved_search_client = SavedSearchService(mock_connection, file_event_client)
        saved_search_client.get()
        assert mock_connection.get.call_count == 1
        assert (
            mock_connection.get.call_args[0][0]
            == "/forensic-search/queryservice/api/v1/saved"
        )

    def test_get_by_id_calls_get_with_expected_uri(
        self, mock_connection, py42_response
    ):
        mock_connection.get.return_value = py42_response
        file_event_client = FileEventService(mock_connection)
        saved_search_client = SavedSearchService(mock_connection, file_event_client)
        saved_search_client.get_by_id(u"TEst-id")
        assert (
            mock_connection.get.call_args[0][0]
            == "/forensic-search/queryservice/api/v1/saved/TEst-id"
        )

    def test_execute_calls_post_with_expected_uri(self, mock_connection, py42_response):
        py42_response.text = '{u"searches": [{u"groups": []}]}'
        mock_connection.post.return_value = py42_response
        file_event_client = FileEventService(mock_connection)
        saved_search_client = SavedSearchService(mock_connection, file_event_client)
        saved_search_client.execute(u"test-id")
        assert (
            mock_connection.post.call_args[0][0]
            == "/forensic-search/queryservice/api/v1/fileevent"
        )

    def test_execute_calls_post_with_expected_query(
        self, mock_connection, py42_response
    ):
        py42_response.text = SAVED_SEARCH_GET_RESPONSE
        mock_connection.get.return_value = py42_response
        file_event_client = FileEventService(mock_connection)
        saved_search_client = SavedSearchService(mock_connection, file_event_client)
        saved_search_client.execute(u"test-id")
        assert mock_connection.post.call_count == 1
        posted_data = json.loads(mock_connection.post.call_args[1]["data"])
        assert (
            posted_data["pgSize"] == 10000
            and posted_data[u"pgNum"] == 1
            and posted_data[u"groups"] == []
        )

    def test_get_query_calls_get_with_expected_uri(
        self, mock_connection, py42_response
    ):
        py42_response.text = '{u"searches": [{u"groups": []}]}'
        mock_connection.post.return_value = py42_response
        file_event_client = FileEventService(mock_connection)
        saved_search_client = SavedSearchService(mock_connection, file_event_client)
        saved_search_client.get_query(u"test-id")
        assert (
            mock_connection.get.call_args[0][0]
            == "/forensic-search/queryservice/api/v1/saved/test-id"
        )
