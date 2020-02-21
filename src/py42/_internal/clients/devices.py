import json

from py42._internal.base_classes import BaseAuthorityClient
from py42._internal.clients.util import get_all_pages
import py42.settings as settings


class DeviceClient(BaseAuthorityClient):
    def _get_devices_page(
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

        return self._default_session.get(uri, params=params)

    def get_devices(
        self,
        active=None,
        blocked=None,
        org_uid=None,
        user_uid=None,
        destination_guid=None,
        include_backup_usage=None,
        include_counts=True,
        q=None,
    ):

        return get_all_pages(
            self._get_devices_page,
            settings.items_per_page,
            u"computers",
            active=active,
            blocked=blocked,
            org_uid=org_uid,
            user_uid=user_uid,
            destination_guid=destination_guid,
            include_backup_usage=include_backup_usage,
            include_counts=include_counts,
            q=q,
        )

    def get_device_by_id(self, device_id, include_backup_usage=None):
        uri = u"/api/Computer/{0}".format(device_id)
        params = {u"incBackupUsage": include_backup_usage}
        return self._default_session.get(uri, params=params)

    def get_device_by_guid(self, guid, include_backup_usage=None):
        uri = u"/api/Computer/{0}?idType=guid".format(guid)
        params = {u"incBackupUsage": include_backup_usage}
        return self._default_session.get(uri, params=params)

    def block_device(self, computer_id):
        uri = u"/api/ComputerBlock/{0}".format(computer_id)
        return self._default_session.put(uri)

    def unblock_device(self, computer_id):
        uri = u"/api/ComputerBlock/{0}".format(computer_id)
        return self._default_session.delete(uri)

    def deactivate_device(self, computer_id):
        uri = u"/api/v4/computer-deactivation/update"
        data = {u"id": computer_id}
        return self._v3_required_session.post(uri, data=json.dumps(data))

    def reactivate_device(self, computer_id):
        uri = u"/api/v4/computer-deactivation/remove"
        data = {u"id": computer_id}
        return self._v3_required_session.post(uri, data=json.dumps(data))

    def deauthorize_device(self, computer_id):
        uri = u"/api/ComputerDeauthorization/{0}".format(computer_id)
        return self._default_session.put(uri)

    def get_device_settings(self, guid, keys=None):
        uri = u"/api/v4/device-setting/view"
        params = {u"guid": guid, u"keys": keys}
        return self._v3_required_session.get(uri, params=params)
