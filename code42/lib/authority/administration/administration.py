from .devices import DeviceClient
from .orgs import OrgClient
from .users import UserClient
from ..authoritybase import AuthorityTargetedClient


class AdministrationClient(AuthorityTargetedClient):

    def __init__(self, session):
        super(AdministrationClient, self).__init__(session)
        self._users = UserClient(session)
        self._devices = DeviceClient(session)
        self._orgs = OrgClient(session)

    @property
    def users(self):
        return self._users

    @property
    def devices(self):
        return self._devices

    @property
    def orgs(self):
        return self._orgs

    def get_diagnostics(self, include_volumes=None, **kwargs):
        uri = "/api/Diagnostic"
        params = {"incVolumes": include_volumes}
        return self.get(uri, params=params, **kwargs)

    def get_alert_log(self, status=None, alert_type=None, page_num=None, page_size=None, **kwargs):
        uri = "/api/AlertLog"
        params = {"status": status, "type": alert_type, "pgNum": page_num, "pgSize": page_size}
        return self.get(uri, params=params, **kwargs)
