from py42._internal.base_classes import BaseAuthorityClient
from py42.util import get_obj_from_response


class AdministrationClient(BaseAuthorityClient):
    def get_diagnostics(self, include_volumes=None):
        uri = u"/api/Diagnostic"
        params = {u"incVolumes": include_volumes}
        return self._default_session.get(uri, params=params)

    def get_alert_log(self, status=None, alert_type=None, page_num=None, page_size=None):
        uri = u"/api/AlertLog"
        params = {u"status": status, u"type": alert_type, u"pgNum": page_num, u"pgSize": page_size}
        return self._default_session.get(uri, params=params)

    def get_current_tenant_id(self):
        uri = u"/c42api/v3/customer/my"
        response = self._default_session.get(uri)
        tenant = get_obj_from_response(response, u"data")
        return tenant.get(u"tenantUid")
