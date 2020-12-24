import json

import pytest
from requests import Response

from py42.exceptions import Py42BadRequestError
from py42.exceptions import Py42InvalidRule
from py42.exceptions import Py42NotFoundError
from py42.exceptions import Py42UserNotOnListError
from py42.services.alertrules import AlertRulesService
from py42.services.detectionlists.user_profile import DetectionListUserService


MOCK_DETECTION_LIST_GET_RESPONSE = """
{"type$": "USER_V2", "tenantId": "1d71796f-af5b-4231-9d8e-df6434da4663",
"userId": "942897397520286581", "userName": "email@test.com", "displayName": "First Name",
"notes": "tests and more tests", "cloudUsernames": ["user.aliases@code42.com"], "riskFactors": []}
"""


@pytest.fixture
def mock_response(mock_connection, py42_response):
    mock_connection.post.return_value = py42_response
    return mock_connection


@pytest.fixture
def mock_detection_list_user_service(mocker, py42_response):
    py42_response.text = MOCK_DETECTION_LIST_GET_RESPONSE
    py42_response.data = json.loads(MOCK_DETECTION_LIST_GET_RESPONSE)
    detection_list_user_service = mocker.MagicMock(spec=DetectionListUserService)
    detection_list_user_service.get_by_id.return_value = py42_response
    return detection_list_user_service


@pytest.fixture
def mock_detection_list_get_by_id_failure_when_invalid_id(
    mocker, mock_connection, py42_response
):
    response = mocker.MagicMock(spec=Response)
    response.status_code = 400
    exception = mocker.MagicMock(spec=Py42BadRequestError)
    exception.response = response
    detection_list_user_service = mocker.MagicMock(spec=DetectionListUserService)
    detection_list_user_service.create_if_not_exists.return_value = False
    detection_list_user_service.get_by_id.side_effect = Py42BadRequestError(
        exception, ""
    )
    return detection_list_user_service


@pytest.fixture
def mock_detection_list_post_failure_when_invalid_rule_id(
    mocker, mock_connection, py42_response
):
    response = mocker.MagicMock(spec=Response)
    response.status_code = 400
    exception = mocker.MagicMock(spec=Py42NotFoundError)
    exception.response = response
    mock_connection.post.side_effect = Py42NotFoundError(exception, "")
    detection_list_user_service = mocker.MagicMock(spec=DetectionListUserService)
    detection_list_user_service.create_if_not_exists.return_value = True
    detection_list_user_service.get_by_id.return_value = py42_response
    return detection_list_user_service


@pytest.fixture
def mock_detection_list_user_service_create_user(
    mocker, py42_response, http_error, mock_connection
):
    py42_response.text = MOCK_DETECTION_LIST_GET_RESPONSE
    py42_response.data = json.loads(MOCK_DETECTION_LIST_GET_RESPONSE)
    response = mocker.MagicMock(spec=Response)
    response.status_code = 400
    exception = mocker.MagicMock(spec=Py42BadRequestError)
    exception.response = response
    detection_list_user_service = mocker.MagicMock(spec=DetectionListUserService)
    detection_list_user_service.get_by_id.return_value = py42_response
    detection_list_user_service.create_if_not_exists.return_value = False
    mock_connection.post.return_value = py42_response
    return detection_list_user_service


class TestAlertRulesService(object):
    def test_add_user_posts_expected_data(
        self, mock_connection, user_context, mock_detection_list_user_service
    ):
        alert_rule_service = AlertRulesService(
            mock_connection, user_context, mock_detection_list_user_service
        )
        alert_rule_service.add_user(u"rule-id", u"user-id")

        assert mock_connection.post.call_count == 1
        posted_data = mock_connection.post.call_args[1]["json"]
        assert mock_connection.post.call_args[0][0] == "/svc/api/v1/Rules/add-users"
        assert (
            posted_data["tenantId"] == user_context.get_current_tenant_id()
            and posted_data["ruleId"] == u"rule-id"
            and posted_data["userList"][0]["userIdFromAuthority"] == u"user-id"
            and posted_data["userList"][0]["userAliasList"]
            == [u"user.aliases@code42.com"]
        )

    def test_remove_user_posts_expected_data(
        self, mock_connection, user_context, mock_detection_list_user_service
    ):
        alert_rule_service = AlertRulesService(
            mock_connection, user_context, mock_detection_list_user_service
        )
        alert_rule_service.remove_user(u"rule-id", u"user-id")

        assert mock_connection.post.call_count == 1
        posted_data = mock_connection.post.call_args[1]["json"]
        assert mock_connection.post.call_args[0][0] == "/svc/api/v1/Rules/remove-users"
        assert (
            posted_data["tenantId"] == user_context.get_current_tenant_id()
            and posted_data["ruleId"] == u"rule-id"
            and posted_data["userIdList"] == [u"user-id"]
        )

    def test_remove_all_users_posts_expected_data(
        self, mock_connection, user_context, mock_detection_list_user_service
    ):
        alert_rule_service = AlertRulesService(
            mock_connection, user_context, mock_detection_list_user_service
        )
        alert_rule_service.remove_all_users(u"rule-id")

        assert mock_connection.post.call_count == 1
        posted_data = mock_connection.post.call_args[1]["json"]
        assert (
            mock_connection.post.call_args[0][0] == "/svc/api/v1/Rules/remove-all-users"
        )
        assert (
            posted_data["tenantId"] == user_context.get_current_tenant_id()
            and posted_data["ruleId"] == u"rule-id"
        )

    def test_add_user_raises_valid_exception_when_user_id_is_invalid(
        self,
        mock_connection,
        user_context,
        mock_detection_list_get_by_id_failure_when_invalid_id,
    ):
        alert_rule_service = AlertRulesService(
            mock_connection,
            user_context,
            mock_detection_list_get_by_id_failure_when_invalid_id,
        )
        with pytest.raises(Py42UserNotOnListError) as e:
            alert_rule_service.add_user("rule-id", "invalid-user-id")
        assert (
            "'invalid-user-id' is not currently on the user profile list."
            in e.value.args[0]
        )

    def test_add_user_raises_valid_exception_when_rule_id_is_invalid(
        self,
        mock_connection,
        user_context,
        mock_detection_list_post_failure_when_invalid_rule_id,
    ):
        alert_rule_service = AlertRulesService(
            mock_connection,
            user_context,
            mock_detection_list_post_failure_when_invalid_rule_id,
        )
        with pytest.raises(Py42InvalidRule) as e:
            alert_rule_service.add_user("invalid-rule-id", "user-id")
        assert "Invalid Observer Rule ID 'invalid-rule-id'." in e.value.args[0]

    def test_add_user_posts_expected_data_when_user_does_not_exist_in_detectionlist(
        self,
        mock_connection,
        user_context,
        mock_detection_list_user_service_create_user,
    ):
        alert_rule_service = AlertRulesService(
            mock_connection, user_context, mock_detection_list_user_service_create_user
        )
        alert_rule_service.add_user(u"rule-id", u"user-id")

        assert mock_connection.post.call_count == 1
        posted_data = mock_connection.post.call_args[1]["json"]
        assert mock_connection.post.call_args[0][0] == "/svc/api/v1/Rules/add-users"
        assert (
            posted_data["tenantId"] == user_context.get_current_tenant_id()
            and posted_data["ruleId"] == u"rule-id"
            and posted_data["userList"][0]["userIdFromAuthority"] == u"user-id"
            and posted_data["userList"][0]["userAliasList"]
            == [u"user.aliases@code42.com"]
        )
