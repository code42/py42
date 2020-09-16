import pytest

from py42.clients.auditlogs import AuditLogsClient
from py42.services.auditlogs import AuditLogsService


@pytest.fixture
def auditlog_service(mocker):
    return mocker.MagicMock(spec=AuditLogsService)


class TestAuditLogsClient(object):
    def test_get_all_calls_expected_auditlogs_service(self, auditlog_service):
        client = AuditLogsClient(auditlog_service)
        for _ in client.get_all():
            pass
        auditlog_service.get_all.assert_called_once_with(
            begin_time=None,
            end_time=None,
            event_types=None,
            user_ids=None,
            usernames=None,
            user_ip_addresses=None,
            affected_user_ids=None,
            affected_usernames=None,
        )

    def test_get_page_calls_expected_auditlogs_service(self, auditlog_service):
        client = AuditLogsClient(auditlog_service)
        client.get_page()
        auditlog_service.get_page.assert_called_once_with(
            page_num=1,
            page_size=None,
            begin_time=None,
            end_time=None,
            event_types=None,
            user_ids=None,
            usernames=None,
            user_ip_addresses=None,
            affected_user_ids=None,
            affected_usernames=None,
        )

    def test_get_all_passes_undefined_param_to_service(self, auditlog_service):
        client = AuditLogsClient(auditlog_service)
        for _ in client.get_all(customParam="abc"):
            pass
        auditlog_service.get_all.assert_called_once_with(
            begin_time=None,
            end_time=None,
            event_types=None,
            user_ids=None,
            usernames=None,
            user_ip_addresses=None,
            affected_user_ids=None,
            affected_usernames=None,
            customParam="abc",
        )

    def test_get_page_passes_undefined_param_to_auditlogs_service(
        self, auditlog_service
    ):
        client = AuditLogsClient(auditlog_service)
        client.get_page(customParam="abc")
        auditlog_service.get_page.assert_called_once_with(
            page_num=1,
            page_size=None,
            begin_time=None,
            end_time=None,
            event_types=None,
            user_ids=None,
            usernames=None,
            user_ip_addresses=None,
            affected_user_ids=None,
            affected_usernames=None,
            customParam="abc",
        )

    def test_export_passes_default_format_option_to_auditlogs_service(
        self, auditlog_service
    ):
        client = AuditLogsClient(auditlog_service)
        client.export()
        auditlog_service.get_page.assert_called_once_with(
            format="CSV",
            page_num=1,
            page_size=10000,
            begin_time=None,
            end_time=None,
            event_types=None,
            user_ids=None,
            usernames=None,
            user_ip_addresses=None,
            affected_user_ids=None,
            affected_usernames=None,
        )

    def test_export_passes_passed_format_option_to_auditlogs_service(
        self, auditlog_service
    ):
        client = AuditLogsClient(auditlog_service)
        client.export(format="CEF")
        auditlog_service.get_page.assert_called_once_with(
            format="CEF",
            page_num=1,
            page_size=10000,
            begin_time=None,
            end_time=None,
            event_types=None,
            user_ids=None,
            usernames=None,
            user_ip_addresses=None,
            affected_user_ids=None,
            affected_usernames=None,
        )

    def test_export_passes_passed_format_option_with_filter_params_to_auditlogs_service(
        self, auditlog_service
    ):
        client = AuditLogsClient(auditlog_service)
        client.export(
            format="CEF", usernames="test@test.test", user_ip_addresses="0.0.0.0"
        )
        auditlog_service.get_page.assert_called_once_with(
            format="CEF",
            page_num=1,
            page_size=10000,
            begin_time=None,
            end_time=None,
            event_types=None,
            user_ids=None,
            usernames="test@test.test",
            user_ip_addresses="0.0.0.0",
            affected_user_ids=None,
            affected_usernames=None,
        )

    def test_export_passes_passed_format_option_with_custom_arg_to_auditlogs_service(
        self, auditlog_service
    ):
        client = AuditLogsClient(auditlog_service)
        client.export(format="CEF", customParam="abc")
        auditlog_service.get_page.assert_called_once_with(
            format="CEF",
            page_num=1,
            page_size=10000,
            begin_time=None,
            end_time=None,
            event_types=None,
            user_ids=None,
            usernames=None,
            user_ip_addresses=None,
            affected_user_ids=None,
            affected_usernames=None,
            customParam="abc",
        )
