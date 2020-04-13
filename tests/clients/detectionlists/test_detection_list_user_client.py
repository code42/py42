import pytest
import json

from py42.clients.detectionlists.detection_list_user_client import DetectionListUserClient


class TestDetectionListUserClient(object):
    def test_create_posts_expected_data(self, mock_session, user_context):
        detection_list_user_client = DetectionListUserClient(mock_session, user_context)
        detection_list_user_client.create("942897397520289999")

        posted_data = json.loads(mock_session.post.call_args[1]["data"])
        assert mock_session.post.call_count == 1
        assert mock_session.post.call_args[0][0] == "/svc/api/v2/user/create"
        assert (
            posted_data["tenantId"] == user_context.get_current_tenant_id()
            and posted_data["userName"] == "942897397520289999"
            and posted_data["riskFactors"] == []
            and posted_data["cloudUsernames"] == []
            and posted_data["notes"] == ""
        )

    def test_get_posts_expected_data(self, mock_session, user_context):
        detection_list_user_client = DetectionListUserClient(mock_session, user_context)
        detection_list_user_client.get("942897397520289999")

        posted_data = json.loads(mock_session.post.call_args[1]["data"])
        assert mock_session.post.call_count == 1
        assert mock_session.post.call_args[0][0] == "/svc/api/v2/user/getbyusername"
        assert (
            posted_data["tenantId"] == user_context.get_current_tenant_id()
            and posted_data["username"] == "942897397520289999"
        )

    def test_get_by_id_posts_expected_data(self, mock_session, user_context):
        detection_list_user_client = DetectionListUserClient(mock_session, user_context)
        detection_list_user_client.get_by_id("942897397520289999")

        posted_data = json.loads(mock_session.post.call_args[1]["data"])
        assert mock_session.post.call_count == 1
        assert mock_session.post.call_args[0][0] == "/svc/api/v2/user/getbyuserid"
        assert (
            posted_data["tenantId"] == user_context.get_current_tenant_id()
            and posted_data["userId"] == "942897397520289999"
        )

    def test_update_notes_posts_expected_data(self, mock_session, user_context):
        detection_list_user_client = DetectionListUserClient(mock_session, user_context)
        detection_list_user_client.update_notes("942897397520289999", "Test")

        posted_data = json.loads(mock_session.post.call_args[1]["data"])
        assert mock_session.post.call_count == 1
        assert mock_session.post.call_args[0][0] == "/svc/api/v2/user/updatenotes"
        assert (
            posted_data["tenantId"] == user_context.get_current_tenant_id()
            and posted_data["userId"] == "942897397520289999"
            and posted_data["notes"] == "Test"
        )

    def test_add_risk_tag_posts_expected_data(self, mock_session, user_context):
        detection_list_user_client = DetectionListUserClient(mock_session, user_context)
        detection_list_user_client.add_risk_tag("942897397520289999", u"Test")

        posted_data = json.loads(mock_session.post.call_args[1]["data"])
        assert mock_session.post.call_count == 1
        assert mock_session.post.call_args[0][0] == "/svc/api/v2/user/addriskfactors"
        assert (
            posted_data["tenantId"] == user_context.get_current_tenant_id()
            and posted_data["userId"] == "942897397520289999"
            and posted_data["riskFactors"] == ["Test"]
        )

    def test_remove_risk_tag_posts_expected_data(self, mock_session, user_context):
        detection_list_user_client = DetectionListUserClient(mock_session, user_context)
        detection_list_user_client.remove_risk_tag("942897397520289999", u"Test")

        posted_data = json.loads(mock_session.post.call_args[1]["data"])
        assert mock_session.post.call_count == 1
        assert mock_session.post.call_args[0][0] == "/svc/api/v2/user/removeriskfactors"
        assert (
            posted_data["tenantId"] == user_context.get_current_tenant_id()
            and posted_data["userId"] == "942897397520289999"
            and posted_data["riskFactors"] == ["Test"]
        )

    def test_add_cloud_alias_posts_expected_data(self, mock_session, user_context):
        detection_list_user_client = DetectionListUserClient(mock_session, user_context)
        detection_list_user_client.add_cloud_alias("942897397520289999", u"Test")

        posted_data = json.loads(mock_session.post.call_args[1]["data"])
        assert mock_session.post.call_count == 1
        assert mock_session.post.call_args[0][0] == "/svc/api/v2/user/addcloudusernames"
        assert (
            posted_data["tenantId"] == user_context.get_current_tenant_id()
            and posted_data["userId"] == "942897397520289999"
            and posted_data["cloudUsernames"] == ["Test"]
        )

    def test_remove_cloud_alias_posts_expected_data(self, mock_session, user_context):
        detection_list_user_client = DetectionListUserClient(mock_session, user_context)
        detection_list_user_client.remove_cloud_alias("942897397520289999", u"Test")

        posted_data = json.loads(mock_session.post.call_args[1]["data"])
        assert mock_session.post.call_count == 1
        assert mock_session.post.call_args[0][0] == "/svc/api/v2/user/removecloudusernames"
        assert (
            posted_data["tenantId"] == user_context.get_current_tenant_id()
            and posted_data["userId"] == "942897397520289999"
            and posted_data["cloudUsernames"] == ["Test"]
        )
