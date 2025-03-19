import pytest
from requests import Session
from tests.conftest import create_mock_response
from tests.conftest import TEST_DEVICE_GUID

from pycpg.exceptions import PycpgError
from pycpg.services._connection import Connection
from pycpg.services.devices import DeviceService
from pycpg.services.storage._service_factory import StorageServiceFactory
from pycpg.services.storage.archive import StorageArchiveService


@pytest.fixture
def mock_device_service(mocker):
    service = mocker.MagicMock(spec=DeviceService)
    response = create_mock_response(
        mocker, '{"backupUsage": [{"targetComputerGuid": "123"}]}'
    )
    service.get_by_guid.return_value = response
    return service


@pytest.fixture
def mock_connection_with_storage_lookup(mocker):
    mock_session = mocker.MagicMock(spec=Session)
    mock_session.headers = {}
    connection = Connection.from_host_address(
        "https://example.com", session=mock_session
    )

    def mock_get(url, params):
        server_url = "{}-{}".format(*params.values())
        if url == "api/v1/WebRestoreInfo":
            return create_mock_response(mocker, f'{{"serverUrl": "{server_url}"}}')
        else:
            return create_mock_response(mocker, "")

    connection.get = mock_get
    return connection


class TestStorageServiceFactory:
    def test_create_archive_service(
        self, mock_connection_with_storage_lookup, mock_device_service
    ):
        factory = StorageServiceFactory(
            mock_connection_with_storage_lookup, mock_device_service
        )
        service = factory.create_archive_service("testguid", None)
        assert type(service) == StorageArchiveService

    def test_create_archive_service_caches_results_for_same_args(
        self, mock_connection_with_storage_lookup, mock_device_service
    ):
        factory = StorageServiceFactory(
            mock_connection_with_storage_lookup, mock_device_service
        )
        service = factory.create_archive_service("123", "456")
        service_2 = factory.create_archive_service("456", "789")
        service_3 = factory.create_archive_service("123", "456")
        assert service._connection.host_address == "https://123-456"
        assert service_2._connection.host_address == "https://456-789"
        assert service._connection is service_3._connection

    def test_create_archive_service_when_given_destination_guid_does_not_call_device_service(
        self, mock_connection_with_storage_lookup, mock_device_service
    ):
        factory = StorageServiceFactory(
            mock_connection_with_storage_lookup, mock_device_service
        )
        service = factory.create_archive_service("testguid", destination_guid=42)
        assert mock_device_service.get_by_guid.call_count == 0
        assert type(service) == StorageArchiveService

    def test_auto_select_destination_guid_when_device_has_no_destination_raises_exception(
        self,
        mock_connection_with_storage_lookup,
        mock_device_service,
        mocker,
    ):
        factory = StorageServiceFactory(
            mock_connection_with_storage_lookup, mock_device_service
        )
        response = create_mock_response(mocker, '{"backupUsage": []}')
        mock_device_service.get_by_guid.return_value = response
        with pytest.raises(PycpgError):
            factory.auto_select_destination_guid(TEST_DEVICE_GUID)