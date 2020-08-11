# import pytest
# from py42._internal.session_factory import SessionFactory
# from py42.exceptions import Py42StorageSessionInitializationError
# from py42.services.storage._auth import StorageTmpAuth
# from py42.services._connection_manager import ConnectionManager
# def get_session_managers(session_factory):
#     return [ConnectionManager(session_factory)]
# @pytest.fixture
# def session_factory(mocker):
#     return mocker.MagicMock(spec=SessionFactory)
# @pytest.fixture
# def token_provider(mocker):
#     return mocker.MagicMock(spec=StorageTmpAuth)
# class TestStorageSessionManager(object):
#     def test_get_storage_session_calls_session_factory_with_token_provider(
#         self, session_factory, token_provider
#     ):
#         storage_session_manager = ConnectionManager(session_factory)
#         storage_session_manager.get_storage_connection(token_provider)
#         assert session_factory.create_storage_connection.call_count == 1
#     def test_get_storage_session_with_multiple_calls_calls_factory_only_once(
#         self, session_factory, token_provider
#     ):
#         storage_session_manager = ConnectionManager(session_factory)
#         storage_session_manager.get_storage_connection(token_provider)
#         storage_session_manager.get_storage_connection(token_provider)
#         assert session_factory.create_storage_connection.call_count == 1
#     def test_get_storage_session_with_multiple_calls_returns_same_session(
#         self, session_factory, token_provider
#     ):
#         storage_session_manager = ConnectionManager(session_factory)
#         session1 = storage_session_manager.get_storage_connection(token_provider)
#         session2 = storage_session_manager.get_storage_connection(token_provider)
#         assert session1 is session2
#     def test_get_storage_session_raises_exception_when_factory_raises_exception(
#         self, session_factory, token_provider
#     ):
#         def mock_get_session(host_address, provider, **kwargs):
#             raise Py42StorageSessionInitializationError("Mock error!")
#         storage_session_manager = ConnectionManager(session_factory)
#         session_factory.create_storage_connection.side_effect = mock_get_session
#         with pytest.raises(Exception) as e:
#             storage_session_manager.get_storage_connection(token_provider)
#         expected_message = "Mock error!"
#         assert e.value.args[0] == expected_message
#     def test_get_storage_session_get_saved_session_initially_returns_none(
#         self, session_factory
#     ):
#         storage_session_manager = ConnectionManager(session_factory)
#         assert storage_session_manager.get_saved_connection_for_url("TEST-URI") is None
#     def test_get_saved_session_returns_session_after_successful_call_to_get_session(
#         self, session_factory, token_provider
#     ):
#         storage_session_manager = ConnectionManager(session_factory)
#         token_provider.get_login_info.return_value = {"serverUrl": "TEST-URI"}
#         storage_session_manager.get_storage_connection(token_provider)
#         assert storage_session_manager.get_saved_connection_for_url("TEST-URI") is not None
#     def test_get_storage_session_calls_create_session_only_once_for_given_token_provider(
#         self, session_factory, token_provider, mocker
#     ):
#         storage_session_manager = ConnectionManager(session_factory)
#         storage_session_manager.create_storage_connection = mocker.MagicMock()
#         storage_session_manager.get_storage_connection(token_provider)
#         storage_session_manager.get_storage_connection(token_provider)
#         assert storage_session_manager.create_storage_connection.call_count == 1
#     def test_get_storage_session_calls_get_saved_session_for_url_if_session_already_created(
#         self, session_factory, token_provider, mocker
#     ):
#         storage_session_manager = ConnectionManager(session_factory)
#         storage_session_manager.create_storage_connection = mocker.MagicMock()
#         storage_session_manager.get_storage_connection(token_provider)
#         assert storage_session_manager.create_storage_connection.call_count == 1
#         storage_session_manager.get_saved_connection_for_url = mocker.MagicMock()
#         storage_session_manager.get_storage_connection(token_provider)
#         storage_session_manager.get_storage_connection(token_provider)
#         assert storage_session_manager.get_saved_connection_for_url.call_count == 2
#         # still only called once
#         assert storage_session_manager.create_storage_connection.call_count == 1
