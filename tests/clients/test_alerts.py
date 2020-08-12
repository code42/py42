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


class TestAlertsClient(object):
    _alert_ids = [u"test-id1", u"test-id2"]

    def test_rules_returns_rules_client(
        self, mock_alerts_service, mock_alert_rules_service
    ):
        alert_client = AlertsClient(mock_alerts_service, mock_alert_rules_service)
        assert alert_client.rules

    def test_alerts_client_calls_search_with_expected_value(
        self, mock_alerts_service, mock_alert_rules_service, mock_alert_query,
    ):
        alert_client = AlertsClient(mock_alerts_service, mock_alert_rules_service)
        alert_client.search(mock_alert_query)
        mock_alerts_service.search.assert_called_once_with(mock_alert_query)

    def test_alerts_client_calls_get_details_with_expected_value(
        self, mock_alerts_service, mock_alert_rules_service
    ):
        alert_client = AlertsClient(mock_alerts_service, mock_alert_rules_service)
        alert_client.get_details(self._alert_ids)
        mock_alerts_service.get_details.assert_called_once_with(
            self._alert_ids, tenant_id=None
        )

    def test_alerts_client_calls_resolve_with_expected_value(
        self, mock_alerts_service, mock_alert_rules_service,
    ):
        alert_client = AlertsClient(mock_alerts_service, mock_alert_rules_service)
        alert_client.resolve(self._alert_ids)
        mock_alerts_service.resolve.assert_called_once_with(
            self._alert_ids, tenant_id=None, reason=None
        )

    def test_alerts_client_calls_reopen_with_expected_value(
        self, mock_alerts_service, mock_alert_rules_service,
    ):
        alert_client = AlertsClient(mock_alerts_service, mock_alert_rules_service)
        alert_client.reopen(self._alert_ids)
        mock_alerts_service.reopen.assert_called_once_with(
            self._alert_ids, tenant_id=None, reason=None
        )
