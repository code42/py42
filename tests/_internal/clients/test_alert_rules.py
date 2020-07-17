import json

import pytest

from py42._internal.clients.detection_list_user import DetectionListUserClient
from py42._internal.clients.alertrules import AlertRulesClient

MOCK_DETECTION_LIST_GET_RESPONSE = """
{"type$": "USER_V2", "tenantId": "1d71796f-af5b-4231-9d8e-df6434da4663",
"userId": "942897397520286581", "userName": "email@test.com", "displayName": "First Name",
"notes": "tests and more tests", "cloudUsernames": ["user.aliases@code42.com"], "riskFactors": []}
"""


@pytest.fixture
def mock_response(self, mock_session, py42_response):
    mock_session.post.return_value = py42_response
    return mock_session


@pytest.fixture
def mock_detection_list_user_client(mocker, py42_response):
    py42_response.text = MOCK_DETECTION_LIST_GET_RESPONSE
    detection_list_user_client = mocker.MagicMock(spec=DetectionListUserClient)
    detection_list_user_client.get_by_id.return_value = py42_response
    return detection_list_user_client


class TestAlertRulesClient(object):
    def test_add_user_posts_expected_data(
        self, mock_session, user_context, mock_detection_list_user_client
    ):
        alert_rule_client = AlertRulesClient(
            mock_session, user_context, mock_detection_list_user_client
        )
        alert_rule_client.add_user(u"rule-id", u"user-id")

        assert mock_session.post.call_count == 1
        posted_data = json.loads(mock_session.post.call_args[1]["data"])
        assert mock_session.post.call_args[0][0] == "/svc/api/v1/Rules/add-users"
        assert (
            posted_data["tenantId"] == user_context.get_current_tenant_id()
            and posted_data["ruleId"] == u"rule-id"
            and posted_data["userList"][0]["userIdFromAuthority"] == u"user-id"
            and posted_data["userList"][0]["userAliasList"]
            == [u"user.aliases@code42.com"]
        )

    def test_remove_user_posts_expected_data(
        self, mock_session, user_context, mock_detection_list_user_client
    ):
        alert_rule_client = AlertRulesClient(
            mock_session, user_context, mock_detection_list_user_client
        )
        alert_rule_client.remove_user(u"rule-id", u"user-id")

        assert mock_session.post.call_count == 1
        posted_data = json.loads(mock_session.post.call_args[1]["data"])
        assert mock_session.post.call_args[0][0] == "/svc/api/v1/Rules/remove-users"
        assert (
            posted_data["tenantId"] == user_context.get_current_tenant_id()
            and posted_data["ruleId"] == u"rule-id"
            and posted_data["userIdList"] == [u"user-id"]
        )

    def test_remove_all_users_posts_expected_data(
        self, mock_session, user_context, mock_detection_list_user_client
    ):
        alert_rule_client = AlertRulesClient(
            mock_session, user_context, mock_detection_list_user_client
        )
        alert_rule_client.remove_all_users(u"rule-id")

        assert mock_session.post.call_count == 1
        posted_data = json.loads(mock_session.post.call_args[1]["data"])
        assert mock_session.post.call_args[0][0] == "/svc/api/v1/Rules/remove-all-users"
        assert (
            posted_data["tenantId"] == user_context.get_current_tenant_id()
            and posted_data["ruleId"] == u"rule-id"
        )
