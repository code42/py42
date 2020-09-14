from py42.services.auditlogs import AuditLogsService


class TestAuditLogService(object):
    def test_get_all_calls_expected_uri_and_params(self, mock_connection):
        service = AuditLogsService(mock_connection)
        for _ in service.get_all():
            pass
        expected_data = {
            "page": 0,
            "pageSize": 500,
            "dateRange": {},
            "eventTypes": [],
            "actorIds": [],
            "actorNames": [],
            "actorIpAddresses": [],
            "affectedUserIds": [],
            "affectedUserNames": [],
            "type$": "audit_log::audit_log_queries.search_audit_log/1",
        }
        mock_connection.post.assert_called_once_with(
            "/rpc/search/search-audit-log", json=expected_data
        )

    def test_get_all_passes_valid_date_range_param_when_begin_and_end_times_are_given(
        self, mock_connection
    ):
        service = AuditLogsService(mock_connection)
        from datetime import datetime as dt

        start_time = dt.strptime("2020-06-06 00:00:00", "%Y-%m-%d %H:%M:%S")
        end_time = dt.strptime("2020-09-09 12:12:21", "%Y-%m-%d %H:%M:%S")
        for _ in service.get_all(begin_time=start_time, end_time=end_time):
            pass
        expected_data = {
            "page": 0,
            "pageSize": 500,
            "dateRange": {
                "startTime": "2020-06-06T00:00:00.000Z",
                "endTime": "2020-09-09T12:12:21.000Z",
            },
            "eventTypes": [],
            "actorIds": [],
            "actorNames": [],
            "actorIpAddresses": [],
            "affectedUserIds": [],
            "affectedUserNames": [],
            "type$": "audit_log::audit_log_queries.search_audit_log/1",
        }
        mock_connection.post.assert_called_once_with(
            "/rpc/search/search-audit-log", json=expected_data
        )

    def test_get_all_calls_actor_names_with_list_of_user_names(self, mock_connection):
        service = AuditLogsService(mock_connection)
        for _ in service.get_all(usernames=["test@test.com", "test@code42.com"]):
            pass
        expected_data = {
            "page": 0,
            "pageSize": 500,
            "dateRange": {},
            "eventTypes": [],
            "actorIds": [],
            "actorNames": ["test@test.com", "test@code42.com"],
            "actorIpAddresses": [],
            "affectedUserIds": [],
            "affectedUserNames": [],
            "type$": "audit_log::audit_log_queries.search_audit_log/1",
        }
        mock_connection.post.assert_called_once_with(
            "/rpc/search/search-audit-log", json=expected_data
        )

    def test_get_all_calls_all_params_in_valid_formats(self, mock_connection):
        service = AuditLogsService(mock_connection)
        for _ in service.get_all(
            usernames=["test@test.com", "test@code42.com"],
            user_ids=["1208", "12089"],
            event_types="abc",
            user_ip_addresses=["127.0.0.1", "0.0.0.0"],
            affected_user_ids="",
            affected_usernames="test_user@name.com",
        ):
            pass
        expected_data = {
            "page": 0,
            "pageSize": 500,
            "dateRange": {},
            "eventTypes": ["abc"],
            "actorIds": ["1208", "12089"],
            "actorNames": ["test@test.com", "test@code42.com"],
            "actorIpAddresses": ["127.0.0.1", "0.0.0.0"],
            "affectedUserIds": [],
            "affectedUserNames": ["test_user@name.com"],
            "type$": "audit_log::audit_log_queries.search_audit_log/1",
        }
        mock_connection.post.assert_called_once_with(
            "/rpc/search/search-audit-log", json=expected_data
        )
