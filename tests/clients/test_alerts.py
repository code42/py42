import json

import pytest

from .conftest import create_mock_response
from py42.clients.alerts import AlertsClient
from py42.sdk.queries.alerts.alert_query import AlertQuery
from py42.services.alertrules import AlertRulesService
from py42.services.alerts import AlertService

ALERT_A = {
    "id": "A",
    "createdAt": "2021-01-01T09:40:05.2837100Z",
    "actor": "A",
    "type": "A",
    "name": "A",
    "description": "A",
    "actorId": "A",
    "target": "A",
    "severity": "A",
    "ruleSource": "A",
    "observations": "A",
    "notes": "A",
    "state": "A",
    "stateLastModifiedAt": "2021-01-01T09:40:05.2837100Z",
    "stateLastModifiedBy": "A",
    "lastModifiedTime": "2021-01-01T09:40:05.2837100Z",
    "lastModifiedBy": "A",
    "ruleId": "A",
    "tenantId": "A",
}
ALERT_B = {
    "id": "B",
    "createdAt": "2021-02-02T18:24:15.5284760Z",
    "actor": "B",
    "type": "B",
    "name": "B",
    "description": "B",
    "actorId": "B",
    "target": "B",
    "severity": "B",
    "ruleSource": "B",
    "observations": "B",
    "notes": "B",
    "state": "B",
    "stateLastModifiedAt": "2021-02-02T18:24:15.5284760Z",
    "stateLastModifiedBy": "B",
    "lastModifiedTime": "2021-02-02T18:24:15.5284760Z",
    "lastModifiedBy": "B",
    "ruleId": "B",
    "tenantId": "B",
}
ALERT_C = {
    "id": "C",
    "createdAt": "2021-03-03T09:40:26.6477830Z",
    "actor": "C",
    "type": "C",
    "name": "C",
    "description": "C",
    "actorId": "C",
    "target": "C",
    "severity": "C",
    "ruleSource": "C",
    "observations": "C",
    "notes": "C",
    "state": "C",
    "stateLastModifiedAt": "2021-03-03T09:40:26.6477830Z",
    "stateLastModifiedBy": "C",
    "lastModifiedTime": "2021-03-03T09:40:26.6477830Z",
    "lastModifiedBy": "C",
    "ruleId": "C",
    "tenantId": "C",
}
ALERT_D = {
    "id": "D",
    "createdAt": "2021-04-04T09:40:50.7749710Z",
    "actor": "D",
    "type": "D",
    "name": "D",
    "description": "D",
    "actorId": "D",
    "target": "D",
    "severity": "D",
    "ruleSource": "D",
    "observations": "D",
    "notes": "D",
    "state": "D",
    "stateLastModifiedAt": "2021-04-04T09:40:50.7749710Z",
    "stateLastModifiedBy": "D",
    "lastModifiedTime": "2021-04-04T09:40:50.7749710Z",
    "lastModifiedBy": "D",
    "ruleId": "D",
    "tenantId": "D",
}
ALERT_E = {
    "id": "E",
    "createdAt": "2021-05-05T21:29:34.5510380Z",
    "actor": "E",
    "type": "E",
    "name": "E",
    "description": "E",
    "actorId": "E",
    "target": "E",
    "severity": "E",
    "ruleSource": "E",
    "observations": "E",
    "notes": "E",
    "state": "E",
    "stateLastModifiedAt": "2021-05-05T21:29:34.5510380Z",
    "stateLastModifiedBy": "E",
    "lastModifiedTime": "2021-05-05T21:29:34.5510380Z",
    "lastModifiedBy": "E",
    "ruleId": "E",
    "tenantId": "E",
}
ALERT_F = {
    "id": "F",
    "createdAt": "2021-06-06T21:24:50.7541390Z",
    "actor": "F",
    "type": "F",
    "name": "F",
    "description": "F",
    "actorId": "F",
    "target": "F",
    "severity": "F",
    "ruleSource": "F",
    "observations": "F",
    "notes": "F",
    "state": "F",
    "stateLastModifiedAt": "2021-06-06T21:24:50.7541390Z",
    "stateLastModifiedBy": "F",
    "lastModifiedTime": "2021-06-06T21:24:50.7541390Z",
    "lastModifiedBy": "F",
    "ruleId": "F",
    "tenantId": "F",
}
TEST_ALERTS = [ALERT_A, ALERT_B, ALERT_C, ALERT_D, ALERT_E, ALERT_F]


@pytest.fixture
def mock_alerts_service(mocker):
    return mocker.MagicMock(spec=AlertService)


@pytest.fixture
def mock_alert_rules_service(mocker):
    return mocker.MagicMock(spec=AlertRulesService)


@pytest.fixture
def mock_alert_query(mocker):
    return mocker.MagicMock(spec=AlertQuery)


@pytest.fixture
def mock_alerts_service_with_pages(mocker, mock_alerts_service):
    def _func(ascending=True):
        alerts = TEST_ALERTS if ascending else TEST_ALERTS[::-1]
        alert_page_1 = create_mock_response(mocker, json.dumps({"alerts": alerts[:3]}))
        alert_page_2 = create_mock_response(mocker, json.dumps({"alerts": alerts[3:]}))

        def page_gen():
            yield alert_page_1
            yield alert_page_2

        mock_alerts_service.search_all_pages.return_value = page_gen()
        return mock_alerts_service

    return _func


@pytest.fixture
def mock_details(mocker):
    detail_page_1 = create_mock_response(
        mocker, json.dumps({"alerts": [ALERT_B, ALERT_C, ALERT_A]})
    )
    detail_page_2 = create_mock_response(
        mocker, json.dumps({"alerts": [ALERT_F, ALERT_E, ALERT_D]})
    )

    def mock_get_details(alert_ids):
        if set(alert_ids) == {"A", "B", "C"}:
            return detail_page_1
        if set(alert_ids) == {"D", "E", "F"}:
            return detail_page_2

    return mock_get_details


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
        mock_alerts_service.search.assert_called_once_with(mock_alert_query, 1, None)

    def test_alerts_client_calls_get_details_with_expected_value(
        self, mock_alerts_service, mock_alert_rules_service
    ):
        alert_client = AlertsClient(mock_alerts_service, mock_alert_rules_service)
        alert_client.get_details(self._alert_ids)
        mock_alerts_service.get_details.assert_called_once_with(self._alert_ids)

    def test_alerts_client_calls_update_state_with_resolve_state_and_expected_value(
        self, mock_alerts_service, mock_alert_rules_service,
    ):
        alert_client = AlertsClient(mock_alerts_service, mock_alert_rules_service)
        alert_client.resolve(self._alert_ids)
        mock_alerts_service.update_state.assert_called_once_with(
            "RESOLVED", self._alert_ids, note=None
        )

    def test_alerts_client_calls_update_state_with_reopen_state_and_expected_value(
        self, mock_alerts_service, mock_alert_rules_service,
    ):
        alert_client = AlertsClient(mock_alerts_service, mock_alert_rules_service)
        alert_client.reopen(self._alert_ids)
        mock_alerts_service.update_state.assert_called_once_with(
            "OPEN", self._alert_ids, note=None
        )

    def test_alerts_client_calls_update_state_with_state_and_expected_value(
        self, mock_alerts_service, mock_alert_rules_service,
    ):
        alert_client = AlertsClient(mock_alerts_service, mock_alert_rules_service)
        alert_client.update_state("RESOLVED", self._alert_ids)
        mock_alerts_service.update_state.assert_called_once_with(
            "RESOLVED", self._alert_ids, note=None
        )

    def test_alerts_client_calls_update_note_with_expected_value_and_param(
        self, mock_alerts_service, mock_alert_rules_service,
    ):
        alert_client = AlertsClient(mock_alerts_service, mock_alert_rules_service)
        alert_client.update_note("alert-id", "a note")
        mock_alerts_service.update_note.assert_called_once_with("alert-id", "a note")

    def test_alerts_client_calls_search_all_pages_with_expected_value_and_param(
        self, mock_alerts_service, mock_alert_rules_service,
    ):
        alert_client = AlertsClient(mock_alerts_service, mock_alert_rules_service)
        query = AlertQuery()
        alert_client.search_all_pages(query)
        mock_alerts_service.search_all_pages.assert_called_once_with(query)

    def test_alerts_client_calls_get_aggregate_data_with_expected_value_and_param(
        self, mock_alerts_service, mock_alert_rules_service,
    ):
        alert_client = AlertsClient(mock_alerts_service, mock_alert_rules_service)
        alert_client.get_aggregate_data("alert-id")
        mock_alerts_service.get_aggregate_data.assert_called_once_with("alert-id")

    def test_alerts_client_get_all_alert_details_calls_get_details_for_each_page(
        self, mock_alerts_service_with_pages, mock_alert_rules_service
    ):
        mock_alerts_service = mock_alerts_service_with_pages(ascending=True)
        alert_client = AlertsClient(mock_alerts_service, mock_alert_rules_service)
        query = AlertQuery()
        list(alert_client.get_all_alert_details(query))
        assert mock_alerts_service.get_details.call_args_list[0][0][0] == [
            "A",
            "B",
            "C",
        ]
        assert mock_alerts_service.get_details.call_args_list[1][0][0] == [
            "D",
            "E",
            "F",
        ]

    @pytest.mark.parametrize(
        "sort_key",
        [
            "AlertId",
            "TenantId",
            "Type",
            "Name",
            "Description",
            "Actor",
            "ActorId",
            "Target",
            "Severity",
            "RuleSource",
            "CreatedAt",
            "Observations",
            "Notes",
            "State",
            "StateLastModifiedAt",
            "StateLastModifiedBy",
            "LastModifiedTime",
            "LastModifiedBy",
            "RuleId",
        ],
    )
    def test_alerts_client_get_all_alert_details_sorts_results_according_to_query_sort_key(
        self,
        mock_alerts_service_with_pages,
        mock_alert_rules_service,
        mock_details,
        sort_key,
    ):
        mock_alerts_service = mock_alerts_service_with_pages(ascending=True)
        mock_alerts_service.get_details = mock_details
        alert_client = AlertsClient(mock_alerts_service, mock_alert_rules_service)
        query = AlertQuery()
        query.sort_direction = "asc"
        query.sort_key = sort_key
        results = list(alert_client.get_all_alert_details(query))
        assert results == [ALERT_A, ALERT_B, ALERT_C, ALERT_D, ALERT_E, ALERT_F]

    @pytest.mark.parametrize(
        "sort_key",
        [
            "AlertId",
            "TenantId",
            "Type",
            "Name",
            "Description",
            "Actor",
            "ActorId",
            "Target",
            "Severity",
            "RuleSource",
            "CreatedAt",
            "Observations",
            "Notes",
            "State",
            "StateLastModifiedAt",
            "StateLastModifiedBy",
            "LastModifiedTime",
            "LastModifiedBy",
            "RuleId",
        ],
    )
    def test_alerts_client_get_all_alert_details_sorts_results_descending_when_specified(
        self,
        mock_alerts_service_with_pages,
        mock_alert_rules_service,
        mock_details,
        sort_key,
    ):
        mock_alerts_service = mock_alerts_service_with_pages(ascending=False)
        mock_alerts_service.get_details = mock_details
        alert_client = AlertsClient(mock_alerts_service, mock_alert_rules_service)
        query = AlertQuery()
        query.sort_direction = "desc"
        query.sort_key = sort_key
        results = list(alert_client.get_all_alert_details(query))
        assert results == [ALERT_F, ALERT_E, ALERT_D, ALERT_C, ALERT_B, ALERT_A]
