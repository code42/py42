import pytest

from py42.clients.alerts import AlertsClient
from py42.sdk.queries.alerts.alert_query import AlertQuery
from py42.services.alertrules import AlertRulesService
from py42.services.alerts import AlertService


@pytest.fixture
def mock_alerts_service(mocker):
    return mocker.MagicMock(spec=AlertService)


@pytest.fixture
def mock_alert_rules_service(mocker):
    return mocker.MagicMock(spec=AlertRulesService)


@pytest.fixture
def mock_alert_query(mocker):
    return mocker.MagicMock(spec=AlertQuery)


class TestAlertsModule(object):
    _alert_ids = [u"test-id1", u"test-id2"]

    def test_rules_returns_rules_module(
        self, mock_alerts_service, mock_alert_rules_service
    ):
        alert_module = AlertsClient(mock_alerts_service, mock_alert_rules_service)
        assert alert_module.rules

    def test_alerts_module_calls_search_with_expected_value(
        self, mock_alerts_service, mock_alert_rules_service, mock_alert_query,
    ):
        alert_module = AlertsClient(mock_alerts_service, mock_alert_rules_service)
        alert_module.search(mock_alert_query)
        mock_alerts_service.search.assert_called_once_with(mock_alert_query)

    def test_alerts_module_calls_get_details_with_expected_value(
        self, mock_alerts_service, mock_alert_rules_service
    ):
        alert_module = AlertsClient(mock_alerts_service, mock_alert_rules_service)
        alert_module.get_details(self._alert_ids)
        mock_alerts_service.get_details.assert_called_once_with(
            self._alert_ids, tenant_id=None
        )

    def test_alerts_module_calls_resolve_with_expected_value(
        self, mock_alerts_service, mock_alert_rules_service,
    ):
        alert_module = AlertsClient(mock_alerts_service, mock_alert_rules_service)
        alert_module.resolve(self._alert_ids)
        mock_alerts_service.resolve.assert_called_once_with(
            self._alert_ids, tenant_id=None, reason=None
        )

    def test_alerts_module_calls_reopen_with_expected_value(
        self, mock_alerts_service, mock_alert_rules_service,
    ):
        alert_module = AlertsClient(mock_alerts_service, mock_alert_rules_service)
        alert_module.reopen(self._alert_ids)
        mock_alerts_service.reopen.assert_called_once_with(
            self._alert_ids, tenant_id=None, reason=None
        )
