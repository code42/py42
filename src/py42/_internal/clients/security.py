from py42._internal.base_classes import BaseClient
from py42._internal.response import Py42Response


class SecurityClient(BaseClient):
    def get_security_event_locations(self, user_uid):
        uri = u"/c42api/v3/SecurityEventsLocation"
        params = {u"userUid": user_uid}
        return Py42Response(self._session.get(uri, params=params))
