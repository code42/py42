class ArchiveModule(object):
    """A module for getting information about archives on storage nodes along with functionality
    for streaming a file from backup.
    """

    def __init__(self, archive_accessor_manager, archive_client):
        self._archive_accessor_manager = archive_accessor_manager
        self._archive_client = archive_client

    def stream_from_backup(self, file_path, device_guid, destination_guid=None):
        """Streams a file from an archive to memory.
        `REST Documentation <https://console.us.code42.com/apidocviewer/#WebRestoreJobResult-get>`__

        Args:
            file_path (str): The path to the file in your archive.
            device_guid (str): The GUID for the device the file belongs to.
            destination_guid (str, optional): The GUID for the server that stores the backup of
                the file. If None, it will use the first destination GUID it finds for your
                device. 'destination_guid' may be useful if the file is missing from one of your
                destinations or if you want to optimize performance. Defaults to None.

        Returns:
            :class:`py42.sdk.response.Py42Response`: A response containing the streamed content.
        """
        archive_accessor = self._archive_accessor_manager.get_archive_accessor(
            device_guid, destination_guid=destination_guid
        )
        return archive_accessor.stream_from_backup(file_path)

    def get_backup_sets(self, device_guid, destination_guid):
        """Gets all backup set names/identifiers referring to single destination for a specific
        device.
        `Support Page <https://support.code42.com/Administrator/Cloud/Configuring/Backup_sets>`__

        Args:
            device_guid (str): The GUID for the device to get backup sets for.
            destination_guid (str): The destination GUID for the device containing the archive
                to get backup sets for.

        Returns:
            :class:`py42.sdk.response.Py42Response`: A response containing the backup sets.
        """
        return self._archive_client.get_backup_sets(device_guid, destination_guid)

    def get_all_restore_history_by_org_id(self, days, org_id):
        """Gets all restore jobs from the past given days for the organization with the given ID.
        `REST Documentation <https://console.us.code42.com/apidocviewer/#RestoreHistory-get>`__

        Args:
            days (int): Number of days of restore history to retrieve.
            org_id (int): The ID for the organization to get restore history for.

        Returns:
            generator: An object that iterates over :class:`py42.sdk.response.Py42Response` objects
            that each contain a page of restore history.
        """
        return self._archive_client.get_all_restore_history(days, u"orgId", org_id)

    def get_all_restore_history_by_user_id(self, days, user_id):
        """Gets all restore jobs from the past given days for the user with the given ID.
        `REST Documentation <https://console.us.code42.com/apidocviewer/#RestoreHistory-get>`__

        Args:
            days (int): Number of days of restore history to retrieve.
            user_id (int): The ID for the user to get restore history for.

        Returns:
            generator: An object that iterates over :class:`py42.sdk.response.Py42Response` objects
            that each contain a page of restore history.
        """
        return self._archive_client.get_all_restore_history(days, u"userId", user_id)

    def get_all_restore_history_by_device_id(self, days, device_id):
        """Gets all restore jobs from the past given days for the device with the given ID.
        `REST Documentation <https://console.us.code42.com/apidocviewer/#RestoreHistory-get>`__

        Args:
            days (int): Number of days of restore history to retrieve.
            device_id (int): The ID for the device to get restore history for.

        Returns:
            generator: An object that iterates over :class:`py42.sdk.response.Py42Response` objects
            that each contain a page of restore history.
        """
        return self._archive_client.get_all_restore_history(days, u"computerId", device_id)
