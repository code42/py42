import pytest

from py42.clients.audit_logs import AuditLogsClient
from py42.services.audit_logs import AuditLogsService


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
            user_names=None,
            user_ip_addresses=None,
            affected_user_ids=None,
            affected_user_names=None,
        )
