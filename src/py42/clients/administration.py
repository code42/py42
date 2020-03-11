from py42.clients import BaseClient


class AdministrationClient(BaseClient):
    def get_diagnostics(self, include_volumes=None):
        uri = u"/api/Diagnostic"
        params = {u"incVolumes": include_volumes}
        return self._session.get(uri, params=params)

    def get_alert_log(self, status=None, alert_type=None, page_num=None, page_size=None):
        uri = u"/api/AlertLog"
        params = {u"status": status, u"type": alert_type, u"pgNum": page_num, u"pgSize": page_size}
        return self._session.get(uri, params=params)

    def get_current_tenant(self):
        uri = u"/c42api/v3/customer/my"
        return self._session.get(uri)
