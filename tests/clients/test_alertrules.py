import pytest
import json

from py42.clients.alertrules import AlertRulesClient


class TestAlertRulesClient(object):
    @pytest.fixture
    def mock_response(self, mock_session, py42_response):
        mock_session.post.return_value = py42_response
        return mock_session

    def test_all_rules_posts_expected_data(self, mock_session, user_context):
        alert_rule_client = AlertRulesClient(mock_session, user_context)
        alert_rule_client.add_user(u"rule-id", u"user-id", u"user-aliases")

        assert mock_session.post.call_count == 1
        posted_data = json.loads(mock_session.post.call_args[1]["data"])
        assert mock_session.post.call_args[0][0] == "/svc/api/v1/Rules/add-users"
        assert (
            posted_data["tenantId"] == user_context.get_current_tenant_id()
            and posted_data["ruleId"] == u"rule-id"
            and posted_data["userList"][0]["userIdFromAuthority"] == u"user-id"
            and posted_data["userList"][0]["userAliasList"] == [u"user-aliases"]
        )

    def test_remove_rules_posts_expected_data(self, mock_session, user_context):
        alert_rule_client = AlertRulesClient(mock_session, user_context)
        alert_rule_client.remove_users(u"rule-id", u"user-id")

        assert mock_session.post.call_count == 1
        posted_data = json.loads(mock_session.post.call_args[1]["data"])
        assert mock_session.post.call_args[0][0] == "/svc/api/v1/Rules/remove-users"
        assert (
            posted_data["tenantId"] == user_context.get_current_tenant_id()
            and posted_data["ruleId"] == u"rule-id"
            and posted_data["userIdList"] == [u"user-id"]
        )

    def test_remove_all_rules_posts_expected_data(self, mock_session, user_context):
        alert_rule_client = AlertRulesClient(mock_session, user_context)
        alert_rule_client.remove_all_users(u"rule-id")

        assert mock_session.post.call_count == 1
        posted_data = json.loads(mock_session.post.call_args[1]["data"])
        assert mock_session.post.call_args[0][0] == "/svc/api/v1/Rules/remove-all-users"
        assert (
            posted_data["tenantId"] == user_context.get_current_tenant_id()
            and posted_data["ruleId"] == u"rule-id"
        )

    def test_get_by_id_posts_expected_data_for_exfiltration_type(self, mock_session, user_context):
        alert_rule_client = AlertRulesClient(mock_session, user_context)
        alert_rule_client.get(u"rule-id", "exfiltration")

        assert mock_session.post.call_count == 1
        posted_data = json.loads(mock_session.post.call_args[1]["data"])
        url = mock_session.post.call_args[0][0]
        assert url == "/svc/api/v1/Rules/query-endpoint-exfiltration-rule"
        assert posted_data["tenantId"] == user_context.get_current_tenant_id() and posted_data[
            "ruleIds"
        ] == [u"rule-id"]

    def test_get_by_id_posts_to_correct_endpoint_for_cloudshare_type(
        self, mock_session, user_context
    ):
        alert_rule_client = AlertRulesClient(mock_session, user_context)
        alert_rule_client.get(u"rule-id", "cloudshare")
        url = mock_session.post.call_args[0][0]
        assert url == "/svc/api/v1/Rules/query-cloud-share-permissions-rule"

    def test_get_by_id_posts_to_correct_endpoint_for_type_mismatch_rule_type(
        self, mock_session, user_context
    ):
        alert_rule_client = AlertRulesClient(mock_session, user_context)
        alert_rule_client.get(u"rule-id", "typemismatch")
        url = mock_session.post.call_args[0][0]
        assert url == "/svc/api/v1/Rules/query-file-type-mismatch-rule"

    def test_get_by_name_posts_expected_data(self, mock_session, user_context):
        alert_rule_client = AlertRulesClient(mock_session, user_context)
        alert_rule_client.get_by_name(u"name")
        pass

    def test_get_by_name_filters_correct_record(self, mock_session, user_context):
        alert_rule_client = AlertRulesClient(mock_session, user_context)
        alert_rule_client.get_by_name(u"name")
        pass

    def test_get_all_posts_expected_data(self, mock_session, user_context):
        alert_rule_client = AlertRulesClient(mock_session, user_context)

        for _ in alert_rule_client.get_all(sort_key="key", sort_direction="ASC"):
            break

        assert mock_session.post.call_count == 1
        posted_data = json.loads(mock_session.post.call_args[1]["data"])
        assert mock_session.post.call_args[0][0] == "/svc/api/v1/rules/query-rule-metadata"
        assert (
            posted_data["tenantId"] == user_context.get_current_tenant_id()
            and posted_data["groups"] == []
            and posted_data["groupClause"] == "AND"
            and posted_data["pgNum"] == 1
            and posted_data["pgSize"] == 1000
            and posted_data["srtKey"] == "key"
            and posted_data["srtDirection"] == "ASC"
        )
