from py42.services import BaseService


class AdministrationService(BaseService):
    def get_diagnostics(self, include_volumes=None):
        uri = "/api/Diagnostic"
        params = {"incVolumes": include_volumes}
        return self._connection.get(uri, params=params)

    def get_alert_log(
        self, status=None, alert_type=None, page_num=None, page_size=None
    ):
        uri = "/api/AlertLog"
        params = {
            "status": status,
            "type": alert_type,
            "pgNum": page_num,
            "pgSize": page_size,
        }
        return self._connection.get(uri, params=params)

    def get_current_tenant(self):
        uri = "/c42api/v3/customer/my"
        return self._connection.get(uri)
