import pytest

from py42._internal.session import Py42Session
from py42._internal.clients.fileevent.file_event import FileEventClient


FILE_EVENT_URI = "/forensic-search/queryservice/api/v1/fileevent"
RAW_QUERY = "RAW JSON QUERY"


class TestFileEventClient(object):

    @pytest.fixture
    def session(self, mocker):
        return mocker.MagicMock(spec=Py42Session)

    def test_search_file_events_calls_post_with_uri_and_query(self, session):
        client = FileEventClient(session)
        client.search_file_events(RAW_QUERY)
        session.post.assert_called_with(FILE_EVENT_URI, data=RAW_QUERY)

    def test_search_file_events_calls_post_with_uri_query_and_one_kwarg(self, session):
        client = FileEventClient(session)
        client.search_file_events(RAW_QUERY, arg1="arg1")
        session.post.assert_called_with(FILE_EVENT_URI, arg1="arg1", data=RAW_QUERY)

    def test_search_file_events_calls_post_with_uri_query_and_multiple_kwargs(self, session):
        client = FileEventClient(session)
        client.search_file_events(RAW_QUERY, arg1="arg1", arg2=2)
        session.post.assert_called_with(FILE_EVENT_URI, arg1="arg1", arg2=2, data=RAW_QUERY)
