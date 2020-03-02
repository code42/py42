import pytest

from py42._internal.login_providers import C42APITmpAuthProvider
from py42._internal.session_factory import SessionFactory
from py42._internal.storage_session_manager import StorageSessionManager


def get_session_managers(session_factory):
    return [StorageSessionManager(session_factory)]


@pytest.fixture
def session_factory(mocker):
    return mocker.MagicMock(spec=SessionFactory)


@pytest.fixture
def login_provider(mocker):
    return mocker.MagicMock(spec=C42APITmpAuthProvider)


class TestStorageSessionManager(object):
    def test_get_storage_session_calls_session_factory_with_login_provider(
        self, session_factory, login_provider
    ):
        storage_session_manager = StorageSessionManager(session_factory)
        storage_session_manager.get_storage_session(login_provider)
        assert session_factory.create_storage_session.call_count == 1

    def test_get_storage_session_with_multiple_calls_calls_factory_only_once(
        self, session_factory, login_provider
    ):
        storage_session_manager = StorageSessionManager(session_factory)
        storage_session_manager.get_storage_session(login_provider)
        storage_session_manager.get_storage_session(login_provider)
        assert session_factory.create_storage_session.call_count == 1

    def test_get_storage_session_with_multiple_calls_returns_same_session(
        self, session_factory, login_provider
    ):
        storage_session_manager = StorageSessionManager(session_factory)
        session1 = storage_session_manager.get_storage_session(login_provider)
        session2 = storage_session_manager.get_storage_session(login_provider)
        assert session1 is session2

    def test_get_storage_session_raises_exception_when_factory_raises_exception(
        self, session_factory, login_provider
    ):
        def mock_get_session(host_address, provider, **kwargs):
            raise Exception("Mock error!")

        storage_session_manager = StorageSessionManager(session_factory)
        session_factory.create_storage_session.side_effect = mock_get_session

        with pytest.raises(Exception) as e:
            storage_session_manager.get_storage_session(login_provider)

        expected_message = "Failed to create or retrieve session, caused by: Mock error!"
        assert e.value.args[0] == expected_message

    def test_get_storage_session_get_saved_session_initially_returns_none(self, session_factory):
        storage_session_manager = StorageSessionManager(session_factory)
        assert storage_session_manager.get_saved_session_for_url("TEST-URI") is None

    # def test_get_saved_session_returns_session_after_successful_call_to_get_session(
    #     self, session_factory, login_provider
    # ):
    #     storage_session_manager = StorageSessionManager(session_factory)
    #     login_provider.get_target_host_address.return_value = "TEST-URI"
    #     storage_session_manager.get_storage_session(login_provider)
    #     assert storage_session_manager.get_saved_session_for_url("TEST-URI") is not None

    def test_get_storage_session_calls_create_session_only_once_for_given_login_provider(
        self, session_factory, login_provider, mocker
    ):
        storage_session_manager = StorageSessionManager(session_factory)
        storage_session_manager.create_storage_session = mocker.MagicMock()
        storage_session_manager.get_storage_session(login_provider)
        storage_session_manager.get_storage_session(login_provider)
        assert storage_session_manager.create_storage_session.call_count == 1

    def test_get_storage_session_calls_get_saved_session_for_url_if_session_already_created(
        self, session_factory, login_provider, mocker
    ):
        storage_session_manager = StorageSessionManager(session_factory)
        storage_session_manager.create_storage_session = mocker.MagicMock()
        storage_session_manager.get_storage_session(login_provider)
        assert storage_session_manager.create_storage_session.call_count == 1

        storage_session_manager.get_saved_session_for_url = mocker.MagicMock()
        storage_session_manager.get_storage_session(login_provider)
        storage_session_manager.get_storage_session(login_provider)
        assert storage_session_manager.get_saved_session_for_url.call_count == 2
        # still only called once
        assert storage_session_manager.create_storage_session.call_count == 1
