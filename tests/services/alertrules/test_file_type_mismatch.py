from py42.services.alertrules import FileTypeMismatchService


class TestFileTypeMisMatchClient:
    def test_get_by_id_posts_to_correct_endpoint_for_type_mismatch_rule_type(
        self, mock_connection
    ):
        alert_rule_client = FileTypeMismatchService(mock_connection, "tenant-id")
        alert_rule_client.get("rule-id")
        url = mock_connection.post.call_args[0][0]
        assert url == "/svc/api/v1/Rules/query-file-type-mismatch-rule"
        posted_data = mock_connection.post.call_args[1]["json"]
        assert posted_data["tenantId"] == "tenant-id" and posted_data["ruleIds"] == [
            "rule-id"
        ]
