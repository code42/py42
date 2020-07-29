import pytest

from py42._internal.client_factories import MicroserviceClientFactory
from py42.services.alerts import AlertClient
from py42.clients.alertrules import AlertRulesModule
from py42.clients.alerts import AlertsModule
from py42.sdk.queries.fileevents.file_event_query import FileEventQuery


@pytest.fixture
def mock_microservice_client_factory(mocker):
    return mocker.MagicMock(spec=MicroserviceClientFactory)


@pytest.fixture
def mock_alerts_client(mocker):
    return mocker.MagicMock(spec=AlertClient)


@pytest.fixture
def mock_file_event_query(mocker):
    return mocker.MagicMock(spec=FileEventQuery)


class TestAlertsModule(object):

    _alert_ids = [u"test-id1", u"test-id2"]

    def test_rules_returns_rules_module(
        self, mock_microservice_client_factory, mock_alerts_client
    ):
        mock_microservice_client_factory.get_alerts_client.return_value = (
            mock_alerts_client
        )
        alert_module = AlertsModule(mock_microservice_client_factory)
        assert type(alert_module.rules) == AlertRulesModule

    def test_alerts_module_calls_search_with_expected_value(
        self,
        mock_microservice_client_factory,
        mock_alerts_client,
        mock_file_event_query,
    ):
        mock_microservice_client_factory.get_alerts_client.return_value = (
            mock_alerts_client
        )
        alert_module = AlertsModule(mock_microservice_client_factory)
        alert_module.search(mock_file_event_query)
        mock_alerts_client.search.assert_called_once_with(mock_file_event_query)

    def test_alerts_module_calls_get_details_with_expected_value(
        self, mock_microservice_client_factory, mock_alerts_client
    ):
        mock_microservice_client_factory.get_alerts_client.return_value = (
            mock_alerts_client
        )
        alert_module = AlertsModule(mock_microservice_client_factory)
        alert_module.get_details(self._alert_ids)
        mock_alerts_client.get_details.assert_called_once_with(
            self._alert_ids, tenant_id=None
        )

    def test_alerts_module_calls_resolve_with_expected_value(
        self,
        mock_microservice_client_factory,
        mock_alerts_client,
        mock_file_event_query,
    ):
        mock_microservice_client_factory.get_alerts_client.return_value = (
            mock_alerts_client
        )
        alert_module = AlertsModule(mock_microservice_client_factory)
        alert_module.resolve(self._alert_ids)
        mock_alerts_client.resolve.assert_called_once_with(
            self._alert_ids, tenant_id=None, reason=None
        )

    def test_alerts_module_calls_reopen_with_expected_value(
        self,
        mock_microservice_client_factory,
        mock_alerts_client,
        mock_file_event_query,
    ):
        mock_microservice_client_factory.get_alerts_client.return_value = (
            mock_alerts_client
        )
        alert_module = AlertsModule(mock_microservice_client_factory)
        alert_module.reopen(self._alert_ids)
        mock_alerts_client.reopen.assert_called_once_with(
            self._alert_ids, tenant_id=None, reason=None
        )
