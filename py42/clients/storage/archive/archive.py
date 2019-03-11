from py42.clients.storage.storage_base import StorageTargetedClient


class ArchiveClient(StorageTargetedClient):

    def search_archive(self, session_id, device_guid, regex=None, max_results=None, timestamp=None, show_deleted=None,
                       **kwargs):
        # session_id is a web restore session ID (see RestoreClient.create_web_restore_session)
        uri = "/api/WebRestoreSearch"
        params = {"webRestoreSessionId": session_id, "guid": device_guid, "regex": regex, "maxResults": max_results,
                  "timestamp": timestamp, "showDeleted": show_deleted}
        return self.get(uri, params=params, **kwargs)

    def get_file_size(self, device_guid, file_id, timestamp=None, show_deleted=None, backup_set_id=None, **kwargs):
        uri = "/api/WebRestoreFileSize"
        params = {"guid": device_guid, "fileId": file_id, "timestamp": timestamp, "showDeleted": show_deleted,
                  "backupSetId": backup_set_id}
        return self.get(uri, params=params, **kwargs)

    def get_archive_tree_node(self, session_id, device_guid, file_id=None, timestamp=None, show_deleted=None,
                              batch_size=None, last_batch_file_id=None, backup_set_id=None, include_os_metadata=None,
                              **kwargs):
        # session_id is a web restore session ID (see RestoreClient.create_web_restore_session)
        uri = "/api/WebRestoreTreeNode"
        params = {"webRestoreSessionId": session_id, "guid": device_guid, "fileId": file_id, "timestamp": timestamp,
                  "showDeleted": show_deleted, "batchSize": batch_size, "lastBatchFileId": last_batch_file_id,
                  "backupSetId": backup_set_id, "includeOsMetadata": include_os_metadata}
        return self.get(uri, params=params, **kwargs)
