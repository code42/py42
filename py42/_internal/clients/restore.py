from py42._internal.base_classes import BaseAuthorityClient


class RestoreClient(BaseAuthorityClient):

    def get_restore_history(self, days, org_id=None, page_num=None, page_size=None, **kwargs):
        uri = "/api/RestoreHistory"
        params = {"days": days, "orgId": org_id, "pgNum": page_num, "pgSize": page_size}
        return self._default_session.get(uri, params=params, **kwargs)

    def get_web_restore_info(self, src_guid, dest_guid, **kwargs):
        uri = "/api/WebRestoreInfo"
        params = {"srcGuid": src_guid, "destGuid": dest_guid}
        return self._default_session.get(uri, params=params, **kwargs)
