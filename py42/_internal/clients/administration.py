from py42._internal.base_classes import BaseAuthorityClient


class AdministrationClient(BaseAuthorityClient):

    def get_diagnostics(self, include_volumes=None, **kwargs):
        uri = "/api/Diagnostic"
        params = {"incVolumes": include_volumes}
        return self._default_session.get(uri, params=params, **kwargs)

    def get_alert_log(self, status=None, alert_type=None, page_num=None, page_size=None, **kwargs):
        uri = "/api/AlertLog"
        params = {"status": status, "type": alert_type, "pgNum": page_num, "pgSize": page_size}
        return self._default_session.get(uri, params=params, **kwargs)
