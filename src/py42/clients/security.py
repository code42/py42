from py42.clients import BaseClient
from py42.sdk.response import Py42Response


class SecurityClient(BaseClient):
    def get_security_event_locations(self, user_uid):
        uri = u"/c42api/v3/SecurityEventsLocation"
        params = {u"userUid": user_uid}
        return Py42Response(
            self._session.get(uri, params=params), json_key=u"securityPlanLocationsByDestination"
        )
