from py42.clients.authority.authority_base import AuthorityTargetedClient


class RestoreClient(AuthorityTargetedClient):

    def get_restore_history(self, days, org_id=None, page_num=None, page_size=None, **kwargs):
        uri = "/api/RestoreHistory"
        params = {"days": days, "orgId": org_id, "pgNum": page_num, "pgSize": page_size}
        return self.get(uri, params=params, **kwargs)

    def get_web_restore_info(self, src_guid, dest_guid, **kwargs):
        uri = "/api/WebRestoreInfo"
        params = {"srcGuid": src_guid, "destGuid": dest_guid}
        return self.get(uri, params=params, **kwargs)
