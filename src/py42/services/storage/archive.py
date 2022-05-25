from py42.services.storage.restore import RestoreService


class StorageArchiveService(RestoreService):
    def search_paths(
        self,
        session_id,
        device_guid,
        regex=None,
        max_results=None,
        timestamp=None,
        show_deleted=None,
    ):
        # session_id is a web restore session ID (see create_restore_session)
        uri = "/api/v1/WebRestoreSearch"
        params = {
            "webRestoreSessionId": session_id,
            "guid": device_guid,
            "regex": regex,
            "maxResults": max_results,
            "timestamp": timestamp,
            "showDeleted": show_deleted,
        }
        return self._connection.get(uri, params=params)

    def get_file_size(
        self,
        device_guid,
        file_id,
        timestamp=None,
        show_deleted=None,
        backup_set_id=None,
    ):
        uri = "/api/v1/WebRestoreFileSize"
        params = {
            "guid": device_guid,
            "fileId": file_id,
            "timestamp": timestamp,
            "showDeleted": show_deleted,
            "backupSetId": backup_set_id,
        }
        return self._connection.get(uri, params=params)

    def create_file_size_job(
        self,
        device_guid,
        file_id,
        timestamp=None,
        show_deleted=None,
    ):
        uri = "/api/v1/WebRestoreFileSizePolling"
        json_dict = {
            "guid": device_guid,
            "fileId": file_id,
            "timestamp": timestamp,
            "showDeleted": show_deleted,
        }
        return self._connection.post(uri, json=json_dict)

    def get_file_size_job(self, job_id, device_guid):
        uri = "/api/v1/WebRestoreFileSizePolling"
        params = {
            "jobId": job_id,
            "guid": device_guid,
        }
        return self._connection.get(uri, params=params)

    def get_file_path_metadata(
        self,
        session_id,
        device_guid,
        backup_set_id,
        file_id=None,
        timestamp=None,
        show_deleted=None,
        batch_size=None,
        last_batch_file_id=None,
        include_os_metadata=None,
    ):
        # session_id is a web restore session ID (see create_restore_session)
        uri = "/api/v1/WebRestoreTreeNode"
        params = {
            "webRestoreSessionId": session_id,
            "guid": device_guid,
            "backupSetId": backup_set_id,
            "fileId": file_id,
            "timestamp": timestamp,
            "showDeleted": show_deleted,
            "batchSize": batch_size,
            "lastBatchFileId": last_batch_file_id,
            "includeOsMetadata": include_os_metadata,
        }
        return self._connection.get(uri, params=params)

    def start_restore(
        self,
        device_guid,
        web_restore_session_id,
        restore_groups,
        num_files,
        num_dirs,
        num_bytes,
        expire_job=None,
        show_deleted=None,
        restore_full_path=None,
        restore_to_server=None,
    ):
        """Submits a web restore job."""
        uri = "/api/v9/restore/web"
        json_dict = {
            "sourceComputerGuid": device_guid,
            "webRestoreSessionId": web_restore_session_id,
            "restoreGroups": restore_groups,
            "numFiles": num_files,
            "numDirs": num_dirs,
            "numBytes": num_bytes,
            "expireJob": expire_job,
            "showDeleted": show_deleted,
            "restoreFullPath": restore_full_path,
            "restoreToServer": restore_to_server,
        }
        return self._connection.post(uri, json=json_dict)

    def cancel_restore(self, job_id):
        uri = "/api/v1/WebRestoreJob"
        json_dict = {"jobId": job_id}
        return self._connection.delete(uri, json=json_dict)

    def stream_restore_result(self, job_id):
        uri = f"/api/v1/WebRestoreJobResult/{job_id}"
        headers = {"Accept": "application/octet-stream"}
        return self._connection.get(uri, stream=True, headers=headers)
