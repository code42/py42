import json

from py42._internal.base_classes import BaseAuthorityClient


class ArchiveClient(BaseAuthorityClient):
    def get_data_key_token(self, computer_guid):
        uri = u"/api/DataKeyToken"
        data = {u"computerGuid": computer_guid}
        return self._default_session.post(uri, data=json.dumps(data))

    def get_backup_sets(self, device_guid, destination_guid):
        uri = u"/c42api/v3/BackupSets/{}/{}".format(device_guid, destination_guid)
        return self._default_session.get(uri)

    def get_restore_history(self, days, org_id=None, page_num=None, page_size=None):
        uri = u"/api/RestoreHistory"
        params = {u"days": days, u"orgId": org_id, u"pgNum": page_num, u"pgSize": page_size}
        return self._default_session.get(uri, params=params)

    def get_web_restore_info(self, src_guid, dest_guid):
        uri = u"/api/WebRestoreInfo"
        params = {u"srcGuid": src_guid, u"destGuid": dest_guid}
        return self._default_session.get(uri, params=params)
