import json

import pytest
from tests.conftest import create_mock_error

from py42.exceptions import Py42BadRequestError
from py42.exceptions import Py42InvalidPageTokenError
from py42.sdk.queries.fileevents.file_event_query import (
    FileEventQuery as FileEventQueryV1,
)
from py42.sdk.queries.fileevents.filters import FileName
from py42.sdk.queries.fileevents.v2.file_event_query import (
    FileEventQuery as FileEventQueryV2,
)
from py42.sdk.queries.fileevents.v2.filters.file import File
from py42.services._connection import Connection
from py42.services.fileevent import FileEventService

FILE_EVENT_URI = "/forensic-search/queryservice/api/v1/fileevent"
FILE_EVENT_URI_V2 = "/forensic-search/queryservice/api/v2/fileevent"


def _create_test_query(test_filename="*"):
    return FileEventQueryV1(FileName.eq(test_filename))


def _create_v2_test_query(test_filename="*"):
    return FileEventQueryV2(File.Name.eq(test_filename))


@pytest.fixture()
def mock_invalid_page_token_connection(mocker, connection):
    connection.post.side_effect = create_mock_error(
        Py42BadRequestError, mocker, "INVALID_PAGE_TOKEN"
    )
    return connection


class TestFileEventService:
    @pytest.fixture
    def connection(self, mocker):
        return mocker.MagicMock(spec=Connection)

    def test_search_calls_post_with_uri_and_query(
        self, connection, successful_response
    ):
        service = FileEventService(connection)
        connection.post.return_value = successful_response
        query = _create_test_query()
        service.search(query)
        connection.post.assert_called_once_with(FILE_EVENT_URI, json=dict(query))

    def test_search_when_given_str_type_query_calls_post_with_uri_and_query(
        self, connection, successful_response
    ):
        service = FileEventService(connection)
        connection.post.return_value = successful_response
        query = str(_create_test_query())
        service.search(query)
        expected = json.loads(query)
        connection.post.assert_called_once_with(FILE_EVENT_URI, json=expected)

    def test_search_when_given_page_token_and_bad_request_with_invalid_page_token_occurs_raises_invalid_page_token_error(
        self, mock_invalid_page_token_connection
    ):
        query = _create_test_query()
        query.page_token = "test_page_token"
        service = FileEventService(mock_invalid_page_token_connection)
        with pytest.raises(Py42InvalidPageTokenError) as err:
            service.search(query)

        assert f'Invalid page token: "{query.page_token}".' in str(err.value)
        assert err.value.page_token == "test_page_token"

    def test_search_when_bad_request_raised_and_token_not_in_query_raises_bad_request(
        self, mock_invalid_page_token_connection
    ):
        query = _create_test_query()
        query.page_token = None
        service = FileEventService(mock_invalid_page_token_connection)
        with pytest.raises(Py42BadRequestError):
            service.search(query)

    def test_search_when_bad_request_raised_with_token_but_has_not_invalid_token_text_raises_bad_request(
        self, mocker, connection
    ):
        connection.post.side_effect = create_mock_error(
            Py42BadRequestError, mocker, "DIFFERENT_ERROR"
        )
        query = _create_test_query()
        query.page_token = "test_page_token"
        service = FileEventService(connection)
        with pytest.raises(Py42BadRequestError):
            service.search(query)

    def test_unicode_query_search_calls_post_with_query(
        self, connection, successful_response
    ):
        service = FileEventService(connection)
        connection.post.return_value = successful_response
        query = _create_test_query("我能吞")
        expected = dict(query)
        service.search(query)
        connection.post.assert_called_once_with(FILE_EVENT_URI, json=expected)

    def test_get_file_location_detail_by_sha256_calls_get_with_hash(
        self, connection, successful_response
    ):
        service = FileEventService(connection)
        connection.get.return_value = successful_response
        service.get_file_location_detail_by_sha256("abc")
        connection.get.assert_called_once_with(
            "/forensic-search/queryservice/api/v1/filelocations",
            params={"sha256": "abc"},
        )

    # V2 TESTS
    def test_search_uses_v2_uri_and_query_if_v2_query(
        self, connection, successful_response
    ):
        service = FileEventService(connection)
        connection.post.return_value = successful_response
        query = _create_v2_test_query()
        service.search(query)
        connection.post.assert_called_once_with(FILE_EVENT_URI_V2, json=dict(query))

    def test_search_when_given_str_type_v2_query_calls_post_with_uri_and_query(
        self, connection, successful_response
    ):
        service = FileEventService(connection)
        connection.post.return_value = successful_response
        query = str(_create_v2_test_query())
        service.search(query)
        expected = json.loads(query)
        connection.post.assert_called_once_with(FILE_EVENT_URI_V2, json=expected)
