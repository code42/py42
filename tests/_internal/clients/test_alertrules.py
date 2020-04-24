import pytest
import json

from py42._internal.clients.alertrules import AlertRulesClient, AlertRulesManagerClient
from py42.exceptions import Py42NotFoundError

TEST_RESPONSE = """
{'type$': 'RULE_METADATA_SEARCH_RESPONSE',
 'ruleMetadata': [{'type$': 'RULE_METADATA', 'modifiedBy': 'Email@code42.com',
 'modifiedAt': '2020-04-24T16:49:42.9767920Z', 'name': 'TESTNAME',
 'description': '', 'severity': 'LOW', 'isSystem': False, 'isEnabled': True, 'ruleSource':
 'Alerting', 'tenantId': '1d71796f-af5b-4231-9d8e-df6434da4663',
 'observerRuleId': 'e57ae2e7-b1f8-4332-92e7-1ff4d47bd951', 'type': 'FED_CLOUD_SHARE_PERMISSIONS',
 'id': '6930a1fe-73fc-4f89-8c45-96cba5547b71', 'createdBy': 'test@code42.com',
 'createdAt': '2020-04-20T06:51:10.9420250Z'}]
, 'totalCount': 1, 'problems': []}
"""


class TestAlertRulesClient(object):
    @pytest.fixture
    def mock_response(self, mock_session, py42_response):
        mock_session.post.return_value = py42_response
        return mock_session

    def test_all_rules_posts_expected_data(self, mock_session, user_context):
        alert_rule_client = AlertRulesClient(mock_session, user_context)
        alert_rule_client.add_user(u"rule-id", u"user-id", [u"user-aliases"])

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
        alert_rule_client.remove_users(u"rule-id", [u"user-id"])

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
        alert_rule_client.get("exfiltration", u"rule-id")

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
        alert_rule_client.get("cloudshare", u"rule-id")
        url = mock_session.post.call_args[0][0]
        assert url == "/svc/api/v1/Rules/query-cloud-share-permissions-rule"

    def test_get_by_id_posts_to_correct_endpoint_for_type_mismatch_rule_type(
        self, mock_session, user_context
    ):
        alert_rule_client = AlertRulesClient(mock_session, user_context)
        alert_rule_client.get("typemismatch", u"rule-id")
        url = mock_session.post.call_args[0][0]
        assert url == "/svc/api/v1/Rules/query-file-type-mismatch-rule"


class TestAlertRulesManagerClient(object):
    def test_get_all_posts_expected_data(self, mock_session, user_context):
        alert_rule_client = AlertRulesManagerClient(mock_session, user_context)

        for _ in alert_rule_client.get_all(sort_key="key", sort_direction="ASC"):
            break

        assert mock_session.post.call_count == 1
        posted_data = json.loads(mock_session.post.call_args[1]["data"])
        assert mock_session.post.call_args[0][0] == "/svc/api/v1/rules/query-rule-metadata"
        assert (
            posted_data["tenantId"] == user_context.get_current_tenant_id()
            and posted_data["groups"] == []
            and posted_data["groupClause"] == "AND"
            and posted_data["pgNum"] == 0
            and posted_data["pgSize"] == 1000
            and posted_data["srtKey"] == "key"
            and posted_data["srtDirection"] == "ASC"
        )

    @pytest.mark.skip("TODO Fix failing test")
    def test_get_by_name_posts_expected_data(self, mock_session, user_context):
        alert_rule_client = AlertRulesManagerClient(mock_session, user_context)
        alert_rule_client.get_by_name(u"TestName")
        assert mock_session.post.call_count == 1
        assert mock_session.post.call_args[0][0] == "/svc/api/v1/rules/query-rule-metadata"

    @pytest.mark.skip("TODO Fix failing test")
    def test_get_by_name_filters_correct_record(self, mock_session, user_context, py42_response):
        py42_response.text = TEST_RESPONSE
        mock_session.post.return_value = py42_response
        alert_rule_client = AlertRulesManagerClient(mock_session, user_context)
        alert_rule_client.get_by_name(u"TESTNAME")

    @pytest.mark.skip("TODO Fix failing test")
    def test_get_by_name_filters_correct_record_case_insenstive_search(
        self, mock_session, user_context, py42_response
    ):
        py42_response.text = TEST_RESPONSE
        mock_session.post.return_value = py42_response
        alert_rule_client = AlertRulesManagerClient(mock_session, user_context)
        alert_rule_client.get_by_name(u"TestName")

    @pytest.mark.skip("TODO Fix failing test")
    def test_get_by_name_raises_exception_when_name_does_not_match(
        self, mock_session, user_context, py42_response
    ):
        py42_response.text = TEST_RESPONSE
        mock_session.post.return_value = py42_response
        alert_rule_client = AlertRulesManagerClient(mock_session, user_context)
        with pytest.raises(Py42NotFoundError):
            alert_rule_client.get_by_name(u"TESTNAME2")
