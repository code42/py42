import json

from py42.clients import BaseClient
from py42.clients.util import get_all_pages


class DeviceClient(BaseClient):
    """Class to interact with Code42 device/computer API."""

    def _get_page(
        self,
        active=None,
        blocked=None,
        org_uid=None,
        user_uid=None,
        destination_guid=None,
        include_backup_usage=None,
        include_counts=True,
        page_num=None,
        page_size=None,
        q=None,
    ):
        uri = u"/api/Computer"
        params = {
            u"active": active,
            u"blocked": blocked,
            u"orgUid": org_uid,
            u"userUid": user_uid,
            u"targetComputerGuid": destination_guid,
            u"incBackupUsage": include_backup_usage,
            u"incCounts": include_counts,
            u"pgNum": page_num,
            u"pgSize": page_size,
            u"q": q,
        }

        return self._session.get(uri, params=params)

    def get_all(
        self,
        active=None,
        blocked=None,
        org_uid=None,
        user_uid=None,
        destination_guid=None,
        include_backup_usage=None,
        include_counts=True,
        q=None,
        **kwargs
    ):
        """Gets all device information.

        When no arguments are passed all records are returned, to filter results specify
        respective arguments.
        For example, to retrieve all active and blocked devices pass active=true and blocked=true.

        `REST API Documentation <https://console.us.code42.com/apidocviewer/#Computer-get>`__

        It returns a generator of pages of devices, depending on logged in user account's role
            in the organization.

            * For a logged in ordinary end user, returns all devices of the user.

            * For an organization administrator, returns all the devices in respective organization.

            * For a cross-organization administrator, returns all devices across all organizations
              that they are administrator of.

            * Finally, for a customer cloud administrator, returns all devices in all organizations.

        Args:
            active (bool, optional): Filters results by device state. When set to True, gets all
              active devices. When set to False, gets all deactivated devices. When set to None
              or excluded, gets all devices regardless of state. Defaults to None.
            blocked (bool, optional): Filter results by blocked status, True or False.
              Defaults to None.
            org_uid (int, optional): Id of Organization. Defaults to None.
            user_uid (int, optional): Id of User. Defaults to None.
            destination_guid (str of int, optional): 'guid' of server that the desktop clients
              back up their files to. Defaults to None.
            include_backup_usage (type, bool): Flag to denote whether to include destination and
              its backup summary. Defaults to None.
            include_counts (bool, optional): Flag to denote whether to include total, warning, and
              critical counts. Defaults to True.
            q (type, optional): Search results flexibly by incomplete guid, host-name,
              computer name, etc Defaults to None.

        Returns:
            generator: Collection of :class:`Py42.sdk.response.Py42Response` objects.

        """

        return get_all_pages(
            self._get_page,
            u"computers",
            active=active,
            blocked=blocked,
            org_uid=org_uid,
            user_uid=user_uid,
            destination_guid=destination_guid,
            include_backup_usage=include_backup_usage,
            include_counts=include_counts,
            q=q,
            **kwargs
        )

    def get_by_id(self, device_id, include_backup_usage=None, **kwargs):
        """Gets device information by device_id.

        `REST API Documentation <https://console.us.code42.com/apidocviewer/#Computer-get>`__

        Args:
            device_id (int): 'device_id'/'computerId' of the node.
            include_backup_usage (bool, optional): Flag to denote whether to include
              backup summary. Defaults to None.

        Returns:
            :class:`Py42.sdk.response.Py42Response`: Py42Response containing device information.
        """
        uri = u"/api/Computer/{0}".format(device_id)
        params = dict(incBackupUsage=include_backup_usage, **kwargs)
        return self._session.get(uri, params=params)

    def get_by_guid(self, guid, include_backup_usage=None, **kwargs):
        """Gets device information by guid.

        `REST API Documentation <https://console.us.code42.com/apidocviewer/#Computer-get>`__

        Args:
            guid (str): 'guid' of the device.
            include_backup_usage (bool, optional): Flag to denote whether to include
              backup summary. Defaults to None.

        Returns:
            :class:`Py42.sdk.response.Py42Response`: Py42Response containing device information
        """
        uri = u"/api/Computer/{0}".format(guid)
        params = dict(idType=u"guid", incBackupUsage=include_backup_usage, **kwargs)
        return self._session.get(uri, params=params)

    def block(self, device_id):
        """Blocks a device causing the user not to be able to login or restore.

        `REST API Documentation <https://console.us.code42.com/apidocviewer/#ComputerBlock>`__

        Args:
            device_id (int): 'device_id'/'computerId' of the node.

        Returns:
            :class:`Py42.sdk.response.Py42Response`: Py42Response containing state of the API call.
        """
        uri = u"/api/ComputerBlock/{0}".format(device_id)
        return self._session.put(uri)

    def unblock(self, device_id):
        """Unblocks a device, permitting a user to be able to login and restore again.

        `REST API Documentation <https://console.us.code42.com/apidocviewer/#ComputerBlock>`__

        Args:
            device_id (int): 'device_id'/'computerId' of the node.

        Returns:
            :class:`Py42.sdk.response.Py42Response`: Py42Response containing state of the API call.
        """
        uri = u"/api/ComputerBlock/{0}".format(device_id)
        return self._session.delete(uri)

    def deactivate(self, device_id):
        """Deactivates a device, causing backups to stop and archives to go to cold storage.

        `REST API Documentation <https://console.us.code42.com/apidocviewer/#ComputerDeactivation>`__

        Args:
            device_id (int): 'device_id'/'computerId' of the node.

        Returns:
            :class:`Py42.sdk.response.Py42Response`: Py42Response containing state of the API call.
        """
        uri = u"/api/v4/computer-deactivation/update"
        data = {u"id": device_id}
        return self._session.post(uri, data=json.dumps(data))

    def reactivate(self, device_id):
        """Activates a previously deactivated device.

        `REST API Documentation <https://console.us.code42.com/apidocviewer/#ComputerDeactivation>`__

        Args:
            device_id (int): 'device_id'/'computerId' of the node.

        Returns:
            :class:`Py42.sdk.response.Py42Response`: Py42Response containing state of the API call.
        """
        uri = u"/api/v4/computer-deactivation/remove"
        data = {u"id": device_id}
        return self._session.post(uri, data=json.dumps(data))

    def deauthorize(self, device_id):
        """
        Deauthorizes the device with the given device ID. If used on a cloud connector device,
        it will remove the authorization token for that account.

        `REST API Documentation <https://console.us.code42.com/apidocviewer/#ComputerDeauthorization>`__

        Args:
            device_id (int): 'device_id'/'computerId' of the node.

        Returns:
            :class:`Py42.sdk.response.Py42Response`: Py42Response containing state of the API call.
        """
        uri = u"/api/ComputerDeauthorization/{0}".format(device_id)
        return self._session.put(uri)

    def get_settings(self, guid, keys=None):
        """Gets settings of the device.

        `REST API Documentation <https://console.us.code42.com/apidocviewer/#DeviceSetting>`__

        Args:
            guid (str): 'guid' of the device.
            keys (type, optional): Comma separated list of device keys. Defaults to None.

        Returns:
            :class:`Py42.sdk.response.Py42Response`: Py42Response containing settings information.
        """
        uri = u"/api/v4/device-setting/view"
        params = {u"guid": guid, u"keys": keys}
        return self._session.get(uri, params=params)
