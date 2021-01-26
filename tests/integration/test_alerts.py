import pytest
from tests.integration.conftest import assert_successful_response

from py42.sdk.queries.alerts.alert_query import AlertQuery
from py42.sdk.queries.alerts.filters import AlertState
from py42.sdk.queries.alerts.filters import Severity


@pytest.mark.integration
def test_search(connection):
    filters = [
        AlertState.eq(AlertState.OPEN),
        Severity.is_in([Severity.HIGH, Severity.MEDIUM]),
    ]
    alert_query = AlertQuery(*filters)
    response = connection.alerts.search(alert_query)
    assert_successful_response(response)


@pytest.mark.integration
def test_get_details(connection, alert_id):
    response = connection.alerts.get_details(alert_id)
    assert_successful_response(response)


@pytest.mark.integration
def test_resolve(connection, alert_id):
    response = connection.alerts.resolve(alert_id)
    assert_successful_response(response)


@pytest.mark.integration
def test_reopen(connection, alert_id):
    response = connection.alerts.reopen(alert_id)
    assert_successful_response(response)
