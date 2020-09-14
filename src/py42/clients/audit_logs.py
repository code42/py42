class AuditLogsClient(object):
    def __init__(self, audit_log_service):
        self._audit_log_service = audit_log_service

    def get_all(
        self,
        begin_time=None,
        end_time=None,
        event_types=None,
        user_ids=None,
        user_names=None,
        user_ip_addresses=None,
        affected_user_ids=None,
        affected_user_names=None,
    ):
        """Retrieve audit logs, filtered based on given arguments.

        Args:
            begin_time (datetime, optional): A datetime.datetime instance for a given timestamp. Defaults to None.
            end_time (datetime, optional): A datetime.datetime instance for a given timestamp. Defaults to None.
            event_types (str, optional): Comma separated str of valid event types. Defaults to None.
            user_ids (str, optional): Comma separated str of user ids. Defaults to None.
            user_names (str, optional): Comma separated str of user names. Defaults to None.
            user_ip_addresses (str, optional): Comma separated str of user ip addresses. Defaults to None.
            affected_user_ids (str, optional): Comma separated str of affected user ids. Defaults to None.
            affected_user_names (str, optional): Comma separated str of affected user names. Defaults to None.

        Returns:
            generator: An object that iterates over :class:`py42.response.Py42Response` objects
            that each contain a page of audit logs.
        """
        return self._audit_log_service.get_all(
            begin_time=begin_time,
            end_time=end_time,
            event_types=event_types,
            user_ids=user_ids,
            user_names=user_names,
            user_ip_addresses=user_ip_addresses,
            affected_user_ids=affected_user_ids,
            affected_user_names=affected_user_names,
        )
