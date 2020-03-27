# -*- coding: utf-8 -*-

import pytest

from py42._internal.session import Py42Session
from py42.clients.file_event import FileEventClient

FILE_EVENT_URI = "/forensic-search/queryservice/api/v1/fileevent"
RAW_QUERY = "RAW JSON QUERY"
RAW_UNICODE_QUERY = u"RAW UNICODE JSON QUERY 我能吞"


class TestFileEventClient(object):
    @pytest.fixture
    def session(self, mocker):
        return mocker.MagicMock(spec=Py42Session)

    def test_search_calls_post_with_uri_and_query(self, session, successful_response):
        client = FileEventClient(session)
        session.post.return_value = successful_response
        client.search(RAW_QUERY)
        session.post.assert_called_once_with(FILE_EVENT_URI, data=RAW_QUERY)

    def test_unicode_query_search_calls_post_with_query(self, session, successful_response):
        client = FileEventClient(session)
        session.post.return_value = successful_response
        client.search(RAW_UNICODE_QUERY)
        session.post.assert_called_once_with(FILE_EVENT_URI, data=RAW_UNICODE_QUERY)
