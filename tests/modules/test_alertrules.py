import pytest
from requests import HTTPError
from requests import Response

from py42._internal.client_factories import MicroserviceClientFactory
from py42._internal.clients.alertrules import AlertRulesClient
from py42._internal.clients.alerts import AlertClient
from py42.exceptions import Py42InternalServerError
from py42.exceptions import Py42InvalidRuleOperationError
from py42.modules.alertrules import AlertRulesModule
from py42.response import Py42Response


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
def mock_microservice_client_factory(mocker):
    return mocker.MagicMock(spec=MicroserviceClientFactory)


@pytest.fixture
def mock_alert_rules_client(mocker):
    return mocker.MagicMock(spec=AlertRulesClient)


@pytest.fixture
def mock_alerts_client(mocker):
    return mocker.MagicMock(spec=AlertClient)


@pytest.fixture
def mock_alerts_client_system_rule(mocker, mock_alerts_client):
    response = mocker.MagicMock(spec=Py42Response)
    response.text = TEST_SYSTEM_RULE_RESPONSE
    mock_alerts_client.get_rule_by_observer_id.return_value = response
    return mock_alerts_client


class TestAlertRulesModules(object):

    _rule_id = u"test-rule-id"
    _user_id = u"test-user-uid"

    def test_alert_rules_module_calls_add_user_with_expected_value(
        self, mock_microservice_client_factory, mock_alert_rules_client
    ):
        mock_microservice_client_factory.get_alert_rules_client.return_value = (
            mock_alert_rules_client
        )
        alert_rules_module = AlertRulesModule(mock_microservice_client_factory)
        alert_rules_module.add_user(self._rule_id, self._rule_id)
        mock_alert_rules_client.add_user.assert_called_once_with(
            self._rule_id, self._rule_id
        )

    def test_alert_rules_modules_raises_invalid_rule_type_error_when_adding_to_system_rule(
        self,
        mocker,
        mock_microservice_client_factory,
        mock_alert_rules_client,
        mock_alerts_client_system_rule,
    ):
        def add(*args, **kwargs):
            base_err = mocker.MagicMock(spec=HTTPError)
            base_err.response = mocker.MagicMock(spec=Response)
            raise Py42InternalServerError(base_err)

        mock_alert_rules_client.add_user.side_effect = add
        mock_microservice_client_factory.get_alert_rules_client.return_value = (
            mock_alert_rules_client
        )
        mock_microservice_client_factory.get_alerts_client.return_value = (
            mock_alerts_client_system_rule
        )
        alert_rules_module = AlertRulesModule(mock_microservice_client_factory)
        with pytest.raises(Py42InvalidRuleOperationError) as err:
            alert_rules_module.add_user(self._rule_id, self._rule_id)

        assert (
            "Only alert rules with a source of 'Alerting' can be targeted by this command."
            in str(err.value)
        )

    def test_alert_rules_module_calls_remove_user_with_expected_value(
        self, mock_microservice_client_factory, mock_alert_rules_client
    ):
        mock_microservice_client_factory.get_alert_rules_client.return_value = (
            mock_alert_rules_client
        )
        alert_rules_module = AlertRulesModule(mock_microservice_client_factory)
        alert_rules_module.remove_user(self._rule_id, self._rule_id)
        mock_alert_rules_client.remove_user.assert_called_once_with(
            self._rule_id, self._rule_id
        )

    def test_alert_rules_module_calls_remove_all_users_with_expected_value(
        self, mock_microservice_client_factory, mock_alert_rules_client
    ):
        mock_microservice_client_factory.get_alert_rules_client.return_value = (
            mock_alert_rules_client
        )
        alert_rules_module = AlertRulesModule(mock_microservice_client_factory)
        alert_rules_module.remove_all_users(self._rule_id)
        mock_alert_rules_client.remove_all_users.assert_called_once_with(self._rule_id)

    def test_alert_rules_module_calls_get_all_with_expected_value(
        self, mock_microservice_client_factory, mock_alerts_client
    ):
        mock_microservice_client_factory.get_alerts_client.return_value = (
            mock_alerts_client
        )
        alert_rules_module = AlertRulesModule(mock_microservice_client_factory)
        alert_rules_module.get_all()
        assert mock_alerts_client.get_all_rules.call_count == 1

    def test_alert_rules_module_calls_get_all_by_name_with_expected_value(
        self, mock_microservice_client_factory, mock_alerts_client
    ):
        rule_name = u"test rule"
        mock_microservice_client_factory.get_alerts_client.return_value = (
            mock_alerts_client
        )
        alert_rules_module = AlertRulesModule(mock_microservice_client_factory)
        alert_rules_module.get_all_by_name(rule_name)
        mock_alerts_client.get_all_rules_by_name.assert_called_once_with(rule_name)

    def test_alert_rules_module_calls_get_rules_by_observer_id_with_expected_value(
        self, mock_microservice_client_factory, mock_alerts_client
    ):
        rule_id = u"test-rule-id"
        mock_microservice_client_factory.get_alerts_client.return_value = (
            mock_alerts_client
        )
        alert_rules_module = AlertRulesModule(mock_microservice_client_factory)
        alert_rules_module.get_by_observer_id(rule_id)
        mock_alerts_client.get_rule_by_observer_id.assert_called_once_with(rule_id)

    def test_alert_rules_module_calls_get_rules_page_with_expected_params(
        self, mock_microservice_client_factory, mock_alerts_client
    ):
        mock_microservice_client_factory.get_alerts_client.return_value = (
            mock_alerts_client
        )
        alert_rules_module = AlertRulesModule(mock_microservice_client_factory)
        alert_rules_module.get_page("key", "dir", 70, 700)
        mock_alerts_client.get_rules_page.assert_called_once_with(
            sort_key="key", sort_direction="dir", page_num=70, page_size=700
        )
