import json

from py42.services.alertrules import ExfiltrationService


class TestExfiltrationClient(object):
    def test_get_by_id_posts_expected_data_for_exfiltration_type(self, mock_connection):
        alert_rule_client = ExfiltrationService(mock_connection, u"tenant-id")
        alert_rule_client.get(u"rule-id")

        assert mock_connection.post.call_count == 1
        url = mock_connection.post.call_args[0][0]
        assert url == "/svc/api/v1/Rules/query-endpoint-exfiltration-rule"
        posted_data = mock_connection.post.call_args[1]["json"]
        assert posted_data["tenantId"] == u"tenant-id" and posted_data["ruleIds"] == [
            u"rule-id"
        ]
