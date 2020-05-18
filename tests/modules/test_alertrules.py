import pytest

from py42._internal.client_factories import MicroserviceClientFactory
from py42._internal.clients.alerts import AlertClient
from py42._internal.clients.alertrules import AlertRulesClient
from py42.modules.alertrules import AlertRulesModule


@pytest.fixture
def mock_microservice_client_factory(mocker):
    return mocker.MagicMock(spec=MicroserviceClientFactory)


@pytest.fixture
def mock_alert_rules_client(mocker):
    return mocker.MagicMock(spec=AlertRulesClient)


@pytest.fixture
def mock_alerts_client(mocker):
    return mocker.MagicMock(spec=AlertClient)


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
        mock_alert_rules_client.add_user.assert_called_once_with(self._rule_id, self._rule_id)

    def test_alert_rules_module_calls_remove_user_with_expected_value(
        self, mock_microservice_client_factory, mock_alert_rules_client
    ):
        mock_microservice_client_factory.get_alert_rules_client.return_value = (
            mock_alert_rules_client
        )
        alert_rules_module = AlertRulesModule(mock_microservice_client_factory)
        alert_rules_module.remove_user(self._rule_id, self._rule_id)
        mock_alert_rules_client.remove_user.assert_called_once_with(self._rule_id, self._rule_id)

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
        mock_microservice_client_factory.get_alerts_client.return_value = mock_alerts_client
        alert_rules_module = AlertRulesModule(mock_microservice_client_factory)
        alert_rules_module.get_all()
        assert mock_alerts_client.get_all_rules.call_count == 1

    def test_alert_rules_module_calls_get_all_by_name_with_expected_value(
        self, mock_microservice_client_factory, mock_alerts_client
    ):
        rule_name = u"test rule"
        mock_microservice_client_factory.get_alerts_client.return_value = mock_alerts_client
        alert_rules_module = AlertRulesModule(mock_microservice_client_factory)
        alert_rules_module.get_all_by_name(rule_name)
        mock_alerts_client.get_all_rules_by_name.assert_called_once_with(rule_name)
