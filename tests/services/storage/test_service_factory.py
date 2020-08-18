import pytest
from requests.exceptions import HTTPError

from py42.exceptions import Py42HTTPError
from py42.exceptions import Py42StorageSessionInitializationError
from py42.services._connection import Connection
from py42.services.storage._auth import StorageTmpAuth
from py42.services.storage._service_factory import ConnectionManager


@pytest.fixture
def mock_tmp_auth(mocker):
    mock = mocker.MagicMock(spec=StorageTmpAuth)
    mock.get_storage_url.return_value = "testhost.com"
    return mock


class TestStorageSessionManager(object):
    def test_get_storage_session_calls_session_factory_with_token_provider(
        self, mock_tmp_auth
    ):
        storage_session_manager = ConnectionManager()
        connection = storage_session_manager.get_storage_connection(mock_tmp_auth)
        assert type(connection) == Connection

    def test_get_storage_session_with_multiple_calls_returns_same_session(
        self, mock_tmp_auth
    ):
        storage_session_manager = ConnectionManager()
        session1 = storage_session_manager.get_storage_connection(mock_tmp_auth)
        session2 = storage_session_manager.get_storage_connection(mock_tmp_auth)
        assert session1 is session2

    def test_get_storage_session_raises_session_init_error_when_tmp_auth_raises_http_error(
        self, mock_tmp_auth
    ):
        mock_tmp_auth.get_storage_url.side_effect = Py42HTTPError(HTTPError())
        storage_session_manager = ConnectionManager()
        with pytest.raises(Py42StorageSessionInitializationError):
            storage_session_manager.get_storage_connection(mock_tmp_auth)

    def test_get_storage_session_get_saved_session_initially_returns_none(self,):
        storage_session_manager = ConnectionManager()
        assert (
            storage_session_manager.get_saved_connection_for_url("testhost.com") is None
        )

    def test_get_saved_session_returns_session_after_successful_call_to_get_session(
        self, mock_tmp_auth
    ):
        storage_session_manager = ConnectionManager()
        storage_session_manager.get_storage_connection(mock_tmp_auth)
        assert (
            storage_session_manager.get_saved_connection_for_url("testhost.com")
            is not None
        )

# import pytest
# from requests import Session
# from py42._internal.session_factory import AuthHandlerFactory
# from py42._internal.session_factory import SessionFactory
# from py42._internal.session_factory import SessionModifierFactory
# from py42.services._auth import BasicAuthProvider
# from py42.services.storage._auth import FileArchiveTmpAuth, V1Auth
# from py42.services._auth import HeaderModifier
# from py42.services._auth import V3Auth
# TARGET_HOST_ADDRESS = "http://target-host-address.com"
# class TestSessionFactory(object):
#     @pytest.fixture
#     def login_token_provider(self, mocker):
#         provider = mocker.MagicMock(spec=FileArchiveTmpAuth)
#         return provider
#     @pytest.fixture
#     def session_modifier_factory(self, mocker):
#         return mocker.MagicMock(spec=SessionModifierFactory)
#     @pytest.fixture
#     def auth_handler_factory(self, mocker):
#         return mocker.MagicMock(spec=AuthHandlerFactory)
#     def test_create_basic_auth_session_creates_session_with_expected_address(
#         self, session_modifier_factory, auth_handler_factory
#     ):
#         factory = SessionFactory(
#             Session, session_modifier_factory, auth_handler_factory
#         )
#         session = factory.create_basic_auth_session(
#             TARGET_HOST_ADDRESS, u"username", u"password"
#         )
#         assert session.host_address == TARGET_HOST_ADDRESS
#     def test_create_basic_auth_session_uses_auth_handler_with_expected_provider_and_modifier(
#         self, mocker, session_modifier_factory, auth_handler_factory
#     ):
#         modifier = mocker.MagicMock(spec=HeaderModifier)
#         session_modifier_factory.create_header_modifier.return_value = modifier
#         factory = SessionFactory(
#             Session, session_modifier_factory, auth_handler_factory
#         )
#         factory.create_basic_auth_session(TARGET_HOST_ADDRESS, u"username", u"password")
#         provider = auth_handler_factory.create_auth_handler.call_args[0][0]
#         called_modifier = auth_handler_factory.create_auth_handler.call_args[0][1]
#         assert type(provider) == BasicAuthProvider
#         assert modifier == called_modifier
#     def test_create_v1_session_creates_session_with_expected_address(
#         self, session_modifier_factory, auth_handler_factory, mock_connection
#     ):
#         factory = SessionFactory(
#             Session, session_modifier_factory, auth_handler_factory
#         )
#         session = factory.create_v1_session(TARGET_HOST_ADDRESS, mock_connection)
#         assert session.host_address == TARGET_HOST_ADDRESS
#     def test_create_v1_session_uses_auth_handler_with_expected_provider_and_modifier(
#         self, mocker, session_modifier_factory, auth_handler_factory, mock_connection
#     ):
#         modifier = mocker.MagicMock(spec=HeaderModifier)
#         session_modifier_factory.create_header_modifier.return_value = modifier
#         factory = SessionFactory(
#             Session, session_modifier_factory, auth_handler_factory
#         )
#         factory.create_v1_session(TARGET_HOST_ADDRESS, mock_connection)
#         provider = auth_handler_factory.create_auth_handler.call_args[0][0]
#         called_modifier = auth_handler_factory.create_auth_handler.call_args[0][1]
#         assert type(provider) == V1Auth
#         assert modifier == called_modifier
#     def test_create_jwt_session_creates_session_with_expected_address(
#         self, session_modifier_factory, auth_handler_factory, mock_connection
#     ):
#         factory = SessionFactory(
#             Session, session_modifier_factory, auth_handler_factory
#         )
#         session = factory.create_jwt_session(TARGET_HOST_ADDRESS, mock_connection)
#         assert session.host_address == TARGET_HOST_ADDRESS
#     def test_create_jwt_session_uses_auth_handler_with_expected_provider_and_modifier(
#         self, mocker, session_modifier_factory, auth_handler_factory, mock_connection
#     ):
#         modifier = mocker.MagicMock(spec=HeaderModifier)
#         session_modifier_factory.create_header_modifier.return_value = modifier
#         factory = SessionFactory(
#             Session, session_modifier_factory, auth_handler_factory
#         )
#         factory.create_jwt_session(TARGET_HOST_ADDRESS, mock_connection)
#         provider = auth_handler_factory.create_auth_handler.call_args[0][0]
#         called_modifier = auth_handler_factory.create_auth_handler.call_args[0][1]
#         assert type(provider) == V3Auth
#         assert modifier == called_modifier
#     def test_create_storage_session_creates_session_with_expected_address(
#         self, session_modifier_factory, auth_handler_factory, login_token_provider
#     ):
#         factory = SessionFactory(
#             Session, session_modifier_factory, auth_handler_factory
#         )
#         session = factory.create_storage_connection(
#             TARGET_HOST_ADDRESS, login_token_provider
#         )
#         assert session.host_address == TARGET_HOST_ADDRESS
#     def test_create_storage_session_uses_auth_handler_with_expected_provider_and_modifier(
#         self,
#         mocker,
#         session_modifier_factory,
#         auth_handler_factory,
#         login_token_provider,
#     ):
#         modifier = mocker.MagicMock(spec=HeaderModifier)
#         session_modifier_factory.create_header_modifier.return_value = modifier
#         factory = SessionFactory(
#             Session, session_modifier_factory, auth_handler_factory
#         )
#         factory.create_storage_connection(TARGET_HOST_ADDRESS, login_token_provider)
#         provider = auth_handler_factory.create_auth_handler.call_args[0][0]
#         called_modifier = auth_handler_factory.create_auth_handler.call_args[0][1]
#         assert type(provider) == V1Auth
#         assert modifier == called_modifier
#     def test_create_anonymous_session_creates_session_with_expected_address(
#         self, session_modifier_factory, auth_handler_factory
#     ):
#         factory = SessionFactory(
#             Session, session_modifier_factory, auth_handler_factory
#         )
#         session = factory.create_anonymous_session(TARGET_HOST_ADDRESS)
#         assert session.host_address == TARGET_HOST_ADDRESS
#     def test_create_anonymous_session_does_not_use_auth_handler(
#         self, session_modifier_factory, auth_handler_factory
#     ):
#         factory = SessionFactory(
#             Session, session_modifier_factory, auth_handler_factory
#         )
#         factory.create_anonymous_session(TARGET_HOST_ADDRESS)
#         assert auth_handler_factory.create_auth_handler.call_count == 0
