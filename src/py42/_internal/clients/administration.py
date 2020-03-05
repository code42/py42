from py42._internal.base_classes import BaseClient
from py42._internal.response import Py42Response


class AdministrationClient(BaseClient):
    def get_diagnostics(self, include_volumes=None):
        uri = u"/api/Diagnostic"
        params = {u"incVolumes": include_volumes}
        return Py42Response(self._session.get(uri, params=params))

    def get_alert_log(self, status=None, alert_type=None, page_num=None, page_size=None):
        uri = u"/api/AlertLog"
        params = {u"status": status, u"type": alert_type, u"pgNum": page_num, u"pgSize": page_size}
        return Py42Response(self._session.get(uri, params=params))

    def get_current_tenant(self):
        uri = u"/c42api/v3/customer/my"
        return Py42Response(self._session.get(uri))
