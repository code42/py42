from py42.services import BaseService


class SecurityDataService(BaseService):
    def get_security_event_locations(self, user_uid):
        uri = u"/c42api/v3/SecurityEventsLocation"
        params = {u"userUid": user_uid}
        return self._connection.get(uri, params=params)
