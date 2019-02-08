from datetime import datetime
from .handlers.http import GenericAPIClient, util
from .handlers import V1StorageNodeAuthHandler


class StorageAPIClient(GenericAPIClient):

    @classmethod
    def create_v1_token_client(cls, authority_api, init_plan_uid, init_destination_guid, storage_logon_info, is_async):
        storage_url = storage_logon_info["serverUrl"]
        auth_handler = V1StorageNodeAuthHandler(authority_api, init_plan_uid, init_destination_guid, storage_logon_info)
        session = util.create_session(storage_url, auth_handler, authority_api.proxies, is_async)
        return cls(session)

    def get_security_detection_events(self, plan_uid, user_uid=None, cursor=None, include_files=None,
                                      min_timestamp=None, max_timestamp=None, **kwargs):

        uri = "/api/SecurityDetectionEvent"

        event_types = ",".join(
            ["DEVICE_APPEARED", "DEVICE_DISAPPEARED", "DEVICE_FILE_ACTIVITY", "PERSONAL_CLOUD_FILE_ACTIVITY",
             "RESTORE_JOB", "RESTORE_FILE", "FILE_OPENED", "RULE_MATCH"])

        min_time_str = None
        max_time_str = None

        if min_timestamp:
            min_time_str = datetime.fromtimestamp(min_timestamp).strftime("%Y-%m-%dT%H:%M:%S.%fZ")

        if max_timestamp:
            max_time_str = datetime.fromtimestamp(max_timestamp).strftime("%Y-%m-%dT%H:%M:%S.%fZ")

        params = {"planUid": plan_uid, "userUid": user_uid, "cursor": cursor, "incFiles": include_files,
                  "eventType": event_types, "minTs": min_time_str, "maxTs": max_time_str}

        return self.get(uri, params=params, **kwargs)
