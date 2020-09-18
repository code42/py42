class TestArchiveAccessFactory(object):
    def test_archive_accessor_manager_constructor_constructs_successfully(
        self, archive_client, storage_service_factory
    ):
        assert ArchiveAccessorManager(archive_client, storage_service_factory)

    def test_get_archive_accessor_with_device_guid_and_destination_guid_returns(
        self, archive_client, storage_service_factory, storage_archive_service,
    ):
        storage_service_factory.create_archive_service.return_value = (
            storage_archive_service
        )
        accessor_manager = ArchiveAccessorManager(
            archive_client, storage_service_factory
        )
        assert accessor_manager.create_archive_accessor(DEVICE_GUID)

    def test_get_archive_accessor_calls_storage_service_factory_with_correct_args(
        self, archive_client, storage_service_factory, storage_archive_service,
    ):
        storage_service_factory.create_archive_service.return_value = (
            storage_archive_service
        )
        accessor_manager = ArchiveAccessorManager(
            archive_client, storage_service_factory
        )
        accessor_manager.create_archive_accessor(DEVICE_GUID)
        storage_service_factory.create_archive_service.assert_called_with(
            DEVICE_GUID, destination_guid=None,
        )

    def test_get_archive_accessor_with_opt_dest_guid_calls_storage_service_factory_with_correct_args(
        self, archive_client, storage_service_factory, storage_archive_service,
    ):
        storage_service_factory.create_archive_service.return_value = (
            storage_archive_service
        )
        accessor_manager = ArchiveAccessorManager(
            archive_client, storage_service_factory
        )
        accessor_manager.create_archive_accessor(
            DEVICE_GUID, destination_guid=DESTINATION_GUID
        )
        storage_service_factory.create_archive_service.assert_called_with(
            DEVICE_GUID, destination_guid=DESTINATION_GUID
        )

    def test_get_archive_accessor_creates_web_restore_session_with_correct_args(
        self, archive_client, storage_service_factory, storage_archive_service,
    ):
        storage_service_factory.create_archive_service.return_value = (
            storage_archive_service
        )
        accessor_manager = ArchiveAccessorManager(
            archive_client, storage_service_factory
        )
        accessor_manager.create_archive_accessor(DEVICE_GUID)

        storage_archive_service.create_restore_session.assert_called_once_with(
            DEVICE_GUID, data_key_token=DATA_KEY_TOKEN
        )

    def test_get_archive_accessor_when_given_private_password_creates_expected_restore_session(
        self, archive_client, storage_service_factory, storage_archive_service,
    ):
        storage_service_factory.create_archive_service.return_value = (
            storage_archive_service
        )
        accessor_manager = ArchiveAccessorManager(
            archive_client, storage_service_factory
        )
        accessor_manager.create_archive_accessor(
            DEVICE_GUID, private_password="TEST_PASSWORD"
        )

        storage_archive_service.create_restore_session.assert_called_once_with(
            DEVICE_GUID, data_key_token=DATA_KEY_TOKEN, private_password="TEST_PASSWORD"
        )

    def test_get_archive_accessor_when_given_encryption_key_creates_expected_restore_session(
        self, archive_client, storage_service_factory, storage_archive_service,
    ):
        storage_service_factory.create_archive_service.return_value = (
            storage_archive_service
        )
        accessor_manager = ArchiveAccessorManager(
            archive_client, storage_service_factory
        )
        accessor_manager.create_archive_accessor(DEVICE_GUID, encryption_key="TEST_KEY")

        storage_archive_service.create_restore_session.assert_called_once_with(
            DEVICE_GUID, encryption_key="TEST_KEY"
        )

    def test_get_archive_accessor_calls_create_restore_job_manager_with_correct_args(
        self, mocker, archive_client, storage_service_factory, storage_archive_service,
    ):
        spy = mocker.spy(py42.clients._archive_access, "create_restore_job_manager")
        storage_service_factory.create_archive_service.return_value = (
            storage_archive_service
        )
        accessor_manager = ArchiveAccessorManager(
            archive_client, storage_service_factory
        )
        accessor_manager.create_archive_accessor(DEVICE_GUID)

        assert spy.call_count == 1
        spy.assert_called_once_with(
            storage_archive_service, DEVICE_GUID, WEB_RESTORE_SESSION_ID
        )

    def test_get_archive_accessor_raises_exception_when_create_backup_client_raises(
        self, archive_client, storage_service_factory
    ):
        storage_service_factory.create_archive_service.side_effect = Exception(
            "Exception in create_backup_client"
        )
        accessor_manager = ArchiveAccessorManager(
            archive_client, storage_service_factory
        )
        with pytest.raises(Exception):
            accessor_manager.create_archive_accessor(INVALID_DEVICE_GUID)
