import pytest
from requests import Response
from tests.conftest import create_mock_response

from py42.exceptions import Py42InvalidRuleError
from py42.exceptions import Py42NotFoundError
from py42.services.alertrules import AlertRulesService
from py42.services.userriskprofile import UserRiskProfileService


MOCK_USER_GET_RESPONSE = """
{
    "active": true,
    "cloudAliases": [
    "user.aliases@code42.com"
    ],
    "country": "usa",
    "deleted": false,
    "department": "engineering",
    "displayName": "User Name",
    "division": "test",
    "employmentType": "contract",
    "endDate": {
    "day": 10,
    "month": 20,
    "year": 2030
    },
    "locality": "midwest",
    "managerDisplayName": "My Manager",
    "managerId": "123-manager",
    "managerUsername": "manager@email.com",
    "notes": "my notes",
    "region": "us",
    "startDate": {
    "day": 1,
    "month": 20,
    "year": 2020
    },
    "supportUser": true,
    "tenantId": "123-456",
    "title": "title",
    "userId": "user-id",
    "username": "username@code42.com"
}
"""


@pytest.fixture
def mock_user_service(mocker):
    response = create_mock_response(mocker, MOCK_USER_GET_RESPONSE)
    service = mocker.MagicMock(spec=UserRiskProfileService)
    service.get_by_id.return_value = response
    return service


class TestAlertRulesService:
    def test_add_user_posts_expected_data(
        self, mock_connection, user_context, mock_user_service
    ):
        alert_rule_service = AlertRulesService(
            mock_connection, user_context, mock_user_service
        )
        alert_rule_service.add_user("rule-id", "user-id")

        assert mock_connection.post.call_count == 1
        posted_data = mock_connection.post.call_args[1]["json"]
        assert mock_connection.post.call_args[0][0] == "/svc/api/v1/Rules/add-users"
        assert (
            posted_data["tenantId"] == user_context.get_current_tenant_id()
            and posted_data["ruleId"] == "rule-id"
            and posted_data["userList"][0]["userIdFromAuthority"] == "user-id"
            and posted_data["userList"][0]["userAliasList"]
            == ["user.aliases@code42.com"]
        )

    def test_remove_user_posts_expected_data(
        self, mock_connection, user_context, mock_user_service
    ):
        alert_rule_service = AlertRulesService(
            mock_connection, user_context, mock_user_service
        )
        alert_rule_service.remove_user("rule-id", "user-id")

        assert mock_connection.post.call_count == 1
        posted_data = mock_connection.post.call_args[1]["json"]
        assert mock_connection.post.call_args[0][0] == "/svc/api/v1/Rules/remove-users"
        assert (
            posted_data["tenantId"] == user_context.get_current_tenant_id()
            and posted_data["ruleId"] == "rule-id"
            and posted_data["userIdList"] == ["user-id"]
        )

    def test_remove_all_users_posts_expected_data(
        self, mock_connection, user_context, mock_user_service
    ):
        alert_rule_service = AlertRulesService(
            mock_connection, user_context, mock_user_service
        )
        alert_rule_service.remove_all_users("rule-id")

        assert mock_connection.post.call_count == 1
        posted_data = mock_connection.post.call_args[1]["json"]
        assert (
            mock_connection.post.call_args[0][0] == "/svc/api/v1/Rules/remove-all-users"
        )
        assert (
            posted_data["tenantId"] == user_context.get_current_tenant_id()
            and posted_data["ruleId"] == "rule-id"
        )

    def test_add_user_raises_valid_exception_when_rule_id_is_invalid(
        self,
        mocker,
        mock_connection,
        user_context,
        mock_user_service,
    ):
        response = mocker.MagicMock(spec=Response)
        response.status_code = 400
        exception = mocker.MagicMock(spec=Py42NotFoundError)
        exception.response = response
        mock_connection.post.side_effect = Py42NotFoundError(exception, "")
        alert_rule_service = AlertRulesService(
            mock_connection,
            user_context,
            mock_user_service,
        )
        with pytest.raises(Py42InvalidRuleError) as e:
            alert_rule_service.add_user("invalid-rule-id", "user-id")
        assert "Invalid Observer Rule ID 'invalid-rule-id'." in e.value.args[0]
