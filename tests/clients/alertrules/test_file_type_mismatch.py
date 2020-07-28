import json

from py42.clients.alertrules.file_type_mismatch import FileTypeMismatchClient


class TestFileTypeMisMatchClient(object):
    def test_get_by_id_posts_to_correct_endpoint_for_type_mismatch_rule_type(
        self, mock_session
    ):
        alert_rule_client = FileTypeMismatchClient(mock_session, u"tenant-id")
        alert_rule_client.get(u"rule-id")
        url = mock_session.post.call_args[0][0]
        assert url == "/svc/api/v1/Rules/query-file-type-mismatch-rule"
        posted_data = json.loads(mock_session.post.call_args[1]["data"])
        assert posted_data["tenantId"] == u"tenant-id" and posted_data["ruleIds"] == [
            u"rule-id"
        ]
