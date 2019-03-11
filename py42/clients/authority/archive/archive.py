import json
from py42.clients.authority.authority_base import AuthorityTargetedClient


class ArchiveClient(AuthorityTargetedClient):

    def get_data_key_token(self, computer_guid, **kwargs):
        uri = "/api/DataKeyToken"
        data = {"computerGuid": computer_guid}
        return self.post(uri, data=json.dumps(data), **kwargs)

    def get_backup_sets(self, device_guid, destination_guid, **kwargs):
        uri = "/c42api/v3/BackupSets/{}/{}".format(device_guid, destination_guid)
        return self.get(uri, **kwargs)

