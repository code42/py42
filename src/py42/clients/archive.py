import json

from py42.clients import BaseClient
from py42.clients.util import get_all_pages


class ArchiveClient(BaseClient):
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
        uri = u"/api/DataKeyToken"
        data = {u"computerGuid": device_guid}
        return self._session.post(uri, data=json.dumps(data))

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
        uri = u"/c42api/v3/BackupSets/{}/{}".format(device_guid, destination_guid)
        return self._session.get(uri)

    def get_all_restore_history(self, days, id_type, id_value, **kwargs):
        """Gets all restore jobs from the past given days.
        `REST Documentation: <https://console.us.code42.com/apidocviewer/#RestoreHistory-get>`__

        Args:
            days (int): The number of days back to get all restore history from.
            id_type (str): Either an 'orgId', 'computerId', or 'userId' and should describe
                the parameter 'id_value'.
            id_value (str): The ID described by the parameter `id_type`.

        Returns:
            generator: An object that iterates over :class:`py42.sdk.response.Py42Response` objects
            that each contain a page of restore history.
        """
        return get_all_pages(
            self._get_restore_history_page,
            u"restoreEvents",
            days=days,
            id_type=id_type,
            id_value=id_value,
            **kwargs
        )

    def _get_restore_history_page(self, days, id_type, id_value, page_num, page_size, **kwargs):
        uri = u"/api/RestoreHistory"
        params = dict(days=days, pgNum=page_num, pgSize=page_size, **kwargs)
        params[id_type] = id_value
        return self._session.get(uri, params=params)

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
        uri = u"/api/WebRestoreInfo"
        params = {u"srcGuid": src_guid, u"destGuid": dest_guid}
        return self._session.get(uri, params=params)
