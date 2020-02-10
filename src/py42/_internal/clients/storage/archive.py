from py42._internal.base_classes import BaseClient


class StorageArchiveClient(BaseClient):
    def search_archive(
        self,
        session_id,
        device_guid,
        regex=None,
        max_results=None,
        timestamp=None,
        show_deleted=None,
    ):
        # session_id is a web restore session ID (see RestoreClient.create_web_restore_session)
        uri = u"/api/WebRestoreSearch"
        params = {
            u"webRestoreSessionId": session_id,
            u"guid": device_guid,
            u"regex": regex,
            u"maxResults": max_results,
            u"timestamp": timestamp,
            u"showDeleted": show_deleted,
        }
        return self._default_session.get(uri, params=params)

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
        return self._default_session.get(uri, params=params)

    def get_archive_tree_node(
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
        # session_id is a web restore session ID (see RestoreClient.create_web_restore_session)
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
        return self._default_session.get(uri, params=params)

    def create_web_restore_session(
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
        return self._default_session.post(uri, json=json_dict)

    def submit_web_restore_job(
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

        return self._default_session.post(uri, json=json_dict)

    def get_web_restore_job(self, job_id):
        uri = u"/api/WebRestoreJob/{}".format(job_id)
        return self._default_session.get(uri)

    def cancel_web_restore_job(self, job_id):
        uri = u"/api/WebRestoreJob"
        json_dict = {u"jobId": job_id}
        return self._default_session.delete(uri, json=json_dict)

    def get_web_restore_job_result(self, job_id):
        uri = u"/api/WebRestoreJobResult/{}".format(job_id)
        return self._default_session.get(uri, stream=True)
