from py42 import util
from py42.clients.authority.authority_base import AuthorityTargetedClient


class DeviceClient(AuthorityTargetedClient):

    def get_devices(self, active=None, blocked=None, org_uid=None, user_uid=None, target_computer_guid=None,
                    include_backup_usage=None, include_counts=True, page_num=None, page_size=None, **kwargs):
        uri = "/api/Computer"
        params = {"active": active, "blocked": blocked, "orgUid": org_uid, "userUid": user_uid,
                  "targetComputerGuid": target_computer_guid,"incBackupUsage": include_backup_usage,
                  "incCounts": include_counts, "pgNum": page_num, "pgSize": page_size}

        return self.get(uri, params=params, **kwargs)

    def get_device_by_guid(self, guid, **kwargs):
        uri = "/api/Computer/{}?idType=guid".format(guid)
        return self.get(uri, **kwargs)

    def block_device(self, computer_id, **kwargs):
        uri = "/api/ComputerBlock/{}".format(computer_id)
        return self.put(uri, **kwargs)

    def unblock_device(self, computer_id, **kwargs):
        uri = "/api/ComputerBlock/{}".format(computer_id)
        return self.delete(uri, **kwargs)

    def deauthorize_device(self, computer_id, **kwargs):
        uri = "/api/ComputerDeauthorization/{}".format(computer_id)
        return self.put(uri, **kwargs)

    def get_device_settings(self, guid, keys=None, **kwargs):
        uri = "/api/v4/device-setting/view"
        params = {"guid": guid, "keys": keys}
        return self.get(uri, params=params, **kwargs)

    def for_each_device(self, active=None, org_uid=None, user_uid=None, target_computer_guid=None,
                        include_backup_usage=None, include_counts=True, then=None, return_each_page=False):

        func = self.get_devices

        def for_each(response):
            util.for_each_api_item(response, func, 1000, then, "computers", return_each_page)

        func(active=active, org_uid=org_uid, user_uid=user_uid, target_computer_guid=target_computer_guid,
             include_backup_usage=include_backup_usage, include_counts=include_counts, page_size=1000, then=for_each)
