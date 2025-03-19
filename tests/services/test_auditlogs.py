from datetime import datetime as dt

from pycpg.services.auditlogs import AuditLogsService


class TestAuditLogService:
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
        }
        mock_connection.post.assert_called_once_with(
            "/rpc/search/search-audit-log", json=expected_data, headers=None
        )

    def test_get_all_when_begin_and_end_times_are_given_passes_valid_date_range_param(
        self, mock_connection
    ):
        service = AuditLogsService(mock_connection)

        start_time = dt.strptime("2020-06-06 00:00:00", "%Y-%m-%d %H:%M:%S")
        end_time = dt.strptime("2020-09-09 12:12:21", "%Y-%m-%d %H:%M:%S")
        for _ in service.get_all(begin_time=start_time, end_time=end_time):
            pass
        expected_data = {
            "page": 0,
            "pageSize": 500,
            "dateRange": {
                "startTime": "2020-06-06T00:00:00.000000Z",
                "endTime": "2020-09-09T12:12:21.000000Z",
            },
            "eventTypes": [],
            "actorIds": [],
            "actorNames": [],
            "actorIpAddresses": [],
            "affectedUserIds": [],
            "affectedUserNames": [],
        }
        mock_connection.post.assert_called_once_with(
            "/rpc/search/search-audit-log", json=expected_data, headers=None
        )

    def test_get_all_calls_actor_names_with_list_of_user_names(self, mock_connection):
        service = AuditLogsService(mock_connection)
        for _ in service.get_all(usernames=["test@test.com", "test@crashPlan.com"]):
            pass
        expected_data = {
            "page": 0,
            "pageSize": 500,
            "dateRange": {},
            "eventTypes": [],
            "actorIds": [],
            "actorNames": ["test@test.com", "test@crashPlan.com"],
            "actorIpAddresses": [],
            "affectedUserIds": [],
            "affectedUserNames": [],
        }
        mock_connection.post.assert_called_once_with(
            "/rpc/search/search-audit-log", json=expected_data, headers=None
        )

    def test_get_all_calls_all_params_in_valid_formats(self, mock_connection):
        service = AuditLogsService(mock_connection)
        for _ in service.get_all(
            usernames=["test@test.com", "test@crashPlan.com"],
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
            "actorNames": ["test@test.com", "test@crashPlan.com"],
            "actorIpAddresses": ["127.0.0.1", "0.0.0.0"],
            "affectedUserIds": [],
            "affectedUserNames": ["test_user@name.com"],
        }
        mock_connection.post.assert_called_once_with(
            "/rpc/search/search-audit-log", json=expected_data, headers=None
        )

    def test_get_page_calls_expected_uri_and_params(self, mock_connection):
        service = AuditLogsService(mock_connection)
        service.get_page(
            page_num=1,
            page_size=3,
            begin_time=None,
            end_time=None,
            event_types=None,
            user_ids=None,
            usernames=None,
            user_ip_addresses=None,
            affected_user_ids=None,
            affected_usernames=None,
        )
        expected_data = {
            "page": 0,
            "pageSize": 3,
            "dateRange": {},
            "eventTypes": [],
            "actorIds": [],
            "actorNames": [],
            "actorIpAddresses": [],
            "affectedUserIds": [],
            "affectedUserNames": [],
        }
        mock_connection.post.assert_called_once_with(
            "/rpc/search/search-audit-log", json=expected_data, headers=None
        )

    def test_get_page_calls_expected_uri_and_params_in_valid_formats(
        self, mock_connection
    ):
        service = AuditLogsService(mock_connection)
        service.get_page(
            page_num=5,
            page_size=300,
            begin_time=None,
            end_time=None,
            usernames=["test@test.com", "test@crashPlan.com"],
            user_ids=["1208", "12089"],
            event_types="abc",
            user_ip_addresses=["127.0.0.1", "0.0.0.0"],
            affected_user_ids="",
            affected_usernames="test_user@name.com",
        )
        expected_data = {
            "page": 4,
            "pageSize": 300,
            "dateRange": {},
            "eventTypes": ["abc"],
            "actorIds": ["1208", "12089"],
            "actorNames": ["test@test.com", "test@crashPlan.com"],
            "actorIpAddresses": ["127.0.0.1", "0.0.0.0"],
            "affectedUserIds": [],
            "affectedUserNames": ["test_user@name.com"],
        }
        mock_connection.post.assert_called_once_with(
            "/rpc/search/search-audit-log", json=expected_data, headers=None
        )

    def test_get_page_passes_undefined_field_in_api_request(self, mock_connection):
        service = AuditLogsService(mock_connection)
        service.get_page(
            page_num=1,
            page_size=500,
            begin_time=None,
            end_time=None,
            event_types=None,
            user_ids=None,
            usernames=None,
            user_ip_addresses=None,
            affected_user_ids=None,
            affected_usernames=None,
            customParam="",
        )
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
            "customParam": "",
        }
        mock_connection.post.assert_called_once_with(
            "/rpc/search/search-audit-log", json=expected_data, headers=None
        )

    def test_get_all_passes_undefined_param_in_api(self, mock_connection):
        service = AuditLogsService(mock_connection)
        for _ in service.get_all(custom_param="abc"):
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
            "custom_param": "abc",
        }
        mock_connection.post.assert_called_once_with(
            "/rpc/search/search-audit-log", json=expected_data, headers=None
        )

    def test_get_page_when_format_is_specified_passes_csv_headers_and_params(
        self, mock_connection
    ):
        service = AuditLogsService(mock_connection)
        service.get_page(
            format="CSV",
            page_num=5,
            page_size=300,
            begin_time=None,
            end_time=None,
            usernames=["test@test.com", "test@crashPlan.com"],
            user_ids=["1208", "12089"],
            event_types="abc",
            user_ip_addresses=["127.0.0.1", "0.0.0.0"],
            affected_user_ids="",
            affected_usernames="test_user@name.com",
        )
        expected_data = {
            "page": 4,
            "pageSize": 300,
            "dateRange": {},
            "eventTypes": ["abc"],
            "actorIds": ["1208", "12089"],
            "actorNames": ["test@test.com", "test@crashPlan.com"],
            "actorIpAddresses": ["127.0.0.1", "0.0.0.0"],
            "affectedUserIds": [],
            "affectedUserNames": ["test_user@name.com"],
        }
        mock_connection.post.assert_called_once_with(
            "/rpc/search/search-audit-log",
            json=expected_data,
            headers={"Accept": "text/csv"},
        )

    def test_get_page_when_format_is_specified_passes_cef_headers_and_params(
        self, mock_connection
    ):
        service = AuditLogsService(mock_connection)
        service.get_page(
            format="CEF",
            page_num=5,
            page_size=300,
            begin_time=None,
            end_time=None,
            usernames=["test@test.com", "test@crashPlan.com"],
            user_ids=["1208", "12089"],
            event_types="abc",
            user_ip_addresses=["127.0.0.1", "0.0.0.0"],
            affected_user_ids="",
            affected_usernames="test_user@name.com",
        )
        expected_data = {
            "page": 4,
            "pageSize": 300,
            "dateRange": {},
            "eventTypes": ["abc"],
            "actorIds": ["1208", "12089"],
            "actorNames": ["test@test.com", "test@crashPlan.com"],
            "actorIpAddresses": ["127.0.0.1", "0.0.0.0"],
            "affectedUserIds": [],
            "affectedUserNames": ["test_user@name.com"],
        }
        mock_connection.post.assert_called_once_with(
            "/rpc/search/search-audit-log",
            json=expected_data,
            headers={"Accept": "text/x-cef"},
        )

    def test_get_page_when_invalid_format_is_specified_passes_no_headers_and_params(
        self, mock_connection
    ):
        service = AuditLogsService(mock_connection)
        service.get_page(
            format="abc",
            page_num=5,
            page_size=300,
            begin_time=None,
            end_time=None,
            usernames=["test@test.com", "test@crashPlan.com"],
            user_ids=["1208", "12089"],
            event_types="abc",
            user_ip_addresses=["127.0.0.1", "0.0.0.0"],
            affected_user_ids="",
            affected_usernames="test_user@name.com",
        )
        expected_data = {
            "page": 4,
            "pageSize": 300,
            "dateRange": {},
            "eventTypes": ["abc"],
            "actorIds": ["1208", "12089"],
            "actorNames": ["test@test.com", "test@crashPlan.com"],
            "actorIpAddresses": ["127.0.0.1", "0.0.0.0"],
            "affectedUserIds": [],
            "affectedUserNames": ["test_user@name.com"],
        }
        mock_connection.post.assert_called_once_with(
            "/rpc/search/search-audit-log", json=expected_data, headers=None
        )

    def test_get_all_when_begin_and_end_time_are_string_type_passes_valid_date_range_param(
        self, mock_connection
    ):
        service = AuditLogsService(mock_connection)

        start_time = "2020-06-06 00:00:00"
        end_time = "2020-09-09 12:12:21"
        for _ in service.get_all(begin_time=start_time, end_time=end_time):
            pass
        expected_data = {
            "page": 0,
            "pageSize": 500,
            "dateRange": {
                "startTime": "2020-06-06T00:00:00.000000Z",
                "endTime": "2020-09-09T12:12:21.000000Z",
            },
            "eventTypes": [],
            "actorIds": [],
            "actorNames": [],
            "actorIpAddresses": [],
            "affectedUserIds": [],
            "affectedUserNames": [],
        }
        mock_connection.post.assert_called_once_with(
            "/rpc/search/search-audit-log", json=expected_data, headers=None
        )

    def test_get_all_when_begin_and_end_time_are_epoch_passes_valid_date_range_param(
        self, mock_connection
    ):
        service = AuditLogsService(mock_connection)

        start_time = 1591401600  # 2020-06-06 00:00:00"
        end_time = 1599653541  # 2020-09-09 12:12:21"
        for _ in service.get_all(begin_time=start_time, end_time=end_time):
            pass
        expected_data = {
            "page": 0,
            "pageSize": 500,
            "dateRange": {
                "startTime": "2020-06-06T00:00:00.000000Z",
                "endTime": "2020-09-09T12:12:21.000000Z",
            },
            "eventTypes": [],
            "actorIds": [],
            "actorNames": [],
            "actorIpAddresses": [],
            "affectedUserIds": [],
            "affectedUserNames": [],
        }
        mock_connection.post.assert_called_once_with(
            "/rpc/search/search-audit-log", json=expected_data, headers=None
        )

    def test_get_all_when_begin_and_end_time_are_epoch_with_milliseconds_passes_valid_date_range_param(
        self, mock_connection
    ):
        service = AuditLogsService(mock_connection)

        start_time = 1591401600.123  # 2020-06-06 00:00:00.123456"
        end_time = 1599653541.443  # 2020-09-09 12:12:21.443234"
        for _ in service.get_all(begin_time=start_time, end_time=end_time):
            pass
        expected_data = {
            "page": 0,
            "pageSize": 500,
            "dateRange": {
                "startTime": "2020-06-06T00:00:00.123000Z",
                "endTime": "2020-09-09T12:12:21.443000Z",
            },
            "eventTypes": [],
            "actorIds": [],
            "actorNames": [],
            "actorIpAddresses": [],
            "affectedUserIds": [],
            "affectedUserNames": [],
        }
        mock_connection.post.assert_called_once_with(
            "/rpc/search/search-audit-log", json=expected_data, headers=None
        )

    def test_get_all_when_begin_and_end_time_are_epoch_with_microseconds_passes_valid_date_range_param(
        self, mock_connection
    ):
        service = AuditLogsService(mock_connection)

        start_time = 1591401600.123456  # 2020-06-06 00:00:00.123456"
        end_time = 1599653541.443234  # 2020-09-09 12:12:21.443234"
        for _ in service.get_all(begin_time=start_time, end_time=end_time):
            pass
        expected_data = {
            "page": 0,
            "pageSize": 500,
            "dateRange": {
                "startTime": "2020-06-06T00:00:00.123456Z",
                "endTime": "2020-09-09T12:12:21.443234Z",
            },
            "eventTypes": [],
            "actorIds": [],
            "actorNames": [],
            "actorIpAddresses": [],
            "affectedUserIds": [],
            "affectedUserNames": [],
        }
        mock_connection.post.assert_called_once_with(
            "/rpc/search/search-audit-log", json=expected_data, headers=None
        )
