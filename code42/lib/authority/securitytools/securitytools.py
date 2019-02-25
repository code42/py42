from ..authoritybase import AuthorityTargetedClient


class SecurityToolsClient(AuthorityTargetedClient):

    def get_security_event_locations(self, user_uid, **kwargs):
        uri = "/c42api/v3/SecurityEventsLocation"
        params = {"userUid": user_uid}

        return self.get(uri, params=params, allowed_error_codes=[404], **kwargs)
