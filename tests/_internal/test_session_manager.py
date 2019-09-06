from py42._internal.session_manager import StorageSessionManager, FileEventSessionManager, SessionsManager
from py42._internal.base_classes import BaseSessionFactory
from py42._internal.login_providers import FileEventLoginProvider
import pytest


def get_session_managers(session_factory):
    return [StorageSessionManager(session_factory),
            FileEventSessionManager(session_factory)]


class TestSessionManager(object):

    @pytest.fixture
    def session_factory(self, mocker):
        return mocker.MagicMock(spec=BaseSessionFactory)

    @pytest.fixture
    def login_provider(self, mocker):
        return mocker.MagicMock(spec=FileEventLoginProvider)

    def test_get_file_event_session_returns_session(self, session_factory, login_provider):
        session_managers = get_session_managers(session_factory)
        sessions_manager = SessionsManager(*session_managers)
        session = sessions_manager.get_file_event_session(login_provider)
        assert session is not None

    def test_get_file_event_session_calls_session_factory_with_login_provider(self, session_factory,
                                                                              login_provider):
        session_managers = get_session_managers(session_factory)
        sessions_manager = SessionsManager(*session_managers)
        sessions_manager.get_file_event_session(login_provider)
        session_factory.create_file_event_session.assert_called_with(login_provider)

    def test_get_file_event_session_with_multiple_calls_calls_factory_only_once(self, session_factory, login_provider):
        session_managers = get_session_managers(session_factory)
        sessions_manager = SessionsManager(*session_managers)
        sessions_manager.get_file_event_session(login_provider)
        sessions_manager.get_file_event_session(login_provider)
        session_factory.create_file_event_session.assert_called_once()

    def test_get_file_event_session_with_multiple_calls_returns_same_session(self, session_factory, login_provider):
        session_managers = get_session_managers(session_factory)
        sessions_manager = SessionsManager(*session_managers)
        session1 = sessions_manager.get_file_event_session(login_provider)
        session2 = sessions_manager.get_file_event_session(login_provider)
        assert session1 is session2

    def test_get_file_event_session_raises_exception_when_factory_raises_exception(self, session_factory,
                                                                                   login_provider):

        def mock_create_file_event_session(provider, **kwargs):
            raise Exception("Mock error!")

        session_factory.create_file_event_session.side_effect = mock_create_file_event_session
        session_managers = get_session_managers(session_factory)
        sessions_manager = SessionsManager(*session_managers)

        with pytest.raises(Exception) as e:
            sessions_manager.get_file_event_session(login_provider)

        expected_message = "Failed to create or retrieve session, caused by: Mock error!"
        assert e.value.args[0] == expected_message
