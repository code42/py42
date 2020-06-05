class ArchiveModule(object):
    """A module for getting information about backup archives on storage nodes along with
    functionality for streaming a file from backup.
    """

    def __init__(self, archive_accessor_manager, archive_client):
        self._archive_accessor_manager = archive_accessor_manager
        self._archive_client = archive_client

    def stream_from_backup(
        self,
        file_path,
        device_guid,
        destination_guid=None,
        archive_password=None,
        encryption_key=None,
    ):
        """Streams a file from a backup archive to memory.
        `REST Documentation <https://console.us.code42.com/apidocviewer/#WebRestoreJobResult-get>`__

        Args:
            file_path (str): The path to the file in your archive.
            device_guid (str): The GUID of the device the file belongs to.
            destination_guid (str, optional): The GUID of the destination that stores the backup
                of the file. If None, it will use the first destination GUID it finds for your
                device. 'destination_guid' may be useful if the file is missing from one of your
                destinations or if you want to optimize performance. Defaults to None.
            archive_password (str, None): The password for archives that are protected with an
                additional password. This is only relevant to users with archive key password
                security. Defaults to None.
            encryption_key (str, None): A custom encryption key for decryption an archive's file
                contents, necessary for restoring files. This is only relevant to users with custom
                key archive security. Defaults to None.
        Returns:
            :class:`py42.response.Py42Response`: A response containing the streamed content.

        Usage example::

            stream_response = sdk.archive.stream_from_backup("/full/path/to/file.txt", "1234567890")
            with open("/path/to/my/file", 'wb') as f:
                for chunk in stream_response.iter_content(chunk_size=128):
                    if chunk:
                        f.write(chunk)
        """
        archive_accessor = self._archive_accessor_manager.get_archive_accessor(
            device_guid,
            destination_guid=destination_guid,
            private_password=archive_password,
            encryption_key=encryption_key,
        )
        return archive_accessor.stream_from_backup(file_path)

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
        return self._archive_client.get_backup_sets(device_guid, destination_guid)

    def get_all_org_restore_history(self, days, org_id):
        """Gets all restore jobs from the past given days for the organization with the given ID.
        `REST Documentation <https://console.us.code42.com/apidocviewer/#RestoreHistory-get>`__

        Args:
            days (int): Number of days of restore history to retrieve.
            org_id (int): The identification number of the organization to get restore history for.

        Returns:
            generator: An object that iterates over :class:`py42.response.Py42Response` objects
            that each contain a page of restore history.
        """
        return self._archive_client.get_all_restore_history(days, u"orgId", org_id)

    def get_all_user_restore_history(self, days, user_id):
        """Gets all restore jobs from the past given days for the user with the given ID.
        `REST Documentation <https://console.us.code42.com/apidocviewer/#RestoreHistory-get>`__

        Args:
            days (int): Number of days of restore history to retrieve.
            user_id (int): The identification number of the user to get restore history for.

        Returns:
            generator: An object that iterates over :class:`py42.response.Py42Response` objects
            that each contain a page of restore history.
        """
        return self._archive_client.get_all_restore_history(days, u"userId", user_id)

    def get_all_device_restore_history(self, days, device_id):
        """Gets all restore jobs from the past given days for the device with the given ID.
        `REST Documentation <https://console.us.code42.com/apidocviewer/#RestoreHistory-get>`__

        Args:
            days (int): Number of days of restore history to retrieve.
            device_id (int): The identification number of the device to get restore history for.

        Returns:
            generator: An object that iterates over :class:`py42.response.Py42Response` objects
            that each contain a page of restore history.
        """
        return self._archive_client.get_all_restore_history(days, u"computerId", device_id)

    def update_cold_storage_purge_date(self, archive_guid, purge_date):
        """Updates the cold storage purge date for a specified archive.
        `REST Documentation <https://console.us.code42.com/apidocviewer/#ColdStorage-put>`__

        Args:
            archive_guid (str): The identification number of the archive that should be updated
            purge_date (str): The date on which the archive should be purged in yyyy-MM-dd format

        Returns:
            :class:`py42.response.Py42Response`: the response from the ColdStorage API.
        """
        return self._archive_client.update_cold_storage_purge_date(archive_guid, purge_date)

    def get_all_org_cold_storage_archives(
        self, org_id, include_child_orgs=True, sort_key="archiveHoldExpireDate", sort_dir="asc"
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
        return self._archive_client.get_all_org_cold_storage_archives(org_id)
