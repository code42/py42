import json

from py42 import settings
from py42.clients.file_event import FileEventClient
from py42.clients.savedsearch import SavedSearchClient

SAVED_SEARCH_GET_RESPONSE = """
    {"searches": [{"groups": [] }]}
"""


class TestSavedSearchClient(object):
    def test_get_calls_get_with_expected_uri(self, mock_session, py42_response):
        mock_session.get.return_value = py42_response
        file_event_client = FileEventClient(mock_session)
        saved_search_client = SavedSearchClient(mock_session, file_event_client)
        saved_search_client.get()
        assert mock_session.get.call_count == 1
        assert (
            mock_session.get.call_args[0][0]
            == "/forensic-search/queryservice/api/v1/saved"
        )

    def test_get_by_id_calls_get_with_expected_uri(self, mock_session, py42_response):
        mock_session.get.return_value = py42_response
        file_event_client = FileEventClient(mock_session)
        saved_search_client = SavedSearchClient(mock_session, file_event_client)
        saved_search_client.get_by_id(u"TEst-id")
        assert (
            mock_session.get.call_args[0][0]
            == "/forensic-search/queryservice/api/v1/saved/TEst-id"
        )

    def test_execute_calls_post_with_expected_uri(self, mock_session, py42_response):
        py42_response.text = '{u"searches": [{u"groups": []}]}'
        mock_session.post.return_value = py42_response
        file_event_client = FileEventClient(mock_session)
        saved_search_client = SavedSearchClient(mock_session, file_event_client)
        saved_search_client.execute(u"test-id")
        assert (
            mock_session.post.call_args[0][0]
            == "/forensic-search/queryservice/api/v1/fileevent"
        )

    def test_execute_calls_post_with_expected_query(self, mock_session, py42_response):
        py42_response.text = SAVED_SEARCH_GET_RESPONSE
        mock_session.get.return_value = py42_response
        file_event_client = FileEventClient(mock_session)
        saved_search_client = SavedSearchClient(mock_session, file_event_client)
        saved_search_client.execute(u"test-id")
        assert mock_session.post.call_count == 1
        posted_data = json.loads(mock_session.post.call_args[1]["data"])
        assert (
            posted_data[u"pgSize"] == 10000
            and posted_data[u"pgNum"] == 1
            and posted_data[u"groups"] == []
        )

    def test_execute_calls_post_with_expected_page_params(
        self, mock_session, py42_response
    ):
        test_custom_page_num = 2
        settings.security_events_per_page = 5000

        py42_response.text = SAVED_SEARCH_GET_RESPONSE
        mock_session.get.return_value = py42_response
        file_event_client = FileEventClient(mock_session)
        saved_search_client = SavedSearchClient(mock_session, file_event_client)
        saved_search_client.execute(
            u"test-id",
            pg_num=test_custom_page_num,
        )
        assert mock_session.post.call_count == 1
        posted_data = json.loads(mock_session.post.call_args[1]["data"])
        settings.security_events_per_page = 10000
        assert (
            posted_data[u"pgSize"] == 5000
            and posted_data[u"pgNum"] == 2
            and posted_data[u"groups"] == []
        )

    def test_get_query_calls_get_with_expected_uri(self, mock_session, py42_response):
        py42_response.text = '{u"searches": [{u"groups": []}]}'
        mock_session.post.return_value = py42_response
        file_event_client = FileEventClient(mock_session)
        saved_search_client = SavedSearchClient(mock_session, file_event_client)
        saved_search_client.get_query(u"test-id")
        assert (
            mock_session.get.call_args[0][0]
            == "/forensic-search/queryservice/api/v1/saved/test-id"
        )
