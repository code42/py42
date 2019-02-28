from py42.clients.authority.administration import devices, orgs, users
from py42.clients.authority.authority_base import AuthorityTargetedClient


class AdministrationClient(AuthorityTargetedClient):

    def __init__(self, session):
        super(AdministrationClient, self).__init__(session)
        self._user_client = users.UserClient(session)
        self._device_client = devices.DeviceClient(session)
        self._org_client = orgs.OrgClient(session)

    @property
    def users(self):
        return self._user_client

    @property
    def devices(self):
        return self._device_client

    @property
    def orgs(self):
        return self._org_client

    def get_diagnostics(self, include_volumes=None, **kwargs):
        uri = "/api/Diagnostic"
        params = {"incVolumes": include_volumes}
        return self.get(uri, params=params, **kwargs)

    def get_alert_log(self, status=None, alert_type=None, page_num=None, page_size=None, **kwargs):
        uri = "/api/AlertLog"
        params = {"status": status, "type": alert_type, "pgNum": page_num, "pgSize": page_size}
        return self.get(uri, params=params, **kwargs)
