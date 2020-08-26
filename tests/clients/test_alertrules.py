import pytest
from requests import HTTPError
from requests import Response

from py42.clients.alertrules import AlertRulesClient
from py42.exceptions import Py42InternalServerError
from py42.exceptions import Py42InvalidRuleOperationError
from py42.response import Py42Response
from py42.services.alertrules import AlertRulesService
from py42.services.alerts import AlertService

TEST_RULE_ID = "rule-id"


TEST_SYSTEM_RULE_RESPONSE = {
    "ruleMetadata": [
        {
            "observerRuleId": TEST_RULE_ID,
            "type": "FED_FILE_TYPE_MISMATCH",
            "isSystem": True,
            "ruleSource": "NOTVALID",
        }
    ]
}


@pytest.fixture
def mock_alerts_service_system_rule(mocker, mock_alerts_service):
    response = mocker.MagicMock(spec=Py42Response)
    response.text = TEST_SYSTEM_RULE_RESPONSE
    mock_alerts_service.get_rule_by_observer_id.return_value = response
    return mock_alerts_service


@pytest.fixture
def mock_alert_rules_service(mocker):
    return mocker.MagicMock(spec=AlertRulesService)


@pytest.fixture
def mock_alerts_service(mocker):
    return mocker.MagicMock(spec=AlertService)


class TestAlertRulesClient(object):
    _rule_id = u"test-rule-id"
    _user_id = u"test-user-uid"

    def test_alert_rules_service_calls_add_user_with_expected_value(
        self, mock_alerts_service, mock_alert_rules_service
    ):
        alert_rules_client = AlertRulesClient(
            mock_alerts_service, mock_alert_rules_service
        )
        alert_rules_client.add_user(self._rule_id, self._rule_id)
        mock_alert_rules_service.add_user.assert_called_once_with(
            self._rule_id, self._rule_id
        )

    def test_alert_rules_service_raises_invalid_rule_type_error_when_adding_to_system_rule(
        self, mocker, mock_alerts_service_system_rule, mock_alert_rules_service
    ):
        def add(*args, **kwargs):
            base_err = mocker.MagicMock(spec=HTTPError)
            base_err.response = mocker.MagicMock(spec=Response)
            raise Py42InternalServerError(base_err)

        mock_alert_rules_service.add_user.side_effect = add
        alert_rules_module = AlertRulesClient(
            mock_alerts_service_system_rule, mock_alert_rules_service
        )
        with pytest.raises(Py42InvalidRuleOperationError) as err:
            alert_rules_module.add_user(self._rule_id, self._rule_id)

        assert (
            "Only alert rules with a source of 'Alerting' can be targeted by this command."
            in str(err.value)
        )

    def test_alert_rules_service_calls_remove_user_with_expected_value(
        self, mock_alerts_service, mock_alert_rules_service
    ):
        alert_rules_client = AlertRulesClient(
            mock_alerts_service, mock_alert_rules_service
        )
        alert_rules_client.remove_user(self._rule_id, self._rule_id)
        mock_alert_rules_service.remove_user.assert_called_once_with(
            self._rule_id, self._rule_id
        )

    def test_alert_rules_service_calls_remove_all_users_with_expected_value(
        self, mock_alerts_service, mock_alert_rules_service
    ):
        alert_rules_client = AlertRulesClient(
            mock_alerts_service, mock_alert_rules_service
        )
        alert_rules_client.remove_all_users(self._rule_id)
        mock_alert_rules_service.remove_all_users.assert_called_once_with(self._rule_id)

    def test_alert_rules_service_calls_get_all_with_expected_value(
        self, mock_alerts_service, mock_alert_rules_service
    ):
        alert_rules_client = AlertRulesClient(
            mock_alerts_service, mock_alert_rules_service
        )
        alert_rules_client.get_all()
        assert mock_alerts_service.get_all_rules.call_count == 1

    def test_alert_rules_service_calls_get_all_by_name_with_expected_value(
        self, mock_alerts_service, mock_alert_rules_service
    ):
        rule_name = u"test rule"
        alert_rules_client = AlertRulesClient(
            mock_alerts_service, mock_alert_rules_service
        )
        alert_rules_client.get_all_by_name(rule_name)
        mock_alerts_service.get_all_rules_by_name.assert_called_once_with(rule_name)

    def test_alert_rules_service_calls_get_rules_by_observer_id_with_expected_value(
        self, mock_alerts_service, mock_alert_rules_service
    ):
        rule_id = u"test-rule-id"
        alert_rules_client = AlertRulesClient(
            mock_alerts_service, mock_alert_rules_service
        )
        alert_rules_client.get_by_observer_id(rule_id)
        mock_alerts_service.get_rule_by_observer_id.assert_called_once_with(rule_id)

    def test_alert_rules_service_calls_get_rules_page_with_expected_params(
        self, mock_alerts_service, mock_alert_rules_service
    ):
        alert_rules_client = AlertRulesClient(
            mock_alerts_service, mock_alert_rules_service
        )
        alert_rules_client.get_page("key", "dir", 70, 700)
        mock_alerts_service.get_rules_page.assert_called_once_with(
            sort_key="key", sort_direction="dir", page_num=70, page_size=700
        )
