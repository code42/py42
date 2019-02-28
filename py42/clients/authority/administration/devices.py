from py42 import util
from py42.clients.authority.authority_base import AuthorityTargetedClient


class DeviceClient(AuthorityTargetedClient):

    def for_each_computer(self, active=None, org_uid=None, include_backup_usage=None, then=None,
                          return_each_page=False):
        func = self.get_computers

        def for_each(response):
            util.for_each_api_item(response, func, 1000, then, "computers", return_each_page)

        func(active=active, org_uid=org_uid, page_size=1000, then=for_each,
             include_backup_usage=include_backup_usage)

    def get_computers(self, active=None, org_uid=None, user_uid=None, target_computer_guid=None,
                      include_backup_usage=None, include_counts=True, page_num=None, page_size=None, **kwargs):
        uri = "/api/Computer"
        params = {"active": active, "orgUid": org_uid, "userUid": user_uid, "targetComputerGuid": target_computer_guid,
                  "incBackupUsage": include_backup_usage, "incCounts": include_counts,
                  "pgNum": page_num, "pgSize": page_size}

        return self.get(uri, params=params, **kwargs)
