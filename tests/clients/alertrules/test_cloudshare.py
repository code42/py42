import json

from py42.services.alertrules import CloudShareService


class TestCloudShareClient(object):
    def test_get_by_id_posts_to_correct_endpoint_for_cloudshare_type(
        self, mock_session
    ):
        alert_rule_client = CloudShareService(mock_session, u"tenant-id")
        alert_rule_client.get(u"rule-id")
        url = mock_session.post.call_args[0][0]
        assert url == "/svc/api/v1/Rules/query-cloud-share-permissions-rule"
        posted_data = mock_session.post.call_args[1]["json"]
        assert posted_data["tenantId"] == u"tenant-id" and posted_data["ruleIds"] == [
            u"rule-id"
        ]
