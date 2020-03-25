class ArchiveModule(object):
    """A module that combines the class :class:`py42.clients.ArchiveClient` with a mechanism for
    actually streaming a file from backup. It also simplifies getting restore history by
    providing methods to get history by org ID, device ID, and user ID.
    """

    def __init__(self, archive_accessor_manager, archive_client):
        self._archive_accessor_manager = archive_accessor_manager
        self._archive_client = archive_client

    def stream_from_backup(self, file_path, device_guid, destination_guid=None):
        """Streams a file in your archive to your local machine.

        Args:
            file_path (str): The path to the file on your archive.
            device_guid (str): The device GUID for the device the file belongs to.
            destination_guid (str, optional): The device GUID for the server that stores the
                backup of the file. If None, it will use the first destination GUID it finds for
                your device. 'destination_guid' may be useful if the file is missing from one of
                your destinations or if you want to optimize performance. Defaults to None.

        Returns:
            :class:`py42.sdk.response.Py42Response`: A response containing the streamed content.
        """
        archive_accessor = self._archive_accessor_manager.get_archive_accessor(
            device_guid, destination_guid=destination_guid
        )
        return archive_accessor.stream_from_backup(file_path)

    def get_backup_sets(self, device_guid, destination_guid):
        """Gets Code42 Backup sets, or response objects representing groups of files that are set
        to back up to different locations with different settings.
        `Support Page: <https://support.code42.com/Administrator/Cloud/Configuring/Backup_sets>`__

        Args:
            device_guid (str): The device GUID for the device to get backup sets for.
            destination_guid (str): The destination GUID for the device containing the archive
                to get backup sets for.

        Returns:
            :class:`py42.sdk.response.Py42Response`: A response containing the backup sets.
        """
        return self._archive_client.get_backup_sets(device_guid, destination_guid)

    def get_data_key_token(self, device_guid):
        """Gets a data key token from the server for a storage node in order to request an
        encryption key.
        `REST Documentation: <https://console.us.code42.com/apidocviewer/#DataKeyToken-post>`__

        Args:
            device_guid (str): The device GUID for the device responsible for the archive you
                eventually wish to restore from.

        Returns:
            :class:`py42.sdk.response.Py42Response`: A response containing the token.
        """
        return self._archive_client.get_data_key_token(device_guid)

    def get_all_restore_history_by_org_id(self, days, org_id):
        """Gets all restore jobs from the past given days for the organization with the given
        org ID.
        `REST Documentation`: <https://console.us.code42.com/apidocviewer/#RestoreHistory-get>`__

        Args:
            days (int): The number of days back to get all restore history from.
            org_id (int): The org ID for the organization to get restore history for.

        Returns:
            generator: An object that iterates over :class:`py42.sdk.response.Py42Response` objects
            that each contain a page of restore history.
        """
        return self._archive_client.get_all_restore_history(days, u"orgId", org_id)

    def get_all_restore_history_by_user_id(self, days, user_id):
        """Gets all restore jobs from the past given days for the user with the given user ID.
        `REST Documentation`: <https://console.us.code42.com/apidocviewer/#RestoreHistory-get>`__

        Args:
            days (int): The number of days back to get all restore history from.
            user_id (int): The user ID for the user to get restore history for.

        Returns:
            generator: An object that iterates over :class:`py42.sdk.response.Py42Response` objects
            that each contain a page of restore history.
        """
        return self._archive_client.get_all_restore_history(days, u"userId", user_id)

    def get_all_restore_history_by_device_id(self, days, device_id):
        """Gets all restore jobs from the past given days for the device with the given device ID.
        `REST Documentation`: <https://console.us.code42.com/apidocviewer/#RestoreHistory-get>`__

        Args:
            days (int): The number of days back to get all restore history from.
            device_id (int): The device ID for the device to get restore history for.

        Returns:
            generator: An object that iterates over :class:`py42.sdk.response.Py42Response` objects
            that each contain a page of restore history.
        """
        return self._archive_client.get_all_restore_history(days, u"computerId", device_id)

    def get_web_restore_info(self, src_guid, dest_guid):
        """Gets necessary information for performing a web restore.
        `REST Documentation: <https://console.us.code42.com/apidocviewer/#WebRestoreInfo-get>`__

        Args:
            src_guid (str): The device GUID for the device responsible for the archive you
                eventually wish restore from.
            dest_guid (str): The device GUID for the server containing the archive you eventually
                wish to perform from.

        Returns:
            :class:`py42.sdk.response.Py42Response`: A response containing information needed
            to conduct a web restore.
        """
        return self._archive_client.get_web_restore_info(src_guid, dest_guid)
