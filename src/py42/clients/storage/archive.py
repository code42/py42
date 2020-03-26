from py42.clients import BaseClient


class StorageArchiveClient(BaseClient):
    def search_paths(
        self,
        session_id,
        device_guid,
        regex,
        max_results=None,
        timestamp=None,
        show_deleted=None,
    ):
        """Searches all files from the device with the given GUID during a restore session for a
        filename matching the given regex.
        `REST Documentation <https://console.us.code42.com/apidocviewer/#WebRestoreSearch-get>`__

        Args:
            session_id (str): The ID for the web restore session.
            device_guid (str): The GUID for the device.
            regex (str): A filename regex to search against.
            max_results (int, optional): The max results to return. Defaults to None.
            timestamp (int, optional): The version POSIX timestamp (seconds) of the archive which
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
            timestamp (float, optional): The version POSIX timestamp (seconds) of the file. 0
                indicates the most recent version. It will return the first version on or before
                the given timestamp. Defaults to None.
            show_deleted (bool, optional): Set to True to get the file size of a deleted file.
                Defaults to None.
            backup_set_id (str, optional): The ID of the backup set governing the file to get the
                size of.

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
        """Gets information about the file with the given ID. If the file ID refers to a
        directory, it returns a response containing its child file IDs. If not given `file_id`,
        it returns metadata for the archive's root directory.
        `REST Documentation <https://console.us.code42.com/apidocviewer/#WebRestoreTreeNode-get>`__

        Args:
            session_id (str): The ID for the web restore session.
            device_guid (str): The GUID for the device.
            file_id (str, optional): The ID of the file or directory to get metadata for. When
                None, it uses the root directory. Defaults to None.
            timestamp (float, optional): The version POSIX timestamp (seconds) of the file. 0
                indicates the most recent version. It will return the first version on or before
                the given timestamp. Defaults to None.
            show_deleted (bool, optional): Set to True to get metadata for a deleted file.
                Defaults to None.
            batch_size (int, optional): The number of files to fetch in each batch. Defaults to
                None.
            last_batch_file_id (str, optional): Used for finding the next batch of files. Defaults
                to None.
            backup_set_id (str, optional): The ID of the backup set governing the filepath to get
                metadata for. Defaults to None.
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
        `REST Documentation <https://console.us.code42.com/apidocviewer/#WebRestoreSession-post>`__

        Args:
            device_guid (str): A GUID for the device responsible for the archive in which to
                create a web restore session with.
            data_key_token (str, optional): A token from the method
                :func:`py42.clients.archive.get_data_key_token()` for authorizing the storage
                node to decrypt the archive. Required if not using `encryption_key`. Defaults to
                None.
            private_password (str, optional): An archive password. Required if the archive is
                encrypted with a private password. Defaults to None.
            encryption_key (str, optional): An archive encryption key. Required if the archive is
                encrypted with a custom encryption key. Defaults to None.

        Returns:
            :class:`py42.sdk.response.Py42Response`: A response containing the web restore session
            ID.
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
        device_guid,
        session_id,
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
        `REST Documentation <https://console.us.code42.com/apidocviewer/#WebRestoreJob-post>`__

        Args:
            device_guid (str): A GUID for the device responsible for the archive in which to
                restore from.
            session_id (str): The ID for the web restore session.
            path_set (iter[:class:`py42.clients.storage.archive.RestorePath`]): A list of objects
                representing files and directories that are selected for a restore.
            num_files (int): The number of files anticipated to be restored.
            num_dirs (int): The number of directories anticipated to be restored.
            size (int): The number of bytes that are anticipated to be restored.
            zip_result (bool, optional): If True, it will create a zip file for the files being
                restored for download. Defaults to None.
            expire_job (bool, optional): If True, it will schedule the job to be expired and
                cleaned up after 24 hours. False will not schedule the job to be expired. Defaults
                to None.
            show_deleted (bool, optional): Set to True to include deleted files in the restore.
                Defaults to None.
            restore_full_path (bool, optional): Set to True to restore the entire path. Defaults
                to None.
            timestamp (float, optional): The version POSIX timestamp (seconds) of the file. 0
                indicates the most recent version. It will restore the first version on or before
                the given timestamp. Defaults to None.
            exceptions (iter[:class:`py42.clients.storage.archive.RestoreExclusion`], optional):
                Paths and version timestamps indicating what to exclude during this restore job.
                Defaults to None.
            backup_set_id (str, optional): The ID for the backup set governing the given paths
                for the device with the given GUID on the storage node you are authenticated to.

        Returns:
            :class:`py42.sdk.response.Py42Response`
        """
        uri = u"/api/WebRestoreJob"
        timestamp = timestamp * 1000 if timestamp else timestamp
        path_set = [ps.to_dict() for ps in path_set]
        exceptions = [ex.to_dict() for ex in exceptions]
        json_dict = {
            u"guid": device_guid,
            u"webRestoreSessionId": session_id,
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
        """Gets the status of a restore job.
        `REST Documentation <https://console.us.code42.com/apidocviewer/#WebRestoreJob-get>`__

        Args:
            job_id (str): The ID for the restore job to get the status of.

        Returns:
            :class:`py42.sdk.response.Py42Response`: A response indicating if the job is done yet.
        """
        uri = u"/api/WebRestoreJob/{}".format(job_id)
        return self._session.get(uri)

    def cancel_restore(self, job_id):
        """Cancels a currently-running restore job.
        `REST Documentation <https://console.us.code42.com/apidocviewer/#WebRestoreJob-delete>`__

        Args:
            job_id (str): The ID for the restore job to cancel.

        Returns:
            :class:`py42.sdk.response.Py42Response`
        """
        uri = u"/api/WebRestoreJob"
        json_dict = {u"jobId": job_id}
        return self._session.delete(uri, json=json_dict)

    def stream_restore_result(self, job_id):
        """Streams the result of the restore job as a zipped file. WARNING: If not zipped, it will
        not be able to stream a directory.
        `REST Documentation <https://console.us.code42.com/apidocviewer/#WebRestoreJobResult-get>`__

        Args:
            job_id (str): The ID for the restore job result to stream.

        Returns:
            :class:`py42.sdk.response.Py42Response`
        """
        uri = u"/api/WebRestoreJobResult/{}".format(job_id)
        return self._session.get(uri, stream=True)


class RestorePath(object):
    def __init__(self, path_type, path):
        self._path_type = path_type
        self._path = path

    @property
    def path_type(self):
        """Either 'file', 'directory', or 'version'."""
        return self._path_type

    @property
    def path(self):
        """The path on an archive to a file or directory in which to restore."""
        return self.path

    def to_dict(self):
        """Converts to a dict for putting in a list for the parameter `path_set` on the method
        :func:`py42.clients.storage.archive.StorageArchiveClient.start_restore()`.

        Returns:
            dict: A dict with the type, path, and other required parameters.
        """
        return {u"type": self.path_type, u"path": self.path, u"selected": True}


class RestoreExclusion(object):
    def __init__(self, path, timestamp):
        self._path = path
        self._timestamp = timestamp * 1000

    @property
    def path(self):
        """The path to exclude when doing a restore."""
        return self._path

    @property
    def timestamp(self):
        """The timestamp version of the path to exclude when doing a restore."""
        return self._timestamp

    def to_dict(self):
        """Converts to a dict for putting in a list for the parameter `exceptions` on the method
        :func:`py42.clients.storage.archive.StorageArchiveClient.start_restore()`.

        Returns:
            dict: A dict with the path and timestamp.
        """
        return {u"path": self.path, u"timestamp": self.timestamp}
