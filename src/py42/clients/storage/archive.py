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
        """Searches all files for a device with the given GUID during the web restore session with
        the given ID.
        `REST Documentation <https://console.us.code42.com/apidocviewer/#WebRestoreSearch-get>`__

        Args:
            session_id (int): The ID for the web restore session.
            device_guid (str): The GUID for the device.
            regex (str, optional): A filename regex to filter results by. Defaults to None.
            max_results (int, optional): The max results to return. Defaults to None.
            timestamp (int, optional): The POSIX timestamp (seconds) of the archive against which
                to search. 0 indicates the most recent version. It will return all versions older
                than the timestamp you provide. Defaults to None.
            show_deleted (bool, optional): Set to True to include deleted files in the search.
                Defaults to None.

        Returns:
            :class:`py42.sdk.response.Py42Response`
        """
        uri = u"/api/WebRestoreSearch"
        timestamp = timestamp * 1000 if timestamp else timestamp
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
        """Gets the size of the file with the given ID.
        `REST Documentation <https://console.us.code42.com/apidocviewer/#WebRestoreFileSize-get>`__

        Args:
            device_guid (str): A GUID for a device.
            file_id (str): An ID for the file to get the size for.
            timestamp (float, optional): The POSIX timestamp (seconds) of the archive against which
                to search. 0 indicates the most recent version. It will return all versions older
                than the timestamp you provide. Defaults to None.
            show_deleted:
            backup_set_id:

        Returns:
            :class:`py42.sdk.response.Py42Response`: A response containing the file size.
        """
        uri = u"/api/WebRestoreFileSize"
        timestamp = timestamp * 1000 if timestamp else timestamp
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
        """Gets the children of a file or directory in a restore tree. If not given `file_id`, it
        gets metadata for the archive's root directory.
        `REST Documentation <https://console.us.code42.com/apidocviewer/#WebRestoreTreeNode-get>`__

        Args:
            session_id (int): The ID for the web restore session.
            device_guid (str): The GUID for the device.
            file_id (str, optional): The ID of the file or directory to get metadata for. When
                None, it uses the root directory. Defaults to None.
            timestamp (float, optional): The POSIX timestamp (seconds) of the archive against which
                to search. 0 indicates the most recent version. It will return all versions older
                than the timestamp you provide. Defaults to None.
            show_deleted (bool, optional): Set to True to include deleted files in the search.
                Defaults to None.
            batch_size (int, optional): The number of files to fetch in each batch. Defaults to
                None.
            last_batch_file_id (str, optional: Used for finding the next batch of files. Defaults
                to None.
            backup_set_id (str, optional): The ID for the backup set the filepath is a part of.
                Defaults to None.
            include_os_metadata (bool, optional): For Macs, it will add properties
                'sourceBackupDate', 'sourceAccessDate', 'sourceCreationDate',
                'sourceModificationDate', 'sourceChecksum', and 'sourceLength' to the response.
                Defaults to None.

        Returns:
            :class:`py42.sdk.response.Py42Response`
        """
        uri = u"/api/WebRestoreTreeNode"
        timestamp = timestamp * 1000 if timestamp else timestamp
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
