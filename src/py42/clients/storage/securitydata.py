from datetime import datetime

from py42.clients import BaseClient


class StorageSecurityClient(BaseClient):
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

        def get_time_str_from_timestamp(timestamp):
            return datetime.utcfromtimestamp(timestamp).strftime(u"%Y-%m-%dT%H:%M:%S.%fZ")

        if min_timestamp:
            min_time_str = get_time_str_from_timestamp(min_timestamp)

        if max_timestamp:
            max_time_str = get_time_str_from_timestamp(max_timestamp)

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

        return self._session.get(uri, params=params)

    def get_plan_security_events(
        self,
        plan_uid,
        cursor=None,
        include_files=None,
        event_types=None,
        min_timestamp=None,
        max_timestamp=None,
    ):
        """Gets legacy security events for the plan with the given plan UID. Plans are for either
        a single user, multiple users, or a backup.

        Args:
            plan_uid (str): A plan UID for the plan to get security events for.
            cursor (str, optional): A cursor position for only getting events you did not
                previously get. Defaults to None.
            include_files (bool, optional): Whether to include the files related to the security
                events. Defaults to None.
            event_types: (str, optional): A comma-separated list of event types to filter by.
                Options include 'DEVICE_APPEARED', 'DEVICE_DISAPPEARED', 'DEVICE_FILE_ACTIVITY',
                'PERSONAL_CLOUD_FILE_ACTIVITY', 'RESTORE_JOB', 'RESTORE_FILE', 'FILE_OPENED',
                'RULE_MATCH', 'DEVICE_SCAN_RESULT', and 'PERSONAL_CLOUD_SCAN_RESULT'. Defaults to
                None.
            min_timestamp (float, optional): A POSIX timestamp to filter out events that did not
                occur on or after this date.
            max_timestamp (float, optional): A POSIX timestamp to filter out events that did not
                occur on or before this date.

        Returns:
            :class:`py42.sdk.response.Py42Response`
        """
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
        """Gets legacy security events for the user with the given user UID.

        Args:
            user_uid (str): A user UID for the user to get security events for.
            cursor (str, optional): A cursor position for only getting events you did not
                previously get. Defaults to None.
            include_files (bool, optional): Whether to include the files related to the security
                events. Defaults to None.
            event_types: (str, optional): A comma-separated list of event types to filter by.
                Options include 'DEVICE_APPEARED', 'DEVICE_DISAPPEARED', 'DEVICE_FILE_ACTIVITY',
                'PERSONAL_CLOUD_FILE_ACTIVITY', 'RESTORE_JOB', 'RESTORE_FILE', 'FILE_OPENED',
                'RULE_MATCH', 'DEVICE_SCAN_RESULT', and 'PERSONAL_CLOUD_SCAN_RESULT'. Defaults to
                None.
            min_timestamp (float, optional): A POSIX timestamp to filter out events that did not
                occur on or after this date.
            max_timestamp (float, optional): A POSIX timestamp to filter out events that did not
                occur on or before this date.

        Returns:
            :class:`py42.sdk.response.Py42Response`
        """
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
        """Gets a summary of security events excluding data about individual events for the user
        with the given user UID.

        Args:
            user_uid (str): The user UID for the user to get a security event summary for.
            cursor (str, optional): A cursor position for only getting events you did not
                previously get. Defaults to None.
            min_timestamp (float, optional): A POSIX timestamp to filter out events from the
                summary that did not at occur on or after this date.
            max_timestamp (float, optional): A POSIX timestamp to filter out events from the
                summary that did not occur on or before this date.

        Returns:
            :class:`py42.sdk.response.Py42Response`
        """
        return self._get_security_detection_events(
            user_uid=user_uid,
            cursor=cursor,
            min_timestamp=min_timestamp,
            max_timestamp=max_timestamp,
            summarize=True,
        )
