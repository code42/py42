from threading import Lock

from py42.exceptions import Py42StorageSessionInitializationError
from py42.services._connection import Connection
from py42.services.storage._auth import FileArchiveAuth
from py42.services.storage.archive import StorageArchiveService
from py42.services.storage.exfiltrateddata import ExfiltratedDataService
from py42.services.storage.preservationdata import StoragePreservationDataService
from py42.services.storage.restore import PushRestoreService


class StorageServiceFactory:
    def __init__(self, connection, device_service, connection_manager):
        self._connection = connection
        self._device_service = device_service
        self._connection_manager = connection_manager

    def create_push_restore_service(self, device_guid):
        conn = Connection.from_device_connection(self._connection, device_guid)
        return PushRestoreService(conn)

    def create_archive_service(self, device_guid, destination_guid):
        auth = FileArchiveAuth(self._connection, "my", device_guid, destination_guid)
        conn = self._connection_manager.get_storage_connection(auth)
        return StorageArchiveService(conn)

    def create_preservation_data_service(self, host_address):
        main_connection = self._connection.clone(host_address)
        streaming_connection = Connection.from_host_address(host_address)
        return StoragePreservationDataService(main_connection, streaming_connection)

    def create_exfiltrated_data_service(self, host_address):
        main_connection = self._connection.clone(host_address)
        streaming_connection = Connection.from_host_address(host_address)
        return ExfiltratedDataService(main_connection, streaming_connection)

    def auto_select_destination_guid(self, device_guid):
        response = self._device_service.get_by_guid(
            device_guid, include_backup_usage=True
        )
        # take the first destination guid we find
        destination_list = response["backupUsage"]
        if not destination_list:
            raise Exception(f"No destinations found for device guid: {device_guid}")
        return destination_list[0]["targetComputerGuid"]


class ConnectionManager:
    def __init__(self, session_cache=None):
        self._session_cache = session_cache or {}
        self._list_update_lock = Lock()

    def get_saved_connection_for_url(self, url):
        return self._session_cache.get(url.lower())

    def get_storage_connection(self, storage_auth):
        try:
            url = storage_auth.get_storage_url()
            connection = self.get_saved_connection_for_url(url)
            if connection is None:
                with self._list_update_lock:
                    connection = self.get_saved_connection_for_url(url)
                    if connection is None:
                        connection = Connection.from_host_address(
                            url, auth=storage_auth
                        )
                        self._session_cache[url.lower()] = connection
        except Exception as ex:
            message = f"Failed to create or retrieve connection, caused by: {ex}"
            raise Py42StorageSessionInitializationError(ex, message)
        return connection
