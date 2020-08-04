# -*- coding: utf-8 -*-
import pytest
from services._connection import Connection

from py42.services.file_event import FileEventService

FILE_EVENT_URI = "/forensic-search/queryservice/api/v1/fileevent"
RAW_QUERY = "RAW JSON QUERY"
RAW_UNICODE_QUERY = u"RAW UNICODE JSON QUERY 我能吞"


class TestFileEventClient(object):
    @pytest.fixture
    def connection(self, mocker):
        return mocker.MagicMock(spec=Connection)

    def test_search_calls_post_with_uri_and_query(
        self, connection, successful_response
    ):
        client = FileEventService(connection)
        connection.post.return_value = successful_response
        client.search(RAW_QUERY)
        connection.post.assert_called_once_with(FILE_EVENT_URI, data=RAW_QUERY)

    def test_unicode_query_search_calls_post_with_query(
        self, connection, successful_response
    ):
        client = FileEventService(connection)
        connection.post.return_value = successful_response
        client.search(RAW_UNICODE_QUERY)
        connection.post.assert_called_once_with(FILE_EVENT_URI, data=RAW_UNICODE_QUERY)

    def test_get_file_location_detail_by_sha256_calls_get_with_hash(
        self, connection, successful_response
    ):
        client = FileEventService(connection)
        connection.get.return_value = successful_response
        client.get_file_location_detail_by_sha256("abc")
        connection.get.assert_called_once_with(
            u"/forensic-search/queryservice/api/v1/filelocations",
            params={"sha256": "abc"},
        )
