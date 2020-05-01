import json

from py42.clients.alertrules.cloud_share import CloudShareClient


class TestCloudShareClient(object):
    def test_get_by_id_posts_to_correct_endpoint_for_cloudshare_type(self, mock_session):
        alert_rule_client = CloudShareClient(mock_session, u"tenant-id")
        alert_rule_client.get(u"rule-id")
        url = mock_session.post.call_args[0][0]
        assert url == "/svc/api/v1/Rules/query-cloud-share-permissions-rule"
        posted_data = json.loads(mock_session.post.call_args[1]["data"])
        assert posted_data["tenantId"] == u"tenant-id" and posted_data["ruleIds"] == [u"rule-id"]
