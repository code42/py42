from py42.clients._archiveaccess import ArchiveContentPusher
from py42.clients._archiveaccess.restoremanager import create_file_size_poller
from py42.clients._archiveaccess.restoremanager import create_restore_job_manager


class ArchiveAccessorFactory:
    """Creates different types of :class:`py42.clients._archiveaccess.ArchiveAccessor`
    for use in a web/push restore."""

    def __init__(self, archive_service, storage_service_factory):
        self._archive_service = archive_service
        self._storage_service_factory = storage_service_factory

    def create_archive_accessor(
        self,
        device_guid,
        accessor_class,
        destination_guid=None,
        private_password=None,
        encryption_key=None,
    ):
        """Used for creating instances of ArchiveExplorer or ArchiveContentStreamer.
        Web restore uses this method to create an ArchiveContentStreamer and push
        restore uses create_archive_content_pusher() to create an ArchiveContentPusher
        and this method to create an ArchiveExplorer."""
        destination_guid = (
            destination_guid
            or self._storage_service_factory.auto_select_destination_guid(device_guid)
        )
        storage_archive_service = self._storage_service_factory.create_archive_service(
            device_guid, destination_guid
        )
        (
            decryption_keys,
            session_id,
            restore_job_manager,
            file_size_poller,
        ) = self._create_archive_accessor_dependencies(
            storage_archive_service,
            device_guid,
            private_password,
            encryption_key,
        )
        return accessor_class(
            device_guid,
            session_id,
            destination_guid,
            storage_archive_service,
            restore_job_manager,
            file_size_poller,
        )

    def create_archive_content_pusher(
        self,
        device_guid,
        accepting_guid,
        destination_guid=None,
        private_password=None,
        encryption_key=None,
    ):
        """Creates a class that inherits from the ArchiveAccessor class that has method
        stream_to_device()."""
        push_service = self._storage_service_factory.create_push_restore_service(
            accepting_guid
        )
        (
            decryption_keys,
            session_id,
            restore_job_manager,
            file_size_poller,
        ) = self._create_archive_accessor_dependencies(
            push_service,
            device_guid,
            private_password,
            encryption_key,
        )
        destination_guid = (
            destination_guid
            or self._storage_service_factory.auto_select_destination_guid(device_guid)
        )
        node_guid = self._get_node_guid(device_guid, destination_guid)
        return ArchiveContentPusher(
            device_guid,
            destination_guid,
            node_guid,
            session_id,
            push_service,
            restore_job_manager,
            file_size_poller,
        )

    def _create_archive_accessor_dependencies(
        self, storage_archive_service, device_guid, private_password, encryption_key
    ):
        decryption_keys = self._get_decryption_keys(
            device_guid,
            private_password,
            encryption_key,
        )
        session_id = self._create_restore_session(
            storage_archive_service, device_guid, **decryption_keys
        )
        restore_job_manager = create_restore_job_manager(
            storage_archive_service,
            device_guid,
            session_id,
        )
        file_size_poller = create_file_size_poller(storage_archive_service, device_guid)
        return decryption_keys, session_id, restore_job_manager, file_size_poller

    def _get_decryption_keys(self, device_guid, private_password, encryption_key):
        decryption_keys = {}
        # Favors encryption-key over other security levels.
        if encryption_key:
            decryption_keys["encryption_key"] = encryption_key
        else:
            data_key_token = (
                self._get_data_key_token(device_guid) if not encryption_key else None
            )
            if data_key_token:
                decryption_keys["data_key_token"] = data_key_token
            if private_password:
                decryption_keys["private_password"] = private_password
        return decryption_keys

    def _get_data_key_token(self, device_guid):
        return self._archive_service.get_data_key_token(device_guid)["dataKeyToken"]

    def _get_node_guid(self, device_guid, destination_guid):
        response = self._archive_service.get_web_restore_info(
            device_guid, destination_guid
        )
        return response["nodeGuid"]

    @staticmethod
    def _create_restore_session(session_creator, device_guid, **kwargs):
        """Session creator is :class:`StorageArchiveService` for web restore
        and :class:`PushRestoreService` for push restore."""
        response = session_creator.create_restore_session(device_guid, **kwargs)
        return response["webRestoreSessionId"]
