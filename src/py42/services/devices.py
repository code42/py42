from collections import namedtuple
from time import time

from py42 import settings
from py42.clients.settings.device_settings import DeviceSettings
from py42.exceptions import Py42BadRequestError
from py42.services import BaseService
from py42.services import handle_active_legal_hold_error
from py42.services.util import get_all_pages

DeviceSettingsResponse = namedtuple(
    "DeviceSettingsResponse", ["error", "settings_response", "device_settings_response"]
)


class DeviceService(BaseService):
    """A class to interact with Code42 device/computer APIs."""

    def get_page(
        self,
        page_num,
        active=None,
        blocked=None,
        org_uid=None,
        user_uid=None,
        destination_guid=None,
        include_backup_usage=None,
        include_counts=True,
        page_size=None,
        q=None,
    ):
        """Gets a page of devices.
        `REST Documentation <https://console.us.code42.com/apidocviewer/#Computer-get>`__

        Args:
            page_num (int): The page number to request.
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
            page_size (int, optional): The number of devices to return per page. Defaults to
                `py42.settings.items_per_page`.
            q (str, optional): Searches results flexibly by incomplete GUID, hostname,
                computer name, etc. Defaults to None.

        Returns:
            :class:`py42.response.Py42Response`
        """

        uri = "/api/Computer"
        page_size = page_size or settings.items_per_page
        params = {
            "active": active,
            "blocked": blocked,
            "orgUid": org_uid,
            "userUid": user_uid,
            "targetComputerGuid": destination_guid,
            "incBackupUsage": include_backup_usage,
            "incCounts": include_counts,
            "pgNum": page_num,
            "pgSize": page_size,
            "q": q,
        }

        return self._connection.get(uri, params=params)

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
        **kwargs,
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
            self.get_page,
            "computers",
            active=active,
            blocked=blocked,
            org_uid=org_uid,
            user_uid=user_uid,
            destination_guid=destination_guid,
            include_backup_usage=include_backup_usage,
            include_counts=include_counts,
            q=q,
            **kwargs,
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
        uri = f"/api/Computer/{device_id}"
        params = dict(incBackupUsage=include_backup_usage, **kwargs)
        return self._connection.get(uri, params=params)

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
        uri = f"/api/Computer/{guid}"
        params = dict(idType="guid", incBackupUsage=include_backup_usage, **kwargs)
        return self._connection.get(uri, params=params)

    def block(self, device_id):
        """Blocks a device causing the user not to be able to log in to or restore from Code42 on
        that device.
        `REST Documentation <https://console.us.code42.com/apidocviewer/#ComputerBlock>`__

        Args:
            device_id (int): The identification number of the device.

        Returns:
            :class:`py42.response.Py42Response`
        """
        uri = f"/api/ComputerBlock/{device_id}"
        return self._connection.put(uri)

    def unblock(self, device_id):
        """Unblocks a device, permitting a user to be able to login and restore again.
        `REST Documentation <https://console.us.code42.com/apidocviewer/#ComputerBlock>`__

        Args:
            device_id (int): The identification number of the device.

        Returns:
            :class:`py42.response.Py42Response`
        """
        uri = f"/api/ComputerBlock/{device_id}"
        return self._connection.delete(uri)

    def deactivate(self, device_id):
        """Deactivates a device, causing backups to stop and archives to go to cold storage.
        `REST Documentation <https://console.us.code42.com/swagger/index.html?urls.primaryName=v4#/computer-deactivation/ComputerDeactivation_Update>`__

        Args:
            device_id (int): The identification number of the device.

        Returns:
            :class:`py42.response.Py42Response`
        """
        uri = "/api/v4/computer-deactivation/update"
        data = {"id": device_id}
        try:
            return self._connection.post(uri, json=data)
        except Py42BadRequestError as ex:
            handle_active_legal_hold_error(ex, "device", device_id)
            raise

    def reactivate(self, device_id):
        """Activates a previously deactivated device.
        `REST Documentation <https://console.us.code42.com/swagger/?urls.primaryName=v4#/computer-deactivation/ComputerDeactivation_Remove>`__

        Args:
            device_id (int): The identification number of the device.

        Returns:
            :class:`py42.response.Py42Response`
        """
        uri = "/api/v4/computer-deactivation/remove"
        data = {"id": device_id}
        return self._connection.post(uri, json=data)

    def deauthorize(self, device_id):
        """Deauthorizes the device with the given ID. If used on a cloud connector device, it will
        remove the authorization token for that account.
        `REST Documentation <https://console.us.code42.com/apidocviewer/#ComputerDeauthorization>`__

        Args:
            device_id (int): The identification number of the device.

        Returns:
            :class:`py42.response.Py42Response`
        """
        uri = f"/api/ComputerDeauthorization/{device_id}"
        return self._connection.put(uri)

    def get_agent_state(self, guid, property_name):
        """Gets the agent state of the device.
            `REST Documentation <https://console.us.code42.com/swagger/index.html?urls.primaryName=v14#/agent-state/AgentState_ViewByDeviceGuid>`__

            Args:
                guid (str): The globally unique identifier of the device.
                property_name (str): The name of the property to retrieve (e.g. `fullDiskAccess`).

            Returns:
                :class:`py42.response.Py42Response`: A response containing settings information.
            """
        uri = "/api/v14/agent-state/view-by-device-guid"
        params = {"deviceGuid": guid, "propertyName": property_name}
        return self._connection.get(uri, params=params)

    def get_agent_full_disk_access_state(self, guid):
        """Gets the full disk access status of a device.
            `REST Documentation <https://console.us.code42.com/swagger/index.html?urls.primaryName=v14#/agent-state/AgentState_ViewByDeviceGuid>`__

            Args:
                guid (str): The globally unique identifier of the device.

            Returns:
                :class:`py42.response.Py42Response`: A response containing settings information.
            """
        return self.get_agent_state(guid, "fullDiskAccess")

    def get_settings(self, guid):
        """Gets setting data for a device and returns a `DeviceSettings` object for the target device.

        Args:
            guid (int,str): The globally unique identifier of the device.

        Returns:
            :class:`py42.clients.settings.device_settings.DeviceSettings`: A class to help manage device settings.
        """
        settings = self.get_by_guid(guid, incSettings=True)
        return DeviceSettings(settings.data)

    def update_settings(self, device_settings):
        """Updates a device's settings based on changes to the passed in `DeviceSettings` instance.

        Args:
            device_settings (`DeviceSettings`): An instance of `DeviceSettings` with desired modifications to settings.

        Returns:
            :class:`py42.response.Py42Response`: A response containing the result of the setting change.
        """
        device_settings = dict(device_settings)
        device_id = device_settings["computerId"]
        uri = f"/api/Computer/{device_id}"
        new_config_date_ms = str(int(time() * 1000))
        device_settings["settings"]["configDateMs"] = new_config_date_ms
        return self._connection.put(uri, json=device_settings)
