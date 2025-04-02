import pytest
from tests.conftest import TEST_ACCEPTING_GUID
from tests.conftest import TEST_DATA_KEY_TOKEN
from tests.conftest import TEST_DESTINATION_GUID_1
from tests.conftest import TEST_DEVICE_GUID
from tests.conftest import TEST_ENCRYPTION_KEY
from tests.conftest import TEST_NODE_GUID
from tests.conftest import TEST_PASSWORD
from tests.conftest import TEST_SESSION_ID

import pycpg.clients._archiveaccess.restoremanager
from pycpg.clients._archiveaccess import ArchiveAccessor
from pycpg.clients._archiveaccess.accessorfactory import ArchiveAccessorFactory
from pycpg.services.storage._service_factory import StorageServiceFactory


INVALID_DEVICE_GUID = "invalid-device-guid"


@pytest.fixture
def storage_service_factory(mocker, storage_archive_service):
    factory = mocker.MagicMock(spec=StorageServiceFactory)
    factory.create_archive_service.return_value = storage_archive_service
    factory.auto_select_destination_guid.return_value = TEST_DESTINATION_GUID_1
    return factory


class TestArchiveAccessFactory:
    def test_archive_accessor_manager_constructor_constructs_successfully(
        self, archive_service, storage_service_factory
    ):
        assert ArchiveAccessorFactory(archive_service, storage_service_factory)

    def test_create_archive_accessor_with_device_guid_and_destination_guid_returns(
        self,
        archive_service,
        storage_service_factory,
        storage_archive_service,
    ):
        storage_service_factory.create_archive_service.return_value = (
            storage_archive_service
        )
        accessor_factory = ArchiveAccessorFactory(
            archive_service, storage_service_factory
        )
        assert accessor_factory.create_archive_accessor(
            TEST_DEVICE_GUID, accessor_class=ArchiveAccessor
        )

    def test_create_archive_accessor_calls_storage_service_factory_with_correct_args(
        self,
        archive_service,
        storage_service_factory,
        storage_archive_service,
    ):
        storage_service_factory.create_archive_service.return_value = (
            storage_archive_service
        )
        accessor_factory = ArchiveAccessorFactory(
            archive_service, storage_service_factory
        )
        accessor_factory.create_archive_accessor(TEST_DEVICE_GUID, ArchiveAccessor)
        storage_service_factory.create_archive_service.assert_called_with(
            TEST_DEVICE_GUID,
            TEST_DESTINATION_GUID_1,
        )

    def test_create_archive_accessor_with_opt_dest_guid_calls_storage_service_factory_with_correct_args(
        self,
        archive_service,
        storage_service_factory,
        storage_archive_service,
    ):
        storage_service_factory.create_archive_service.return_value = (
            storage_archive_service
        )
        accessor_factory = ArchiveAccessorFactory(
            archive_service, storage_service_factory
        )
        accessor_factory.create_archive_accessor(
            TEST_DEVICE_GUID,
            ArchiveAccessor,
            TEST_DESTINATION_GUID_1,
        )
        storage_service_factory.create_archive_service.assert_called_with(
            TEST_DEVICE_GUID, TEST_DESTINATION_GUID_1
        )

    def test_create_archive_accessor_creates_web_restore_session_with_correct_args(
        self,
        archive_service,
        storage_service_factory,
        storage_archive_service,
    ):
        storage_service_factory.create_archive_service.return_value = (
            storage_archive_service
        )
        accessor_factory = ArchiveAccessorFactory(
            archive_service, storage_service_factory
        )
        accessor_factory.create_archive_accessor(TEST_DEVICE_GUID, ArchiveAccessor)

        storage_archive_service.create_restore_session.assert_called_once_with(
            TEST_DEVICE_GUID, data_key_token=TEST_DATA_KEY_TOKEN
        )

    def test_create_archive_accessor_when_given_private_password_creates_expected_restore_session(
        self,
        archive_service,
        storage_service_factory,
        storage_archive_service,
    ):
        storage_service_factory.create_archive_service.return_value = (
            storage_archive_service
        )
        accessor_factory = ArchiveAccessorFactory(
            archive_service, storage_service_factory
        )
        accessor_factory.create_archive_accessor(
            TEST_DEVICE_GUID,
            ArchiveAccessor,
            private_password=TEST_PASSWORD,
        )
        storage_archive_service.create_restore_session.assert_called_once_with(
            TEST_DEVICE_GUID,
            data_key_token=TEST_DATA_KEY_TOKEN,
            private_password=TEST_PASSWORD,
        )

    def test_create_archive_accessor_when_given_encryption_key_creates_expected_restore_session(
        self,
        archive_service,
        storage_service_factory,
        storage_archive_service,
    ):
        storage_service_factory.create_archive_service.return_value = (
            storage_archive_service
        )
        accessor_factory = ArchiveAccessorFactory(
            archive_service, storage_service_factory
        )
        accessor_factory.create_archive_accessor(
            TEST_DEVICE_GUID,
            encryption_key=TEST_ENCRYPTION_KEY,
            accessor_class=ArchiveAccessor,
        )

        storage_archive_service.create_restore_session.assert_called_once_with(
            TEST_DEVICE_GUID, encryption_key=TEST_ENCRYPTION_KEY
        )

    def test_create_archive_accessor_calls_create_restore_job_manager_with_correct_args(
        self,
        mocker,
        archive_service,
        storage_service_factory,
        storage_archive_service,
    ):
        spy = mocker.spy(
            pycpg.clients._archiveaccess.accessorfactory, "create_restore_job_manager"
        )
        storage_service_factory.create_archive_service.return_value = (
            storage_archive_service
        )
        accessor_factory = ArchiveAccessorFactory(
            archive_service, storage_service_factory
        )
        accessor_factory.create_archive_accessor(TEST_DEVICE_GUID, ArchiveAccessor)

        assert spy.call_count == 1
        spy.assert_called_once_with(
            storage_archive_service, TEST_DEVICE_GUID, TEST_SESSION_ID
        )

    def test_create_archive_accessor_raises_exception_when_create_backup_client_raises(
        self, archive_service, storage_service_factory
    ):
        storage_service_factory.create_archive_service.side_effect = ValueError(
            "Exception in create_backup_client"
        )
        accessor_factory = ArchiveAccessorFactory(
            archive_service, storage_service_factory
        )
        with pytest.raises(ValueError):
            accessor_factory.create_archive_accessor(
                INVALID_DEVICE_GUID, ArchiveAccessor
            )

    def test_create_archive_accessor_when_given_destination_guid_does_not_auto_select(
        self, archive_service, storage_service_factory
    ):
        accessor_factory = ArchiveAccessorFactory(
            archive_service, storage_service_factory
        )
        accessor_factory.create_archive_accessor(
            TEST_DEVICE_GUID, ArchiveAccessor, TEST_DESTINATION_GUID_1
        )
        storage_service_factory.auto_select_destination_guid.assert_not_called()

    def test_create_archive_content_pusher_creates_push_service_with_accepting_guid(
        self, archive_service, storage_service_factory
    ):
        accessor_factory = ArchiveAccessorFactory(
            archive_service, storage_service_factory
        )
        accessor_factory.create_archive_content_pusher(
            TEST_DEVICE_GUID, TEST_ACCEPTING_GUID
        )
        storage_service_factory.create_push_restore_service.assert_called_once_with(
            TEST_ACCEPTING_GUID
        )

    def test_create_archive_content_push_creates_pusher_with_expected_properties(
        self, archive_service, storage_service_factory
    ):
        accessor_factory = ArchiveAccessorFactory(
            archive_service, storage_service_factory
        )
        pusher = accessor_factory.create_archive_content_pusher(
            TEST_DEVICE_GUID, TEST_ACCEPTING_GUID
        )
        # Set inside device_service mock
        assert pusher.destination_guid == TEST_DESTINATION_GUID_1
        assert pusher._node_guid == TEST_NODE_GUID
