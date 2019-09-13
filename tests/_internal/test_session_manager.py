import pytest

from py42._internal.base_classes import BaseSessionFactory
from py42._internal.login_providers import LoginProvider
from py42._internal.session_manager import FileEventSessionManager, SessionsManager, StorageSessionManager


def get_session_managers(session_factory):
    return [StorageSessionManager(session_factory),
            FileEventSessionManager(session_factory)]


@pytest.fixture
def session_factory(mocker):
    return mocker.MagicMock(spec=BaseSessionFactory)


@pytest.fixture
def login_provider(mocker):
    return mocker.MagicMock(spec=LoginProvider)


class TestSessionsManager(object):

    def test_get_file_event_session_returns_session(self, session_factory, login_provider):
        session_managers = get_session_managers(session_factory)
        sessions_manager = SessionsManager(*session_managers)
        session = sessions_manager.get_file_event_session(login_provider)
        assert session is not None

    def test_get_storage_session_returns_session(self, session_factory, login_provider):
        session_managers = get_session_managers(session_factory)
        sessions_manager = SessionsManager(*session_managers)
        session = sessions_manager.get_storage_session(login_provider)
        assert session is not None


class TestFileEventSessionManager(object):

    def test_get_session_calls_session_factory_with_login_provider(self, session_factory, login_provider):
        file_event_session_manager = FileEventSessionManager(session_factory)
        file_event_session_manager.get_session(login_provider)
        session_factory.create_file_event_session.assert_called_with(login_provider)

    def test_get_session_with_multiple_calls_calls_factory_only_once(self, session_factory, login_provider):
        file_event_session_manager = FileEventSessionManager(session_factory)
        file_event_session_manager.get_session(login_provider)
        file_event_session_manager.get_session(login_provider)
        session_factory.create_file_event_session.assert_called_once()

    def test_get_session_with_multiple_calls_returns_same_session(self, session_factory, login_provider):
        file_event_session_manager = FileEventSessionManager(session_factory)
        session1 = file_event_session_manager.get_session(login_provider)
        session2 = file_event_session_manager.get_session(login_provider)
        assert session1 is session2

    def test_get_session_raises_exception_when_factory_raises_exception(self, session_factory, login_provider):

        def mock_create_file_event_session(provider, **kwargs):
            raise Exception("Mock error!")

        file_event_session_manager = FileEventSessionManager(session_factory)
        session_factory.create_file_event_session.side_effect = mock_create_file_event_session

        with pytest.raises(Exception) as e:
            file_event_session_manager.get_session(login_provider)

        expected_message = "Failed to create or retrieve session, caused by: Mock error!"
        assert e.value.args[0] == expected_message


class TestStorageSessionManager(object):

    def test_get_session_calls_session_factory_with_login_provider(self, session_factory, login_provider):
        storage_session_manager = StorageSessionManager(session_factory)
        storage_session_manager.get_session(login_provider)
        session_factory.create_storage_session.assert_called_with(login_provider)

    def test_get_session_with_multiple_calls_calls_factory_only_once(self, session_factory, login_provider):
        storage_session_manager = StorageSessionManager(session_factory)
        storage_session_manager.get_session(login_provider)
        storage_session_manager.get_session(login_provider)
        session_factory.create_storage_session.assert_called_once()

    def test_get_session_with_multiple_calls_returns_same_session(self, session_factory, login_provider):
        storage_session_manager = StorageSessionManager(session_factory)
        session1 = storage_session_manager.get_session(login_provider)
        session2 = storage_session_manager.get_session(login_provider)
        assert session1 is session2

    def test_get_session_raises_exception_when_factory_raises_exception(self, session_factory, login_provider):

        def mock_get_session(provider, **kwargs):
            raise Exception("Mock error!")

        storage_session_manager = StorageSessionManager(session_factory)
        session_factory.create_storage_session.side_effect = mock_get_session

        with pytest.raises(Exception) as e:
            storage_session_manager.get_session(login_provider)

        expected_message = "Failed to create or retrieve session, caused by: Mock error!"
        assert e.value.args[0] == expected_message

    def test_get_session_get_saved_session_initially_returns_none(self, session_factory):
        storage_session_manager = StorageSessionManager(session_factory)
        assert storage_session_manager.get_saved_session_for_url("TEST-URI") is None

    def test_get_saved_session_returns_session_after_successful_call_to_get_session(self, session_factory, login_provider):
        storage_session_manager = StorageSessionManager(session_factory)
        login_provider.get_target_host_address.return_value = "TEST-URI"
        storage_session_manager.get_session(login_provider)
        assert storage_session_manager.get_saved_session_for_url("TEST-URI") is not None

    def test_get_session_calls_create_session_only_once_for_given_login_provider(self, session_factory, login_provider, mocker):
        storage_session_manager = StorageSessionManager(session_factory)
        storage_session_manager.create_session = mocker.MagicMock()
        storage_session_manager.get_session(login_provider)
        storage_session_manager.get_session(login_provider)
        storage_session_manager.create_session.assert_called_once()

    def test_get_session_calls_get_saved_session_for_url_if_session_already_created(self, session_factory, login_provider, mocker):
        storage_session_manager = StorageSessionManager(session_factory)
        storage_session_manager.create_session = mocker.MagicMock()
        storage_session_manager.get_session(login_provider)
        storage_session_manager.create_session.assert_called_once()

        storage_session_manager.get_saved_session_for_url = mocker.MagicMock()
        storage_session_manager.get_session(login_provider)
        storage_session_manager.get_session(login_provider)
        assert storage_session_manager.get_saved_session_for_url.call_count == 2
        # still only called once
        storage_session_manager.create_session.assert_called_once()