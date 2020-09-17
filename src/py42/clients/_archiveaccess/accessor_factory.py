from py42.clients._archiveaccess import ArchiveAccessor
from py42.clients._archiveaccess.restore_polling import create_file_size_poller
from py42.clients._archiveaccess.restore_polling import create_restore_job_manager


class ArchiveAccessorFactory(object):
    def __init__(self, archive_service, storage_service_factory, devices_service):
        self._archive_service = archive_service
        self._storage_service_factory = storage_service_factory
        self._devices_service = devices_service

    def create_archive_accessor(
        self,
        device_guid,
        destination_guid=None,
        private_password=None,
        encryption_key=None,
    ):
        storage_archive_service = self._storage_service_factory.create_archive_service(
            device_guid, destination_guid=destination_guid
        )
        return self._get_archive_accessor(
            device_guid=device_guid,
            private_password=private_password,
            encryption_key=encryption_key,
            storage_archive_service=storage_archive_service,
        )

    def create_archive_accessor_for_push_restore(
        self,
        device_guid,
        destination_guid,
        private_password=None,
        encryption_key=None
    ):
        factory = self._storage_service_factory
        push_service = factory.create_push_restore_service(
            device_guid
        )
        storage_archive_service = self._storage_service_factory.create_archive_service(
            device_guid, destination_guid=destination_guid
        )
        return self._get_archive_accessor(
            device_guid=device_guid,
            private_password=private_password,
            encryption_key=encryption_key,
            storage_archive_service=push_service,
        )

    def _get_archive_accessor(
        self,
        storage_archive_service,
        device_guid,
        private_password,
        encryption_key,
    ):
        decryption_keys = self._get_decryption_keys(
            device_guid=device_guid,
            private_password=private_password,
            encryption_key=encryption_key,
        )
        session_id = self._create_restore_session(
            storage_archive_service, device_guid, **decryption_keys
        )
        restore_job_manager = create_restore_job_manager(
            archive_service=self._archive_service,
            storage_archive_service=storage_archive_service,
            device_guid=device_guid,
            archive_session_id=session_id,
        )
        file_size_poller = create_file_size_poller(storage_archive_service, device_guid)
        node_guid = self._get_first_node_guid(device_guid)
        return ArchiveAccessor(
            device_guid=device_guid,
            node_guid=node_guid,
            archive_session_id=session_id,
            storage_archive_service=storage_archive_service,
            restore_job_manager=restore_job_manager,
            file_size_poller=file_size_poller,
        )

    def _get_decryption_keys(self, device_guid, private_password, encryption_key):
        decryption_keys = {}
        # Favor encryption-key over other security levels.
        if encryption_key:
            decryption_keys[u"encryption_key"] = encryption_key
        else:
            data_key_token = (
                self._get_data_key_token(device_guid) if not encryption_key else None
            )
            if data_key_token:
                decryption_keys[u"data_key_token"] = data_key_token
            if private_password:
                decryption_keys[u"private_password"] = private_password
        return decryption_keys

    def _get_data_key_token(self, device_guid):
        return self._archive_service.get_data_key_token(device_guid)[u"dataKeyToken"]

    def _get_first_node_guid(self, device_guid):
        response = self._devices_service.get_by_guid(device_guid, include_backup_usage=True)
        backup_usage = response[u"backupUsage"]
        if backup_usage:
            return backup_usage[0][u"serverGuid"]

    @staticmethod
    def _create_restore_session(session_creator, device_guid, **kwargs):
        """Session creator is :class:`StorageArchiveService` for web restore
        and :class:`PushRestoreService` for push restore."""
        response = session_creator.create_restore_session(device_guid, **kwargs)
        return response[u"webRestoreSessionId"]
