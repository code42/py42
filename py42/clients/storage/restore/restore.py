from py42.clients.storage.storage_base import StorageTargetedClient
import json


class RestoreClient(StorageTargetedClient):

    def create_web_restore_session(self, device_guid, data_key_token=None, private_password=None, encryption_key=None,
                                   **kwargs):
        uri = "/api/WebRestoreSession"
        data = {"computerGuid": device_guid, "dataKeyToken": data_key_token, "privatePassword": private_password,
                "encryptionKey": encryption_key}
        return self.post(uri, data=json.dumps(data), **kwargs)

    def submit_web_restore_job(self, guid, web_restore_session_id, path_set, num_files, num_dirs, size, zip_result=None,
                               expire_job=None, show_deleted=None, restore_full_path=None, timestamp=None,
                               exceptions=None, backup_set_id=None, **kwargs):
        uri = "/api/WebRestoreJob"
        data = {"guid": guid, "webRestoreSessionId": web_restore_session_id, "pathSet": path_set, "numFiles": num_files,
                "numDirs": num_dirs, "size": size, "zipResult": zip_result, "expireJob": expire_job,
                "showDeleted": show_deleted, "restoreFullPath": restore_full_path, "timestamp": timestamp,
                "exceptions": exceptions, "backupSetId": backup_set_id}
        return self.post(uri, data=json.dumps(data), **kwargs)

    def get_web_restore_job(self, job_id, **kwargs):
        uri = "/api/WebRestoreJob/{}".format(job_id)
        return self.get(uri, **kwargs)

    def cancel_web_restore_job(self, job_id, **kwargs):
        uri = "/api/WebRestoreJob"
        data = {"jobId": job_id}
        return self.delete(uri, data=json.dumps(data), **kwargs)

    def get_web_restore_job_result(self, job_id, **kwargs):
        uri = "/api/WebRestoreJobResult/{}".format(job_id)
        return self.get(uri, **kwargs)
