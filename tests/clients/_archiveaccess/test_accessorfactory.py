import pytest
import json

import py42.clients._archiveaccess.restoremanager
from py42.clients._archiveaccess.accessorfactory import ArchiveAccessorFactory
from py42.response import Py42Response
from py42.services.archive import ArchiveService
from py42.services.devices import DeviceService
from py42.services.storage._service_factory import StorageServiceFactory
from py42.clients._archiveaccess import ArchiveAccessor
from tests.clients._archiveaccess.conftest import DEVICE_GUID
from tests.clients._archiveaccess.conftest import DESTINATION_GUID
from tests.clients._archiveaccess.conftest import WEB_RESTORE_SESSION_ID


DATA_KEY_TOKEN = "FAKE_DATA_KEY_TOKEN"
INVALID_DEVICE_GUID = "invalid-device-guid"


@pytest.fixture
def archive_service(mocker):
    client = mocker.MagicMock(spec=ArchiveService)
    py42_response = mocker.MagicMock(spec=Py42Response)
    py42_response.text = '{{"dataKeyToken": "{0}"}}'.format(DATA_KEY_TOKEN)
    py42_response.status_code = 200
    py42_response.encoding = None
    py42_response.__getitem__ = lambda _, key: json.loads(py42_response.text).get(key)
    client.get_data_key_token.return_value = py42_response
    return client


@pytest.fixture
def device_service(mocker):
    return mocker.MagicMock(spec=DeviceService)


@pytest.fixture
def storage_service_factory(mocker, storage_archive_service):
    factory = mocker.MagicMock(spec=StorageServiceFactory)
    factory.create_archive_service.return_value = storage_archive_service
    return factory


class TestArchiveAccessFactory(object):
    def test_archive_accessor_manager_constructor_constructs_successfully(
        self, archive_service, storage_service_factory, device_service,
    ):
        assert ArchiveAccessorFactory(archive_service, storage_service_factory, device_service)

    def test_get_archive_accessor_with_device_guid_and_destination_guid_returns(
        self, archive_service, storage_service_factory, storage_archive_service, device_service
    ):
        storage_service_factory.create_archive_service.return_value = (
            storage_archive_service
        )
        accessor_manager = ArchiveAccessorFactory(
            archive_service, storage_service_factory, device_service
        )
        assert accessor_manager.create_archive_accessor(DEVICE_GUID, accessor_class=ArchiveAccessor)

    def test_get_archive_accessor_calls_storage_service_factory_with_correct_args(
        self, archive_service, storage_service_factory, storage_archive_service, device_service
    ):
        storage_service_factory.create_archive_service.return_value = (
            storage_archive_service
        )
        accessor_manager = ArchiveAccessorFactory(
            archive_service, storage_service_factory, device_service
        )
        accessor_manager.create_archive_accessor(DEVICE_GUID, accessor_class=ArchiveAccessor)
        storage_service_factory.create_archive_service.assert_called_with(
            DEVICE_GUID, destination_guid=None,
        )

    def test_get_archive_accessor_with_opt_dest_guid_calls_storage_service_factory_with_correct_args(
        self, archive_service, storage_service_factory, storage_archive_service, device_service
    ):
        storage_service_factory.create_archive_service.return_value = (
            storage_archive_service
        )
        accessor_manager = ArchiveAccessorFactory(
            archive_service, storage_service_factory, device_service
        )
        accessor_manager.create_archive_accessor(
            DEVICE_GUID, destination_guid=DESTINATION_GUID, accessor_class=ArchiveAccessor,
        )
        storage_service_factory.create_archive_service.assert_called_with(
            DEVICE_GUID, destination_guid=DESTINATION_GUID
        )

    def test_get_archive_accessor_creates_web_restore_session_with_correct_args(
        self, archive_service, storage_service_factory, storage_archive_service, device_service
    ):
        storage_service_factory.create_archive_service.return_value = (
            storage_archive_service
        )
        accessor_manager = ArchiveAccessorFactory(
            archive_service, storage_service_factory, device_service
        )
        accessor_manager.create_archive_accessor(DEVICE_GUID, accessor_class=ArchiveAccessor)

        storage_archive_service.create_restore_session.assert_called_once_with(
            DEVICE_GUID, data_key_token=DATA_KEY_TOKEN
        )

    def test_get_archive_accessor_when_given_private_password_creates_expected_restore_session(
        self, archive_service, storage_service_factory, storage_archive_service, device_service,
    ):
        storage_service_factory.create_archive_service.return_value = (
            storage_archive_service
        )
        accessor_manager = ArchiveAccessorFactory(
            archive_service, storage_service_factory, device_service
        )
        accessor_manager.create_archive_accessor(
            DEVICE_GUID, private_password="TEST_PASSWORD", accessor_class=ArchiveAccessor
        )
        storage_archive_service.create_restore_session.assert_called_once_with(
            DEVICE_GUID, data_key_token=DATA_KEY_TOKEN, private_password="TEST_PASSWORD"
        )

    def test_get_archive_accessor_when_given_encryption_key_creates_expected_restore_session(
        self, archive_service, storage_service_factory, storage_archive_service, device_service
    ):
        storage_service_factory.create_archive_service.return_value = (
            storage_archive_service
        )
        accessor_manager = ArchiveAccessorFactory(
            archive_service, storage_service_factory, device_service
        )
        accessor_manager.create_archive_accessor(DEVICE_GUID, encryption_key="TEST_KEY", accessor_class=ArchiveAccessor)

        storage_archive_service.create_restore_session.assert_called_once_with(
            DEVICE_GUID, encryption_key="TEST_KEY"
        )

    def test_get_archive_accessor_calls_create_restore_job_manager_with_correct_args(
        self, mocker, archive_service, storage_service_factory, storage_archive_service, device_service
    ):
        spy = mocker.spy(py42.clients._archiveaccess.accessorfactory, "create_restore_job_manager")
        storage_service_factory.create_archive_service.return_value = (
            storage_archive_service
        )
        accessor_manager = ArchiveAccessorFactory(
            archive_service, storage_service_factory, device_service
        )
        accessor_manager.create_archive_accessor(DEVICE_GUID, accessor_class=ArchiveAccessor)

        assert spy.call_count == 1
        spy.assert_called_once_with(
            storage_archive_service, DEVICE_GUID, WEB_RESTORE_SESSION_ID
        )

    def test_get_archive_accessor_raises_exception_when_create_backup_client_raises(
        self, archive_service, storage_service_factory, device_service
    ):
        storage_service_factory.create_archive_service.side_effect = Exception(
            "Exception in create_backup_client"
        )
        accessor_manager = ArchiveAccessorFactory(
            archive_service, storage_service_factory, device_service
        )
        with pytest.raises(Exception):
            accessor_manager.create_archive_accessor(INVALID_DEVICE_GUID, accessor_class=ArchiveAccessor)
