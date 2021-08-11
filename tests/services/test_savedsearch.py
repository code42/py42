import pytest
from tests.conftest import create_mock_response

from py42 import settings
from py42.services._connection import Connection
from py42.services.fileevent import FileEventService
from py42.services.savedsearch import SavedSearchService

SAVED_SEARCH_GET_RESPONSE = """
    {"searches": [{"groups": [] }]}
"""
FILE_EVENT_URI = "/forensic-search/queryservice/api/v1/fileevent"


class TestSavedSearchService:
    @pytest.fixture
    def connection(self, mocker):
        return mocker.MagicMock(spec=Connection)

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
            "test-id", page_number=test_custom_page_num,
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

    def test_execute_get_all_calls_post_with_expected_uri(
        self, mock_connection, mocker
    ):
        response = create_mock_response(mocker, SAVED_SEARCH_GET_RESPONSE)
        mock_connection.post.return_value = response
        file_event_service = FileEventService(mock_connection)
        saved_search_service = SavedSearchService(mock_connection, file_event_service)
        saved_search_service.execute_get_all("test-id")
        assert mock_connection.post.call_args[0][0] == FILE_EVENT_URI

    def test_execute_get_all_calls_post_with_expected_query_without_token(
        self, connection
    ):
        file_event_service = FileEventService(connection)
        saved_search_service = SavedSearchService(connection, file_event_service)

        successful_response = {
            "totalCount": None,
            "fileEvents": None,
            "nextPgToken": None,
            "problems": None,
        }
        connection.post.return_value = successful_response

        actual_response = saved_search_service.execute_get_all("test-id")
        expected = {
            "groupClause": "AND",
            "groups": [],
            "srtDir": "asc",
            "srtKey": "eventId",
            "pgToken": "",
            "pgSize": 10000,
        }

        connection.post.assert_called_once_with(FILE_EVENT_URI, json=expected)
        assert actual_response is successful_response

    def test_execute_get_all_calls_post_with_expected_query_with_token(
        self, connection
    ):
        file_event_service = FileEventService(connection)
        saved_search_service = SavedSearchService(connection, file_event_service)

        successful_response = {
            "totalCount": None,
            "fileEvents": None,
            "nextPgToken": "pqr",
            "problems": None,
        }
        connection.post.return_value = successful_response

        actual_response = saved_search_service.execute_get_all("test-id", "abc")
        expected = {
            "groupClause": "AND",
            "groups": [],
            "srtDir": "asc",
            "srtKey": "eventId",
            "pgToken": "abc",
            "pgSize": 10000,
        }

        connection.post.assert_called_once_with(FILE_EVENT_URI, json=expected)
        assert actual_response is successful_response

    def test_execute_get_all_handles_unescaped_quote_chars_in_token(
        self, mock_connection, mocker
    ):
        response = create_mock_response(mocker, SAVED_SEARCH_GET_RESPONSE)
        mock_connection.get.return_value = response
        file_event_service = FileEventService(mock_connection)
        saved_search_service = SavedSearchService(mock_connection, file_event_service)
        unescaped_token = '1234_"abcde"'
        escaped_token = r"1234_\"abcde\""
        saved_search_service.execute_get_all("test-id", unescaped_token)
        expected = {
            "groupClause": "AND",
            "groups": [],
            "srtDir": "asc",
            "srtKey": "eventId",
            "pgToken": escaped_token,
            "pgSize": 10000,
        }
        mock_connection.post.assert_called_once_with(FILE_EVENT_URI, json=expected)

    def test_execute_get_all_handles_escaped_quote_chars_in_token(
        self, mock_connection, mocker
    ):
        response = create_mock_response(mocker, SAVED_SEARCH_GET_RESPONSE)
        mock_connection.get.return_value = response
        file_event_service = FileEventService(mock_connection)
        saved_search_service = SavedSearchService(mock_connection, file_event_service)
        escaped_token = r"1234_\"abcde\""
        saved_search_service.execute_get_all("test-id", escaped_token)
        expected = {
            "groupClause": "AND",
            "groups": [],
            "srtDir": "asc",
            "srtKey": "eventId",
            "pgToken": escaped_token,
            "pgSize": 10000,
        }
        mock_connection.post.assert_called_once_with(FILE_EVENT_URI, json=expected)
