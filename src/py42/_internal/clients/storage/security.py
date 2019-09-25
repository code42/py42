from datetime import datetime

from py42._internal.base_classes import BaseStorageClient


class StorageSecurityClient(BaseStorageClient):
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
        **kwargs
    ):
        uri = u"/api/SecurityDetectionEvent"

        min_time_str = None
        max_time_str = None

        if min_timestamp:
            min_time_str = datetime.fromtimestamp(min_timestamp).strftime(u"%Y-%m-%dT%H:%M:%S.%fZ")

        if max_timestamp:
            max_time_str = datetime.fromtimestamp(max_timestamp).strftime(u"%Y-%m-%dT%H:%M:%S.%fZ")

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

        return self._session.get(uri, params=params, **kwargs)

    def get_security_detection_events_for_plan(
        self,
        plan_uid,
        cursor=None,
        include_files=None,
        event_types=None,
        min_timestamp=None,
        max_timestamp=None,
        **kwargs
    ):
        return self._get_security_detection_events(
            plan_uid=plan_uid,
            cursor=cursor,
            include_files=include_files,
            event_types=event_types,
            min_timestamp=min_timestamp,
            max_timestamp=max_timestamp,
            **kwargs
        )

    def get_security_detection_events_for_user(
        self,
        user_uid,
        cursor=None,
        include_files=None,
        event_types=None,
        min_timestamp=None,
        max_timestamp=None,
        **kwargs
    ):
        return self._get_security_detection_events(
            user_uid=user_uid,
            cursor=cursor,
            include_files=include_files,
            event_types=event_types,
            min_timestamp=min_timestamp,
            max_timestamp=max_timestamp,
            **kwargs
        )

    def get_security_detection_event_summary(
        self, user_uid, cursor=None, min_timestamp=None, max_timestamp=None, **kwargs
    ):
        return self._get_security_detection_events(
            user_uid=user_uid,
            cursor=cursor,
            min_timestamp=min_timestamp,
            max_timestamp=max_timestamp,
            summarize=True,
            **kwargs
        )
