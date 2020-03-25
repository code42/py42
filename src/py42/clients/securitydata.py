from py42.clients import BaseClient


class SecurityClient(BaseClient):
    def get_security_event_locations(self, user_uid):
        """Gets storage node IDs for the storage nodes containing the legacy security event data
        for the user with the given user UID.
        `REST Documentation <https://console.us.code42.com/swagger/#/Feature/getStorageNode>`__

        Args:
            user_uid (str): A user UID for the user to get storage node locations for.

        Returns:
            :class:`py42.sdk.response.Py42Response`: A response containing storage node IDs.
        """
        uri = u"/c42api/v3/SecurityEventsLocation"
        params = {u"userUid": user_uid}
        return self._session.get(uri, params=params)
