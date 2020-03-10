import json

from py42.clients import BaseClient
from py42.sdk.response import Py42Response


class ArchiveClient(BaseClient):
    def get_data_key_token(self, computer_guid):
        uri = u"/api/DataKeyToken"
        data = {u"computerGuid": computer_guid}
        return Py42Response(
            self._session.post(uri, data=json.dumps(data)), json_key=u"dataKeyToken"
        )

    def get_backup_sets(self, device_guid, destination_guid):
        uri = u"/c42api/v3/BackupSets/{}/{}".format(device_guid, destination_guid)
        return Py42Response(self._session.get(uri), json_key="backupSets")

    def get_restore_history(self, days, id_type, id_value, page_num=None, page_size=None, **kwargs):
        uri = u"/api/RestoreHistory"
        params = dict(days=days, pgNum=page_num, pgSize=page_size, **kwargs)
        params[id_type] = id_value
        return Py42Response(self._session.get(uri, params=params))

    def get_web_restore_info(self, src_guid, dest_guid):
        uri = u"/api/WebRestoreInfo"
        params = {u"srcGuid": src_guid, u"destGuid": dest_guid}
        return Py42Response(self._session.get(uri, params=params))
