from py42._internal.base_classes import BaseArchiveLocatorFactory
from py42._internal.client_factories import StorageClientFactory
from py42._internal.session_manager import SessionsManager
import pytest

_USER_UID = "user-uid"


@pytest.fixture
def session_manager(mocker):
    return mocker.MagicMock(spec=SessionsManager)


@pytest.fixture
def login_provider_factory(mocker):
    return mocker.MagicMock(spec=BaseArchiveLocatorFactory)


@pytest.fixture
def login_providers(mocker):
    return [mocker.MagicMock(), mocker.MagicMock()]


class TestStorageClientFactory(object):

    def test_create_security_plan_clients_with_get_storage_session_error_still_returns_one_good_session(
            self, mocker, session_manager, login_provider_factory, login_providers):

        login_provider_factory.create_security_archive_locators.return_value = login_providers
        storage_client_factory = StorageClientFactory(session_manager, login_provider_factory)
        session_2 = mocker.MagicMock()

        def get_storage_session_mock(provider):
            if provider == login_providers[0]:
                raise Exception()
            elif provider == login_providers[1]:
                return session_2

        session_manager.get_storage_session.side_effect = get_storage_session_mock

        clients = storage_client_factory.create_security_plan_clients(user_uid=_USER_UID)

        assert len(clients) == 1
        assert clients[0]._session == session_2

    def test_create_security_plan_clients_with_get_storage_session_error_calls_catch_arg_with_exception(
            self, mocker, session_manager, login_provider_factory, login_providers, exception):

        login_provider_factory.create_security_archive_locators.return_value = [login_providers[0]]
        session_manager.get_storage_session.side_effect = exception
        catch = mocker.MagicMock()
        storage_client_factory = StorageClientFactory(session_manager, login_provider_factory)

        storage_client_factory.create_security_plan_clients(user_uid=_USER_UID, catch=catch)

        expected_message = "Error creating storage session. user_uid={0} node_guid={1} exception={2}"
        expected_message = expected_message.format(_USER_UID, login_providers[0].session_cache_key, repr(exception))

        exception = catch.call_args[0][0]  # first and only arg from list of ordered args
        assert type(exception) == Exception
        assert str(exception) == expected_message

    def test_create_security_plan_clients_passes_catch_kwarg_along_to_login_provider_factory(
            self, mocker, session_manager, login_provider_factory, login_providers):

        storage_client_factory = StorageClientFactory(session_manager, login_provider_factory)
        catch = mocker.MagicMock()
        storage_client_factory.create_security_plan_clients(user_uid=_USER_UID, catch=catch)

        create_security_archive_locators_kwargs = login_provider_factory.create_security_archive_locators.call_args[1]
        assert create_security_archive_locators_kwargs["catch"] == catch
