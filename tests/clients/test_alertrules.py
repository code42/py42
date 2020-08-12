import pytest

from py42.clients.alertrules import AlertRulesClient
from py42.services.alertrules import AlertRulesService
from py42.services.alerts import AlertService


@pytest.fixture
def mock_alert_rules_service(mocker):
    return mocker.MagicMock(spec=AlertRulesService)


@pytest.fixture
def mock_alerts_service(mocker):
    return mocker.MagicMock(spec=AlertService)


class TestAlertRulesClient(object):
    _rule_id = u"test-rule-id"
    _user_id = u"test-user-uid"

    def test_alert_rules_client_calls_add_user_with_expected_value(
        self, mock_alerts_service, mock_alert_rules_service
    ):
        alert_rules_client = AlertRulesClient(
            mock_alerts_service, mock_alert_rules_service
        )
        alert_rules_client.add_user(self._rule_id, self._rule_id)
        mock_alert_rules_service.add_user.assert_called_once_with(
            self._rule_id, self._rule_id
        )

    def test_alert_rules_client_calls_remove_user_with_expected_value(
        self, mock_alerts_service, mock_alert_rules_service
    ):
        alert_rules_client = AlertRulesClient(
            mock_alerts_service, mock_alert_rules_service
        )
        alert_rules_client.remove_user(self._rule_id, self._rule_id)
        mock_alert_rules_service.remove_user.assert_called_once_with(
            self._rule_id, self._rule_id
        )

    def test_alert_rules_client_calls_remove_all_users_with_expected_value(
        self, mock_alerts_service, mock_alert_rules_service
    ):
        alert_rules_client = AlertRulesClient(
            mock_alerts_service, mock_alert_rules_service
        )
        alert_rules_client.remove_all_users(self._rule_id)
        mock_alert_rules_service.remove_all_users.assert_called_once_with(self._rule_id)

    def test_alert_rules_client_calls_get_all_with_expected_value(
        self, mock_alerts_service, mock_alert_rules_service
    ):
        alert_rules_client = AlertRulesClient(
            mock_alerts_service, mock_alert_rules_service
        )
        alert_rules_client.get_all()
        assert mock_alerts_service.get_all_rules.call_count == 1

    def test_alert_rules_client_calls_get_all_by_name_with_expected_value(
        self, mock_alerts_service, mock_alert_rules_service
    ):
        rule_name = u"test rule"
        alert_rules_client = AlertRulesClient(
            mock_alerts_service, mock_alert_rules_service
        )
        alert_rules_client.get_all_by_name(rule_name)
        mock_alerts_service.get_all_rules_by_name.assert_called_once_with(rule_name)

    def test_alert_rules_client_calls_get_rules_by_observer_id_with_expected_value(
        self, mock_alerts_service, mock_alert_rules_service
    ):
        rule_id = u"test-rule-id"
        alert_rules_client = AlertRulesClient(
            mock_alerts_service, mock_alert_rules_service
        )
        alert_rules_client.get_by_observer_id(rule_id)
        mock_alerts_service.get_rule_by_observer_id.assert_called_once_with(rule_id)

    def test_alert_rules_client_calls_get_rules_page_with_expected_params(
        self, mock_alerts_service, mock_alert_rules_service
    ):
        alert_rules_client = AlertRulesClient(
            mock_alerts_service, mock_alert_rules_service
        )
        alert_rules_client.get_page("key", "dir", 70, 700)
        mock_alerts_service.get_rules_page.assert_called_once_with(
            sort_key="key", sort_direction="dir", page_num=70, page_size=700
        )
