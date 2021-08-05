from py42.services.alertrules import ExfiltrationService


class TestExfiltrationClient:
    def test_get_by_id_posts_expected_data_for_exfiltration_type(self, mock_connection):
        alert_rule_client = ExfiltrationService(mock_connection, "tenant-id")
        alert_rule_client.get("rule-id")

        assert mock_connection.post.call_count == 1
        url = mock_connection.post.call_args[0][0]
        assert url == "/svc/api/v1/Rules/query-endpoint-exfiltration-rule"
        posted_data = mock_connection.post.call_args[1]["json"]
        assert posted_data["tenantId"] == "tenant-id" and posted_data["ruleIds"] == [
            "rule-id"
        ]
