import pytest
from requests.exceptions import HTTPError

from py42.exceptions import Py42HTTPError
from py42.exceptions import Py42StorageSessionInitializationError
from py42.services._connection import Connection
from py42.services.devices import DeviceService
from py42.services.storage._auth import StorageTmpAuth
from py42.services.storage._service_factory import ConnectionManager
from py42.services.storage._service_factory import StorageServiceFactory
from py42.services.storage.archive import StorageArchiveService
from py42.services.storage.preservationdata import StoragePreservationDataService
from py42.services.storage.securitydata import StorageSecurityDataService


@pytest.fixture
def mock_tmp_auth(mocker):
    mock = mocker.MagicMock(spec=StorageTmpAuth)
    mock.get_storage_url.return_value = "testhost.com"
    return mock


@pytest.fixture
def mock_device_service(mocker):
    return mocker.MagicMock(spec=DeviceService)


@pytest.fixture
def mock_connection_manager(mocker):
    mock = mocker.MagicMock(spec=ConnectionManager)
    return mock


class TestStorageServiceFactory(object):
    def test_create_archive_service(
        self, mock_successful_connection, mock_device_service, mock_connection_manager
    ):
        factory = StorageServiceFactory(
            mock_successful_connection, mock_device_service, mock_connection_manager
        )
        service = factory.create_archive_service("testguid")
        mock_device_service.get_by_guid.assert_called_once_with(
            "testguid", include_backup_usage=True
        )
        assert type(service) == StorageArchiveService

    def test_create_archive_service_when_given_destination_guid_does_not_call_device_service(
        self, mock_successful_connection, mock_device_service, mock_connection_manager
    ):
        factory = StorageServiceFactory(
            mock_successful_connection, mock_device_service, mock_connection_manager
        )
        service = factory.create_archive_service("testguid")
        mock_device_service.get_by_guid.call_count == 0
        assert type(service) == StorageArchiveService

    def test_create_archive_service_when_device_has_no_destination_raises_exception(
        self,
        mock_successful_connection,
        mock_device_service,
        mock_connection_manager,
        py42_response,
    ):
        factory = StorageServiceFactory(
            mock_successful_connection, mock_device_service, mock_connection_manager
        )
        py42_response.text = '{"backupUsage": []}'
        mock_device_service.get_by_guid.return_value = py42_response
        with pytest.raises(Exception):
            factory.create_archive_service("testguid")

    def test_create_security_data_service(
        self, mock_successful_connection, mock_device_service, mock_connection_manager
    ):
        factory = StorageServiceFactory(
            mock_successful_connection, mock_device_service, mock_connection_manager
        )
        service = factory.create_security_data_service(
            "testplanuid", "testdestinationguid"
        )
        assert type(service) == StorageSecurityDataService

    def test_preservation_data_service(
        self, mock_successful_connection, mock_device_service, mock_connection_manager
    ):
        factory = StorageServiceFactory(
            mock_successful_connection, mock_device_service, mock_connection_manager
        )
        service = factory.create_preservation_data_service("testhost.com")
        assert type(service) == StoragePreservationDataService


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
