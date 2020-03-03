import pytest

from py42._internal.session import Py42Session
from py42._internal.session_factory import SessionFactory


class TestSDKDependencies(object):
    @pytest.fixture
    def mock_session(self, mocker):
        return mocker.MagicMock(spec=Py42Session)

    @pytest.fixture
    def mock_session_factory(self, mocker):
        return mocker.MagicMock(spec=SessionFactory)
