# import pytest

# from py42._internal.client_factories import AuthorityClient
# from py42._internal.client_factories import MicroserviceClientFactory
# from py42._internal.session_factory import SessionFactory
# from py42.services import _key_value_store
# from py42.services import administration
# from py42.services import alerts
# from py42.services import archive
# from py42.services import detectionlists
# from py42.services import devices
# from py42.services import file_event
# from py42.services import legalhold
# from py42.services import orgs
# from py42.services import securitydata
# from py42.services import users
# from py42.services._auth import StorageTokenProviderFactory
# from py42.services._connection_manager import ConnectionManager
# from py42.services.storage import StorageClient
# from py42.services.storage import StorageClientFactory
# from py42.services.users import UserService
# from py42.usercontext import UserContext

# TEST_ROOT_URL = "https://example.com"
# ALERTS_URL = "alerts.example.com"
# FILE_EVENTS_URL = "fileevents.example.com"
# DEPARTING_EMPLOYEE_URL = "departing.example.com"


# @pytest.fixture
# def token_provider_factory(mocker):
#     return mocker.MagicMock(spec=StorageTokenProviderFactory)


# @pytest.fixture
# def storage_session_manager(mocker):
#     return mocker.MagicMock(spec=ConnectionManager)


# @pytest.fixture
# def session_factory(mocker, mock_session):
#     mock_factory = mocker.MagicMock(spec=SessionFactory)
#     mock_env_response = '{"stsBaseUrl": "sts-"}'
#     mock_session.get.return_value.text = mock_env_response
#     mock_factory.create_anonymous_session.return_value = mock_session
#     return mock_factory


# @pytest.fixture
# def user_context(mocker):
#     return mocker.MagicMock(spec=UserContext)


# @pytest.fixture
# def user_client(mocker):
#     return mocker.MagicMock(spec=UserService)


# @pytest.fixture
# def key_value_store_client(mocker):
#     return mocker.MagicMock(spec=_key_value_store.KeyValueStoreClient)


# class TestAuthorityClientFactory(object):
#     def test_create_adminstration_client(self, mock_session):
#         factory = AuthorityClient(mock_session)
#         client = factory.create_administration_client()
#         assert type(client) == administration.AdministrationService

#     def test_create_archive_client(self, mock_session):
#         factory = AuthorityClient(mock_session)
#         client = factory.create_archive_client()
#         assert type(client) == archive.ArchiveService

#     def test_create_device_client(self, mock_session):
#         factory = AuthorityClient(mock_session)
#         client = factory.create_device_client()
#         assert type(client) == devices.DeviceService

#     def test_create_legal_hold_client(self, mock_session):
#         factory = AuthorityClient(mock_session)
#         client = factory.create_legal_hold_client()
#         assert type(client) == legalhold.LegalHoldService

#     def test_create_org_client(self, mock_session):
#         factory = AuthorityClient(mock_session)
#         client = factory.create_org_client()
#         assert type(client) == orgs.OrgService

#     def test_create_security_client(self, mock_session):
#         factory = AuthorityClient(mock_session)
#         client = factory.create_security_client()
#         assert type(client) == securitydata.SecurityDataService

#     def test_create_user_client(self, mock_session):
#         factory = AuthorityClient(mock_session)
#         client = factory.create_user_client()
#         assert type(client) == users.UserService


# class TestStorageClientFactory(object):
#     def test_from_device_guid(self, token_provider_factory, storage_session_manager):
#         factory = StorageClientFactory(storage_session_manager, token_provider_factory)
#         client = factory.from_device_guid("test-device-guid")
#         assert type(client) == StorageClient

#     def test_from_plan_info(self, token_provider_factory, storage_session_manager):
#         factory = StorageClientFactory(storage_session_manager, token_provider_factory)
#         client = factory.from_plan_info("test-plan-uid", "test-dest-guid")
#         assert type(client) == StorageClient


# class TestMicroserviceClientFactory(object):
#     def test_get_alerts_client(
#         self, mock_session, session_factory, user_context, user_client
#     ):
#         factory = MicroserviceClientFactory(
#             TEST_ROOT_URL, mock_session, session_factory, user_context, user_client
#         )
#         client = factory.get_alerts_client()
#         assert type(client) == alerts.AlertService

#     def test_get_alerts_client_calls_get_stored_value_with_expected_key(
#         self,
#         mock_session,
#         session_factory,
#         user_context,
#         user_client,
#         key_value_store_client,
#     ):
#         factory = MicroserviceClientFactory(
#             TEST_ROOT_URL,
#             mock_session,
#             session_factory,
#             user_context,
#             user_client,
#             key_value_store_client,
#         )
#         factory.get_alerts_client()
#         key_value_store_client.get_stored_value.assert_called_once_with(
#             "AlertService-API_URL"
#         )

#     def test_get_alerts_client_creates_client_with_expected_url(
#         self,
#         mock_session,
#         session_factory,
#         user_context,
#         user_client,
#         key_value_store_client,
#     ):
#         key_value_store_client.get_stored_value.return_value.text = ALERTS_URL
#         factory = MicroserviceClientFactory(
#             TEST_ROOT_URL,
#             mock_session,
#             session_factory,
#             user_context,
#             user_client,
#             key_value_store_client,
#         )
#         factory.get_alerts_client()
#         session_factory.create_jwt_session.assert_called_once_with(
#             ALERTS_URL, mock_session
#         )

#     def test_get_alerts_client_returns_same_intance_on_multiple_calls(
#         self, mock_session, session_factory, user_context, user_client
#     ):
#         factory = MicroserviceClientFactory(
#             TEST_ROOT_URL, mock_session, session_factory, user_context, user_client
#         )
#         client1 = factory.get_alerts_client()
#         client2 = factory.get_alerts_client()

#         assert client1 is client2

#     def test_get_departing_employee_client(
#         self, mock_session, session_factory, user_context, user_client
#     ):
#         factory = MicroserviceClientFactory(
#             TEST_ROOT_URL, mock_session, session_factory, user_context, user_client
#         )
#         client = factory.get_departing_employee_client()
#         assert type(client) == detectionlists.departing_employee.DepartingEmployeeService

#     def test_get_departing_employee_client_calls_get_stored_value_with_expected_key(
#         self,
#         mock_session,
#         session_factory,
#         user_context,
#         user_client,
#         key_value_store_client,
#     ):
#         factory = MicroserviceClientFactory(
#             TEST_ROOT_URL,
#             mock_session,
#             session_factory,
#             user_context,
#             user_client,
#             key_value_store_client,
#         )
#         factory.get_departing_employee_client()

#         key_value_store_client.get_stored_value.assert_called_with(
#             "employeecasemanagement-API_URL"
#         )
#         assert key_value_store_client.get_stored_value.call_count == 1

#     def test_get_departing_employee_client_creates_client_with_expected_url(
#         self,
#         mock_session,
#         session_factory,
#         user_context,
#         user_client,
#         key_value_store_client,
#     ):
#         key_value_store_client.get_stored_value.return_value.text = (
#             DEPARTING_EMPLOYEE_URL
#         )
#         factory = MicroserviceClientFactory(
#             TEST_ROOT_URL,
#             mock_session,
#             session_factory,
#             user_context,
#             user_client,
#             key_value_store_client,
#         )
#         factory.get_departing_employee_client()
#         session_factory.create_jwt_session.assert_called_with(
#             DEPARTING_EMPLOYEE_URL, mock_session
#         )
#         assert session_factory.create_jwt_session.call_count == 1

#     def test_get_departing_employee_client_returns_same_intance_on_multiple_calls(
#         self, mock_session, session_factory, user_context, user_client
#     ):
#         factory = MicroserviceClientFactory(
#             TEST_ROOT_URL, mock_session, session_factory, user_context, user_client
#         )
#         client1 = factory.get_departing_employee_client()
#         client2 = factory.get_departing_employee_client()

#         assert client1 is client2

#     def test_get_file_event_client(
#         self, mock_session, session_factory, user_context, user_client
#     ):
#         factory = MicroserviceClientFactory(
#             TEST_ROOT_URL, mock_session, session_factory, user_context, user_client
#         )
#         client = factory.get_file_event_client()
#         assert type(client) == file_event.FileEventService

#     def test_get_file_event_client_calls_get_stored_value_with_expected_key(
#         self,
#         mock_session,
#         session_factory,
#         user_context,
#         user_client,
#         key_value_store_client,
#     ):
#         factory = MicroserviceClientFactory(
#             TEST_ROOT_URL,
#             mock_session,
#             session_factory,
#             user_context,
#             user_client,
#             key_value_store_client,
#         )
#         factory.get_file_event_client()
#         key_value_store_client.get_stored_value.assert_called_once_with(
#             "FORENSIC_SEARCH-API_URL"
#         )

#     def test_get_file_event_client_calls_creates_client_with_expected_url(
#         self,
#         mock_session,
#         session_factory,
#         user_context,
#         user_client,
#         key_value_store_client,
#     ):
#         key_value_store_client.get_stored_value.return_value.text = FILE_EVENTS_URL
#         factory = MicroserviceClientFactory(
#             TEST_ROOT_URL,
#             mock_session,
#             session_factory,
#             user_context,
#             user_client,
#             key_value_store_client,
#         )
#         factory.get_file_event_client()
#         session_factory.create_jwt_session.assert_called_once_with(
#             FILE_EVENTS_URL, mock_session
#         )

#     def test_get_file_event_client_returns_same_intance_on_multiple_calls(
#         self, mock_session, session_factory, user_context, user_client
#     ):
#         factory = MicroserviceClientFactory(
#             TEST_ROOT_URL, mock_session, session_factory, user_context, user_client
#         )
#         client1 = factory.get_file_event_client()
#         client2 = factory.get_file_event_client()

#         assert client1 is client2

#     def test_get_saved_search_client_calls_creates_client_with_expected_url(
#         self,
#         mock_session,
#         key_value_store_client,
#         user_context,
#         user_client,
#         session_factory,
#     ):
#         key_value_store_client.get_stored_value.return_value.text = FILE_EVENTS_URL
#         factory = MicroserviceClientFactory(
#             TEST_ROOT_URL,
#             mock_session,
#             session_factory,
#             user_context,
#             user_client,
#             key_value_store_client,
#         )
#         factory.get_saved_search_client()
#         session_factory.create_jwt_session.assert_called_once_with(
#             FILE_EVENTS_URL, mock_session
#         )

#     def test_create_storage_preservation_client(
#         self, mock_session, user_context, user_client, session_factory
#     ):
#         factory = MicroserviceClientFactory(
#             TEST_ROOT_URL, mock_session, session_factory, user_context, user_client
#         )
#         factory.create_storage_preservation_client("https://host.com")
#         session_factory.create_jwt_session.assert_called_once_with(
#             "https://host.com", mock_session
#         )
#         session_factory.create_anonymous_session.assert_called_once_with(
#             "https://host.com"
#         )
