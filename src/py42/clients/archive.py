from py42.clients._archiveaccess import ArchiveContentStreamer
from py42.clients._archiveaccess import ArchiveExplorer
from py42.exceptions import Py42Error


_FILE_SIZE_CALC_TIMEOUT = 10
_DEFAULT_BACKUP_SET_ID = "1"


class ArchiveClient:
    """A module for getting information about backup archives on storage nodes along with
    functionality for streaming a file from backup.
    """

    def __init__(self, archive_accessor_factory, archive_service):
        self._archive_accessor_factory = archive_accessor_factory
        self._archive_service = archive_service

    def get_by_archive_guid(self, archive_guid):
        """Gets single archive information by GUID.

        Args:
            archive_guid (str): The GUID for the archive.

        Returns:
            :class:`py42.response.Py42Response`: A response containing archive
            information.
        """
        return self._archive_service.get_single_archive(archive_guid)

    def get_all_by_device_guid(self, device_guid):
        """Gets archive information for a device.

        Args:
            device_guid (str): The GUID for the device.

        Returns:
            generator: An object that iterates over :class:`py42.response.Py42Response`
            objects that each contain a page of archives.
        """
        return self._archive_service.get_all_archives_from_value(
            device_guid, "backupSourceGuid"
        )

    def stream_from_backup(
        self,
        file_paths,
        device_guid,
        destination_guid=None,
        archive_password=None,
        encryption_key=None,
        show_deleted=None,
        file_size_calc_timeout=_FILE_SIZE_CALC_TIMEOUT,
        backup_set_id=None,
    ):
        """Streams a file from a backup archive to memory. This method uses the same endpoint
        as restoring from Console and therefore has all the same considerations.

        `Support Documentation <https://support.code42.com/Administrator/Cloud/Monitoring_and_managing/Restore_files_from_the_Code42_console#Troubleshooting>`__

        Args:
            file_paths (str or list of str): The path or list of paths to the files or directories in
                the archive.
            device_guid (str): The GUID of the device the file belongs to.
            destination_guid (str, optional): The GUID of the destination that stores the backup
                of the file. If None, it will use the first destination GUID it finds for your
                device. 'destination_guid' may be useful if the file is missing from one of your
                destinations or if you want to optimize performance. Defaults to None.
            archive_password (str or None, optional): The password for the archive, if password-
                protected. This is only relevant to users with archive key password security. Defaults
                to None.
            encryption_key (str or None, optional): A custom encryption key for decrypting an archive's
                file contents, necessary for restoring files. This is only relevant to users with custom
                key archive security. Defaults to None.
            show_deleted (bool, optional): Set to True to include deleted files when restoring a directory.
                Defaults to None.
            file_size_calc_timeout (int, optional): Set to limit the amount of seconds spent calculating
                file sizes when crafting the request. Set to 0 or None to ignore file sizes altogether.
                Defaults to 10.
            backup_set_id (str, optional): The ID of the backup set restore from (only useful for V3 archives).
                If not supplied, the default backup set (id=1) will be used if it exists, otherwise
                the first in the list of existing backup sets will be used.

        Returns:
            :class:`py42.response.Py42Response`: A response containing the streamed content.

        Usage example::

            stream_response = sdk.archive.stream_from_backup("/full/path/to/file.txt", "1234567890")
            with open("/path/to/save/file/to", "wb") as f:
                for chunk in stream_response.iter_content(chunk_size=128):
                    if chunk:
                        f.write(chunk)

        In certain cases, you will have to unzip the results::

            import zipfile
            with zipfile.ZipFile("downloaded_directory.zip", "r") as zf:
                zf.extractall(".")
        """
        archive_accessor = self._archive_accessor_factory.create_archive_accessor(
            device_guid,
            ArchiveContentStreamer,
            destination_guid=destination_guid,
            private_password=archive_password,
            encryption_key=encryption_key,
        )
        backup_set_id = self._select_backup_set_id(
            device_guid, archive_accessor.destination_guid, backup_set_id
        )
        return archive_accessor.stream_from_backup(
            backup_set_id,
            file_paths,
            file_size_calc_timeout=file_size_calc_timeout,
            show_deleted=show_deleted,
        )

    def stream_to_device(
        self,
        file_paths,
        device_guid,
        accepting_device_guid,
        restore_path,
        destination_guid=None,
        archive_password=None,
        encryption_key=None,
        show_deleted=None,
        overwrite_existing_files=False,
        file_size_calc_timeout=_FILE_SIZE_CALC_TIMEOUT,
        backup_set_id=None,
    ):
        """Streams a file from a backup archive to a specified device.

        Args:
            file_paths (str or list of str): The path or list of paths to the files or directories in
                the archive.
            device_guid (str): The GUID of the device the file belongs to.
            accepting_device_guid (str): The GUID of the device accepting the restore.
            restore_path (str, optional): The path on the accepting device where the restore will be
                saved. Alternatively, pass in the value ``ORIGINAL_LOCATION`` to restore the file
                to the original location, which may be the case if you are replacing a device.
            destination_guid (str, optional): The GUID of the destination that stores the backup
                of the file. If None, it will use the first destination GUID it finds for your
                device. 'destination_guid' may be useful if the file is missing from one of your
                destinations or if you want to optimize performance. Defaults to None.
            archive_password (str or None, optional): The password for the archive, if password-
                protected. This is only relevant to users with archive key password security. Defaults
                to None.
            encryption_key (str or None, optional): A custom encryption key for decrypting an archive's
                file contents, necessary for restoring files. This is only relevant to users with custom
                key archive security. Defaults to None.
            show_deleted (bool, optional): Set to True to include deleted files when restoring a directory.
                Defaults to None.
            overwrite_existing_files (bool, optional): to overwrite any existing files with the restored
                data. If False (the default), any existing files that match a path being restored will
                first get renamed.
            file_size_calc_timeout (int, optional): Set to limit the amount of seconds spent calculating
                file sizes when crafting the request. Set to 0 or None to ignore file sizes altogether.
                Defaults to 10.
            backup_set_id (str, optional): The ID of the backup set restore from (only useful for V3 archives).
                If not supplied, the default backup set (id=1) will be used if it exists, otherwise
                the first in the list of existing backup sets will be used.

        Returns:
            :class:`py42.response.Py42Response`.
        """
        explorer = self._archive_accessor_factory.create_archive_accessor(
            device_guid,
            ArchiveExplorer,
            destination_guid=destination_guid,
            private_password=archive_password,
            encryption_key=encryption_key,
        )
        backup_set_id = self._select_backup_set_id(
            device_guid, explorer.destination_guid, backup_set_id
        )
        file_selections = explorer.create_file_selections(
            backup_set_id, file_paths, file_size_calc_timeout
        )
        pusher = self._archive_accessor_factory.create_archive_content_pusher(
            device_guid,
            accepting_device_guid,
            private_password=archive_password,
            encryption_key=encryption_key,
            destination_guid=explorer.destination_guid,
        )
        return pusher.stream_to_device(
            restore_path,
            accepting_device_guid,
            file_selections,
            backup_set_id,
            show_deleted,
            overwrite_existing_files,
        )

    def _select_backup_set_id(self, device_guid, destination_guid, backup_set_id):
        backup_sets = self.get_backup_sets(device_guid, destination_guid)["backupSets"]
        backup_set_ids = [bs["backupSetId"] for bs in backup_sets]
        if backup_set_id:
            if backup_set_id not in backup_set_ids:
                raise Py42Error(
                    f"backup_set_id={backup_set_id} not found in device backup sets: {backup_sets}"
                )
            return backup_set_id
        # id=1 is the "default" backup set, use this if it exists and no explicit id
        # is provided by user
        elif "1" in backup_set_ids:
            return "1"
        elif len(backup_set_ids) > 0:
            return backup_set_ids[0]
        else:
            raise Py42Error("Failed to get backup sets for device.")

    def get_backup_sets(self, device_guid, destination_guid):
        """Gets all backup set names/identifiers referring to a single destination for a specific
        device.
        `Learn more about backup sets. <https://support.code42.com/Administrator/Cloud/Configuring/Backup_sets>`__

        Args:
            device_guid (str): The GUID of the device to get backup sets for.
            destination_guid (str): The GUID of the destination containing the archive to get
                backup sets for.

        Returns:
            :class:`py42.response.Py42Response`: A response containing the backup sets.
        """
        return self._archive_service.get_backup_sets(device_guid, destination_guid)

    def get_all_org_restore_history(self, days, org_id):
        """Gets all restore jobs from the past given days for the organization with the given ID.

        Args:
            days (int): Number of days of restore history to retrieve.
            org_id (int): The identification number of the organization to get restore history for.

        Returns:
            generator: An object that iterates over :class:`py42.response.Py42Response` objects
            that each contain a page of restore history.
        """
        return self._archive_service.get_all_restore_history(days, "orgId", org_id)

    def get_all_user_restore_history(self, days, user_id):
        """Gets all restore jobs from the past given days for the user with the given ID.

        Args:
            days (int): Number of days of restore history to retrieve.
            user_id (int): The identification number of the user to get restore history for.

        Returns:
            generator: An object that iterates over :class:`py42.response.Py42Response` objects
            that each contain a page of restore history.
        """
        return self._archive_service.get_all_restore_history(days, "userId", user_id)

    def get_all_device_restore_history(self, days, device_id):
        """Gets all restore jobs from the past given days for the device with the given ID.

        Args:
            days (int): Number of days of restore history to retrieve.
            device_id (int): The identification number of the device to get restore history for.

        Returns:
            generator: An object that iterates over :class:`py42.response.Py42Response` objects
            that each contain a page of restore history.
        """
        return self._archive_service.get_all_restore_history(
            days, "computerId", device_id
        )

    def update_cold_storage_purge_date(self, archive_guid, purge_date):
        """Updates the cold storage purge date for a specified archive.

        Args:
            archive_guid (str): The identification number of the archive that should be updated
            purge_date (str): The date on which the archive should be purged in yyyy-MM-dd format

        Returns:
            :class:`py42.response.Py42Response`: the response from the ColdStorage API.
        """
        return self._archive_service.update_cold_storage_purge_date(
            archive_guid, purge_date
        )

    def get_all_org_cold_storage_archives(
        self,
        org_id,
        include_child_orgs=True,
        sort_key="archiveHoldExpireDate",
        sort_dir="asc",
    ):
        """Returns a detailed list of cold storage archive information for a given org ID.

        Args:
            org_id (str): The ID of a Code42 organization.
            include_child_orgs (bool, optional): Determines whether cold storage information from
             the Org's children is also returned. Defaults to True.
            sort_key (str, optional): Sets the property by which the returned results will be sorted.
             Choose from archiveHoldExpireDate, orgName, mountPointName, archiveBytes, and archiveType. Defaults to archiveHoldExpireDate.
            sort_dir (str, optional): Sets the order by which sort_key should be sorted. Choose from
             asc or desc. Defaults to asc.

        Returns:
            generator: An object that iterates over :class:`py42.response.Py42Response` objects
            that each contain a page of cold storage archive information.
        """
        return self._archive_service.get_all_org_cold_storage_archives(
            org_id=org_id,
            include_child_orgs=include_child_orgs,
            sort_key=sort_key,
            sort_dir=sort_dir,
        )
