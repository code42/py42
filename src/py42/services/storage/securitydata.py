from py42.services import BaseService
from py42.util import parse_timestamp_to_microseconds_precision


class StorageSecurityDataService(BaseService):
    def _get_security_detection_events(
        self,
        user_uid=None,
        plan_uid=None,
        cursor=None,
        include_files=None,
        event_types=None,
        min_timestamp=None,
        max_timestamp=None,
        summarize=None,
    ):
        uri = u"/api/SecurityDetectionEvent"

        min_time_str = None
        max_time_str = None

        if min_timestamp:
            min_time_str = parse_timestamp_to_microseconds_precision(min_timestamp)

        if max_timestamp:
            max_time_str = parse_timestamp_to_microseconds_precision(max_timestamp)

        params = {
            u"userUid": user_uid,
            u"planUid": plan_uid,
            u"cursor": cursor,
            u"incFiles": include_files,
            u"eventType": event_types,
            u"minTs": min_time_str,
            u"maxTs": max_time_str,
            u"summarize": summarize,
        }

        return self._connection.get(uri, params=params)

    def get_plan_security_events(
        self,
        plan_uid,
        cursor=None,
        include_files=None,
        event_types=None,
        min_timestamp=None,
        max_timestamp=None,
    ):
        return self._get_security_detection_events(
            plan_uid=plan_uid,
            cursor=cursor,
            include_files=include_files,
            event_types=event_types,
            min_timestamp=min_timestamp,
            max_timestamp=max_timestamp,
        )

    def get_user_security_events(
        self,
        user_uid,
        cursor=None,
        include_files=None,
        event_types=None,
        min_timestamp=None,
        max_timestamp=None,
    ):
        return self._get_security_detection_events(
            user_uid=user_uid,
            cursor=cursor,
            include_files=include_files,
            event_types=event_types,
            min_timestamp=min_timestamp,
            max_timestamp=max_timestamp,
        )

    def get_security_detection_event_summary(
        self, user_uid, cursor=None, min_timestamp=None, max_timestamp=None
    ):
        return self._get_security_detection_events(
            user_uid=user_uid,
            cursor=cursor,
            min_timestamp=min_timestamp,
            max_timestamp=max_timestamp,
            summarize=True,
        )
