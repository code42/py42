import json

from py42.clients import BaseClient
from py42.clients.util import get_all_pages


class DeviceClient(BaseClient):
    """
        Class to represent a storage device/node/machine/computer
    """

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
        """Get all device information

        Args:
            active ([bool], optional): device state, True or False. Defaults to None.
            blocked ([bool], optional): blocked status, True or False. Defaults to None.
            org_uid ([int], optional): Id of Organization. Defaults to None.
            user_uid ([int], optional): Id of User. Defaults to None.
            destination_guid ([int], optional): description. Defaults to None.
            include_backup_usage ([type], bool): Flag to denote whether to include backup summary.
             Defaults to None.
            include_counts (bool, optional): [description]. Defaults to True.
            q ([type], optional): [description]. Defaults to None.

        Returns:
            (Py42.sdk.response.Py42Response): A generator containing collection of Py42Response
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
        """Get device information by device_id

        Args:
            device_id ([int]): device_id/'computerId' of the node
            include_backup_usage ([bool], optional): Flag to denote whether to include
              backup summary]. Defaults to None.

        Returns:
            Py42.sdk.response.Py42Response: Py42Response containing device information
        """
        uri = u"/api/Computer/{0}".format(device_id)
        params = dict(incBackupUsage=include_backup_usage, **kwargs)
        return self._session.get(uri, params=params)

    def get_by_guid(self, guid, include_backup_usage=None, **kwargs):
        """Get device information by guid

        Args:
            guid ([str]): guid of the device
            include_backup_usage ([bool], optional): [Flag to denote whether to include
              backup summary]. Defaults to None.

        Returns:
            Py42.sdk.response.Py42Response: Py42Response containing device information
        """
        uri = u"/api/Computer/{0}".format(guid)
        params = dict(idType=u"guid", incBackupUsage=include_backup_usage, **kwargs)
        return self._session.get(uri, params=params)

    def block(self, device_id):
        """Block a device, set blocked_status of the device true

        Args:
            device_id ([int]): device_id/'computerId' of the node

        Returns:
            Py42.sdk.response.Py42Response: Py42Response containing state of the API call
        """
        uri = u"/api/ComputerBlock/{0}".format(device_id)
        return self._session.put(uri)

    def unblock(self, device_id):
        """Unblock a device, set blocked_status of the device false

        Args:
            device_id ([int]): device_id/'computerId' of the node

        Returns:
            Py42.sdk.response.Py42Response: Py42Response containing state of the API call
        """
        uri = u"/api/ComputerBlock/{0}".format(device_id)
        return self._session.delete(uri)

    def deactivate(self, device_id):
        """Deactivate a device, set 'active' status to false

        Args:
            device_id ([int]): device_id/'computerId' of the node

        Returns:
            Py42.sdk.response.Py42Response: Py42Response containing state of the API call
        """
        uri = u"/api/v4/computer-deactivation/update"
        data = {u"id": device_id}
        return self._session.post(uri, data=json.dumps(data))

    def reactivate(self, device_id):
        """Activate a device, set 'active' status to true

        Args:
            device_id ([int]): device_id/'computerId' of the node

        Returns:
            Py42.sdk.response.Py42Response: Py42Response containing state of the API call
        """
        uri = u"/api/v4/computer-deactivation/remove"
        data = {u"id": device_id}
        return self._session.post(uri, data=json.dumps(data))

    def deauthorize(self, device_id):
        """Deauthorize the device

        Args:
            device_id ([int]): device_id/'computerId' of the node

        Returns:
            Py42.sdk.response.Py42Response: Py42Response containing state of the API call
        """
        uri = u"/api/ComputerDeauthorization/{0}".format(device_id)
        return self._session.put(uri)

    def get_settings(self, guid, keys=None):
        """Settings of the device

        Args:
            guid ([str]): guid of the device
            keys ([type], optional): [description]. Defaults to None.

        Returns:
            Py42.sdk.response.Py42Response: Py42Response containing settings information
        """
        uri = u"/api/v4/device-setting/view"
        params = {u"guid": guid, u"keys": keys}
        return self._session.get(uri, params=params)
