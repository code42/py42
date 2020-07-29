import json

from py42.services.alertrules.exfiltration import ExfiltrationClient


class TestExfiltrationClient(object):
    def test_get_by_id_posts_expected_data_for_exfiltration_type(self, mock_session):
        alert_rule_client = ExfiltrationClient(mock_session, u"tenant-id")
        alert_rule_client.get(u"rule-id")

        assert mock_session.post.call_count == 1
        url = mock_session.post.call_args[0][0]
        assert url == "/svc/api/v1/Rules/query-endpoint-exfiltration-rule"
        posted_data = json.loads(mock_session.post.call_args[1]["data"])
        assert posted_data["tenantId"] == u"tenant-id" and posted_data["ruleIds"] == [
            u"rule-id"
        ]
