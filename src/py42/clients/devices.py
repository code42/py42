import json

from py42.clients import BaseClient
from py42.clients.util import get_all_pages


class DeviceClient(BaseClient):
    """A class to interact with Code42 device/computer APIs."""

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

        When no arguments are passed, all records are returned. To filter results, specify
        respective arguments. For example, to retrieve all active and blocked devices, pass
        active=true and blocked=true.
        `REST Documentation <https://console.us.code42.com/apidocviewer/#Computer-get>`__

        Args:
            active (bool, optional): Filters results by device state. When set to True, gets all
                active devices. When set to False, gets all deactivated devices. When set to None
                or excluded, gets all devices regardless of state. Defaults to None.
            blocked (bool, optional): Filters results by blocked status: True or False. Defaults
                to None.
            org_uid (int, optional): The identification number of an Organization. Defaults to None.
            user_uid (int, optional): The identification number of a User. Defaults to None.
            destination_guid (str or int, optional): The globally unique identifier of the storage
                server that the device back up to. Defaults to None.
            include_backup_usage (bool, optional): A flag to denote whether to include the
                destination and its backup stats. Defaults to None.
            include_counts (bool, optional): A flag to denote whether to include total, warning,
                and critical counts. Defaults to True.
            q (str, optional): Searches results flexibly by incomplete GUID, hostname,
                computer name, etc. Defaults to None.

        Returns:
            generator: An object that iterates over :class:`py42.response.Py42Response` objects
            that each contain a page of devices.

            The devices returned by `get_all()` are based on the role and permissions of the user
            authenticating the py42 SDK.
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
        """Gets device information by ID.
        `REST Documentation <https://console.us.code42.com/apidocviewer/#Computer-get>`__

        Args:
            device_id (int): The identification number of the device.
            include_backup_usage (bool, optional): A flag to denote whether to include the
                destination and its backup stats. Defaults to None.

        Returns:
            :class:`py42.response.Py42Response`: A response containing device information.
        """
        uri = u"/api/Computer/{0}".format(device_id)
        params = dict(incBackupUsage=include_backup_usage, **kwargs)
        return self._session.get(uri, params=params)

    def get_by_guid(self, guid, include_backup_usage=None, **kwargs):
        """Gets device information by GUID.
        `REST Documentation <https://console.us.code42.com/apidocviewer/#Computer-get>`__

        Args:
            guid (str): The globally unique identifier of the device.
            include_backup_usage (bool, optional): A flag to denote whether to include the
                destination and its backup stats. Defaults to None.

        Returns:
            :class:`py42.response.Py42Response`: A response containing device information.
        """
        uri = u"/api/Computer/{0}".format(guid)
        params = dict(idType=u"guid", incBackupUsage=include_backup_usage, **kwargs)
        return self._session.get(uri, params=params)

    def block(self, device_id):
        """Blocks a device causing the user not to be able to log in to or restore from Code42 on
        that device.
        `REST Documentation <https://console.us.code42.com/apidocviewer/#ComputerBlock>`__

        Args:
            device_id (int): The identification number of the device.

        Returns:
            :class:`py42.response.Py42Response`
        """
        uri = u"/api/ComputerBlock/{0}".format(device_id)
        return self._session.put(uri)

    def unblock(self, device_id):
        """Unblocks a device, permitting a user to be able to login and restore again.
        `REST Documentation <https://console.us.code42.com/apidocviewer/#ComputerBlock>`__

        Args:
            device_id (int): The identification number of the device.

        Returns:
            :class:`py42.response.Py42Response`
        """
        uri = u"/api/ComputerBlock/{0}".format(device_id)
        return self._session.delete(uri)

    def deactivate(self, device_id):
        """Deactivates a device, causing backups to stop and archives to go to cold storage.
        `REST Documentation <https://console.us.code42.com/apidocviewer/#ComputerDeactivation>`__

        Args:
            device_id (int): The identification number of the device.

        Returns:
            :class:`py42.response.Py42Response`
        """
        uri = u"/api/v4/computer-deactivation/update"
        data = {u"id": device_id}
        return self._session.post(uri, data=json.dumps(data))

    def reactivate(self, device_id):
        """Activates a previously deactivated device.
        `REST Documentation <https://console.us.code42.com/apidocviewer/#ComputerDeactivation>`__

        Args:
            device_id (int): The identification number of the device.

        Returns:
            :class:`py42.response.Py42Response`
        """
        uri = u"/api/v4/computer-deactivation/remove"
        data = {u"id": device_id}
        return self._session.post(uri, data=json.dumps(data))

    def deauthorize(self, device_id):
        """Deauthorizes the device with the given ID. If used on a cloud connector device, it will
        remove the authorization token for that account.
        `REST Documentation <https://console.us.code42.com/apidocviewer/#ComputerDeauthorization>`__

        Args:
            device_id (int): The identification number of the device.

        Returns:
            :class:`py42.response.Py42Response`
        """
        uri = u"/api/ComputerDeauthorization/{0}".format(device_id)
        return self._session.put(uri)

    def get_settings(self, guid, keys=None):
        """Gets settings of the device.
        `REST Documentation <https://console.us.code42.com/apidocviewer/#DeviceSetting>`__

        Args:
            guid (str): The globally unique identifier of the device.
            keys (str, optional): A comma separated list of device keys. Defaults to None.

        Returns:
            :class:`py42.response.Py42Response`: A response containing settings information.
        """
        uri = u"/api/v4/device-setting/view"
        params = {u"guid": guid, u"keys": keys}
        return self._session.get(uri, params=params)
