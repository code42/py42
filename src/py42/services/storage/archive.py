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
        uri = u"/api/WebRestoreSearch"
        params = {
            u"webRestoreSessionId": session_id,
            u"guid": device_guid,
            u"regex": regex,
            u"maxResults": max_results,
            u"timestamp": timestamp,
            u"showDeleted": show_deleted,
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
        uri = u"/api/WebRestoreFileSize"
        params = {
            u"guid": device_guid,
            u"fileId": file_id,
            u"timestamp": timestamp,
            u"showDeleted": show_deleted,
            u"backupSetId": backup_set_id,
        }
        return self._connection.get(uri, params=params)

    def create_file_size_job(
        self, device_guid, file_id, timestamp=None, show_deleted=None,
    ):
        uri = u"/api/WebRestoreFileSizePolling"
        json_dict = {
            u"guid": device_guid,
            u"fileId": file_id,
            u"timestamp": timestamp,
            u"showDeleted": show_deleted,
        }
        return self._connection.post(uri, json=json_dict)

    def get_file_size_job(self, job_id, device_guid):
        uri = u"/api/WebRestoreFileSizePolling"
        params = {
            u"jobId": job_id,
            u"guid": device_guid,
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
        uri = u"/api/WebRestoreTreeNode"
        params = {
            u"webRestoreSessionId": session_id,
            u"guid": device_guid,
            u"backupSetId": backup_set_id,
            u"fileId": file_id,
            u"timestamp": timestamp,
            u"showDeleted": show_deleted,
            u"batchSize": batch_size,
            u"lastBatchFileId": last_batch_file_id,
            u"includeOsMetadata": include_os_metadata,
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
        uri = u"/api/v9/restore/web"
        json_dict = {
            u"sourceComputerGuid": device_guid,
            u"webRestoreSessionId": web_restore_session_id,
            u"restoreGroups": restore_groups,
            u"numFiles": num_files,
            u"numDirs": num_dirs,
            u"numBytes": num_bytes,
            u"expireJob": expire_job,
            u"showDeleted": show_deleted,
            u"restoreFullPath": restore_full_path,
            u"restoreToServer": restore_to_server,
        }
        return self._connection.post(uri, json=json_dict)

    def cancel_restore(self, job_id):
        uri = u"/api/WebRestoreJob"
        json_dict = {u"jobId": job_id}
        return self._connection.delete(uri, json=json_dict)

    def stream_restore_result(self, job_id):
        uri = u"/api/WebRestoreJobResult/{}".format(job_id)
        headers = {u"Accept": u"application/octet-stream"}
        return self._connection.get(uri, stream=True, headers=headers)
