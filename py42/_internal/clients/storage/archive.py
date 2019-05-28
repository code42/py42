from py42._internal.base_classes import BaseStorageClient
import json


class StorageArchiveClient(BaseStorageClient):

    def search_archive(self, session_id, device_guid, regex=None, max_results=None, timestamp=None, show_deleted=None,
                       **kwargs):
        # session_id is a web restore session ID (see RestoreClient.create_web_restore_session)
        uri = "/api/WebRestoreSearch"
        params = {"webRestoreSessionId": session_id, "guid": device_guid, "regex": regex, "maxResults": max_results,
                  "timestamp": timestamp, "showDeleted": show_deleted}
        return self._session.get(uri, params=params, **kwargs)

    def get_file_size(self, device_guid, file_id, timestamp=None, show_deleted=None, backup_set_id=None, **kwargs):
        uri = "/api/WebRestoreFileSize"
        params = {"guid": device_guid, "fileId": file_id, "timestamp": timestamp, "showDeleted": show_deleted,
                  "backupSetId": backup_set_id}
        return self._session.get(uri, params=params, **kwargs)

    def get_archive_tree_node(self, session_id, device_guid, file_id=None, timestamp=None, show_deleted=None,
                              batch_size=None, last_batch_file_id=None, backup_set_id=None, include_os_metadata=None,
                              **kwargs):
        # session_id is a web restore session ID (see RestoreClient.create_web_restore_session)
        uri = "/api/WebRestoreTreeNode"
        params = {"webRestoreSessionId": session_id, "guid": device_guid, "fileId": file_id, "timestamp": timestamp,
                  "showDeleted": show_deleted, "batchSize": batch_size, "lastBatchFileId": last_batch_file_id,
                  "backupSetId": backup_set_id, "includeOsMetadata": include_os_metadata}
        return self._session.get(uri, params=params, **kwargs)

    def create_web_restore_session(self, device_guid, data_key_token=None, private_password=None, encryption_key=None,
                                   **kwargs):
        """Creates a web restore session.
        See https://console.us.code42.com/apidocviewer/#WebRestoreSession
        """
        uri = "/api/WebRestoreSession"
        json_dict = {"computerGuid": device_guid, "dataKeyToken": data_key_token, "privatePassword": private_password,
                     "encryptionKey": encryption_key}
        return self._session.post(uri, json=json_dict, **kwargs)

    def submit_web_restore_job(self, guid, web_restore_session_id, path_set, num_files, num_dirs, size, zip_result=None,
                               expire_job=None, show_deleted=None, restore_full_path=None, timestamp=None,
                               exceptions=None, backup_set_id=None, **kwargs):
        """Submits a web restore job.
        See https://console.us.code42.com/apidocviewer/#WebRestoreJob-post
        """
        uri = "/api/WebRestoreJob"
        json_dict = {"guid": guid, "webRestoreSessionId": web_restore_session_id, "pathSet": path_set,
                     "numFiles": num_files, "numDirs": num_dirs, "size": size, "zipResult": zip_result,
                     "expireJob": expire_job, "showDeleted": show_deleted, "restoreFullPath": restore_full_path,
                     "timestamp": timestamp, "exceptions": exceptions, "backupSetId": backup_set_id}

        return self._session.post(uri, json=json_dict, **kwargs)

    def get_web_restore_job(self, job_id, **kwargs):
        uri = "/api/WebRestoreJob/{}".format(job_id)
        return self._session.get(uri, **kwargs)

    def cancel_web_restore_job(self, job_id, **kwargs):
        uri = "/api/WebRestoreJob"
        json_dict = {"jobId": job_id}
        return self._session.delete(uri, json=json_dict, **kwargs)

    def get_web_restore_job_result(self, job_id, **kwargs):
        uri = "/api/WebRestoreJobResult/{}".format(job_id)
        return self._session.get(uri, **kwargs)
