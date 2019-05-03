from py42._internal.session_manager import SessionManager
from py42._internal.base_classes import BaseSessionFactory
from py42._internal.login_providers import FileEventLoginProvider
import pytest


class TestSessionManager(object):

    @pytest.fixture
    def session_factory(self, mocker):
        return mocker.MagicMock(spec=BaseSessionFactory)

    @pytest.fixture
    def login_provider(self, mocker):
        return mocker.MagicMock(spec=FileEventLoginProvider)

    def test_get_file_event_session_returns_session(self, session_factory, login_provider):
        session_manager = SessionManager(session_factory)
        session = session_manager.get_file_event_session(login_provider)
        assert session is not None

    def test_get_file_event_session_calls_session_factory_with_login_provider(self, session_factory,
                                                                              login_provider):
        session_manager = SessionManager(session_factory)
        session_manager.get_file_event_session(login_provider)
        session_factory.create_file_event_session.assert_called_with(login_provider)

    def test_get_file_event_session_with_multiple_calls_calls_factory_only_once(self, session_factory, login_provider):
        session_manager = SessionManager(session_factory)
        session_manager.get_file_event_session(login_provider)
        session_manager.get_file_event_session(login_provider)
        session_factory.create_file_event_session.assert_called_once()

    def test_get_file_event_session_with_multiple_calls_returns_same_session(self, session_factory, login_provider):
        session_manager = SessionManager(session_factory)
        session1 = session_manager.get_file_event_session(login_provider)
        session2 = session_manager.get_file_event_session(login_provider)
        assert session1 is session2

    def test_get_file_event_session_raises_exception_when_factory_raises_exception(self, session_factory,
                                                                                   login_provider):
        session_manager = SessionManager(session_factory)

        def mock_create_file_event_session(provider):
            raise Exception("Mock error!")

        session_factory.create_file_event_session.side_effect = mock_create_file_event_session

        with pytest.raises(Exception) as e:
            session_manager.get_file_event_session(login_provider)

        expected_message = "Failed to create or retrieve file event session, caused by: Mock error!"
        assert e.value.args[0] == expected_message
