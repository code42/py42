# -*- coding: utf-8 -*-
import pytest
from requests import HTTPError
from requests import Response

from py42.exceptions import Py42BadRequestError
from py42.exceptions import Py42InvalidPageTokenError
from py42.sdk.queries.fileevents.file_event_query import FileEventQuery
from py42.sdk.queries.fileevents.filters import FileName
from py42.services._connection import Connection
from py42.services.fileevent import FileEventService

FILE_EVENT_URI = u"/forensic-search/queryservice/api/v1/fileevent"


def _create_test_query(test_filename="*"):
    return FileEventQuery(FileName.eq(test_filename))


@pytest.fixture()
def mock_invalid_page_token_connection(mocker, connection):
    def side_effect(*args, **kwargs):
        http_error = mocker.MagicMock(spec=HTTPError)
        response = mocker.MagicMock(spec=Response)
        response.text = "INVALID_PAGE_TOKEN"
        http_error.response = response
        raise Py42BadRequestError(http_error)

    connection.post.side_effect = side_effect
    return connection


class TestFileEventService(object):
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
        connection.post.assert_called_once_with(FILE_EVENT_URI, data=str(query))

    def test_search_when_given_page_token_and_bad_request_with_invalid_page_token_occurs_raises_invalid_page_token_error(
        self, mock_invalid_page_token_connection
    ):
        query = _create_test_query()
        query.page_token = "test_page_token"
        service = FileEventService(mock_invalid_page_token_connection)
        with pytest.raises(Py42InvalidPageTokenError) as err:
            service.search(query)

        assert str(err.value) == "Invalid page token: {}".format(query.page_token)

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
        def side_effect(*args, **kwargs):
            http_error = mocker.MagicMock(spec=HTTPError)
            response = mocker.MagicMock(spec=Response)
            response.text = "DIFFERENT_ERROR"
            http_error.response = response
            raise Py42BadRequestError(http_error)

        connection.post.side_effect = side_effect
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
        query = _create_test_query(u"我能吞")
        service.search(query)
        connection.post.assert_called_once_with(FILE_EVENT_URI, data=str(query))

    def test_get_file_location_detail_by_sha256_calls_get_with_hash(
        self, connection, successful_response
    ):
        service = FileEventService(connection)
        connection.get.return_value = successful_response
        service.get_file_location_detail_by_sha256("abc")
        connection.get.assert_called_once_with(
            u"/forensic-search/queryservice/api/v1/filelocations",
            params={"sha256": "abc"},
        )
