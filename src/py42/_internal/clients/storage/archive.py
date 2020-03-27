from py42.clients import BaseClient


class StorageArchiveClient(BaseClient):
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
        return self._session.get(uri, params=params)

    def get_file_size(
        self, device_guid, file_id, timestamp=None, show_deleted=None, backup_set_id=None
    ):
        uri = u"/api/WebRestoreFileSize"
        params = {
            u"guid": device_guid,
            u"fileId": file_id,
            u"timestamp": timestamp,
            u"showDeleted": show_deleted,
            u"backupSetId": backup_set_id,
        }
        return self._session.get(uri, params=params)

    def get_file_path_metadata(
        self,
        session_id,
        device_guid,
        file_id=None,
        timestamp=None,
        show_deleted=None,
        batch_size=None,
        last_batch_file_id=None,
        backup_set_id=None,
        include_os_metadata=None,
    ):
        # session_id is a web restore session ID (see create_restore_session)
        uri = u"/api/WebRestoreTreeNode"
        params = {
            u"webRestoreSessionId": session_id,
            u"guid": device_guid,
            u"fileId": file_id,
            u"timestamp": timestamp,
            u"showDeleted": show_deleted,
            u"batchSize": batch_size,
            u"lastBatchFileId": last_batch_file_id,
            u"backupSetId": backup_set_id,
            u"includeOsMetadata": include_os_metadata,
        }
        return self._session.get(uri, params=params)

    def create_restore_session(
        self, device_guid, data_key_token=None, private_password=None, encryption_key=None
    ):
        """Creates a web restore session.
        See https://console.us.code42.com/apidocviewer/#WebRestoreSession
        """
        uri = u"/api/WebRestoreSession"
        json_dict = {
            u"computerGuid": device_guid,
            u"dataKeyToken": data_key_token,
            u"privatePassword": private_password,
            u"encryptionKey": encryption_key,
        }
        return self._session.post(uri, json=json_dict)

    def start_restore(
        self,
        guid,
        web_restore_session_id,
        path_set,
        num_files,
        num_dirs,
        size,
        zip_result=None,
        expire_job=None,
        show_deleted=None,
        restore_full_path=None,
        timestamp=None,
        exceptions=None,
        backup_set_id=None,
    ):
        """Submits a web restore job.
        See https://console.us.code42.com/apidocviewer/#WebRestoreJob-post
        """
        uri = u"/api/WebRestoreJob"
        json_dict = {
            u"guid": guid,
            u"webRestoreSessionId": web_restore_session_id,
            u"pathSet": path_set,
            u"numFiles": num_files,
            u"numDirs": num_dirs,
            u"size": size,
            u"zipResult": zip_result,
            u"expireJob": expire_job,
            u"showDeleted": show_deleted,
            u"restoreFullPath": restore_full_path,
            u"timestamp": timestamp,
            u"exceptions": exceptions,
            u"backupSetId": backup_set_id,
        }

        return self._session.post(uri, json=json_dict)

    def get_restore_status(self, job_id):
        uri = u"/api/WebRestoreJob/{}".format(job_id)
        return self._session.get(uri)

    def cancel_restore(self, job_id):
        uri = u"/api/WebRestoreJob"
        json_dict = {u"jobId": job_id}
        return self._session.delete(uri, json=json_dict)

    def stream_restore_result(self, job_id):
        uri = u"/api/WebRestoreJobResult/{}".format(job_id)
        return self._session.get(uri, stream=True)
