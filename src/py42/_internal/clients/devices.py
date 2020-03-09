import json

import py42.settings as settings
from py42._internal.base_classes import BaseClient
from py42._internal.clients.util import get_all_pages
from py42._internal.response import Py42Response


class DeviceClient(BaseClient):
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

        return Py42Response(self._session.get(uri, params=params), json_key=u"computers")

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

        return get_all_pages(
            self._get_page,
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
            **kwargs
        )

    def get_by_id(self, device_id, include_backup_usage=None, **kwargs):
        uri = u"/api/Computer/{0}".format(device_id)
        params = dict(incBackupUsage=include_backup_usage, **kwargs)
        return Py42Response(self._session.get(uri, params=params))

    def get_by_guid(self, guid, include_backup_usage=None, **kwargs):
        uri = u"/api/Computer/{0}".format(guid)
        params = dict(idType=u"guid", incBackupUsage=include_backup_usage, **kwargs)
        return Py42Response(self._session.get(uri, params=params))

    def block(self, computer_id):
        uri = u"/api/ComputerBlock/{0}".format(computer_id)
        return Py42Response(self._session.put(uri))

    def unblock(self, computer_id):
        uri = u"/api/ComputerBlock/{0}".format(computer_id)
        return Py42Response(self._session.delete(uri))

    def deactivate(self, computer_id):
        uri = u"/api/v4/computer-deactivation/update"
        data = {u"id": computer_id}
        return Py42Response(self._session.post(uri, data=json.dumps(data)))

    def reactivate(self, computer_id):
        uri = u"/api/v4/computer-deactivation/remove"
        data = {u"id": computer_id}
        return Py42Response(self._session.post(uri, data=json.dumps(data)))

    def deauthorize(self, computer_id):
        uri = u"/api/ComputerDeauthorization/{0}".format(computer_id)
        return Py42Response(self._session.put(uri))

    def get_settings(self, guid, keys=None):
        uri = u"/api/v4/device-setting/view"
        params = {u"guid": guid, u"keys": keys}
        return Py42Response(self._session.get(uri, params=params))
