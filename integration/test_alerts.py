from py42.sdk.queries.alerts.alert_query import AlertQuery
from py42.sdk.queries.alerts.filters import AlertState
from py42.sdk.queries.alerts.filters import Severity


def test_search(connection):
    filters = [
        AlertState.eq(AlertState.OPEN),
        Severity.is_in([Severity.HIGH, Severity.MEDIUM]),
    ]
    alert_query = AlertQuery(*filters)
    response = connection.alerts.search(alert_query)
    assert response.status_code == 200


def test_get_details(connection):
    alert_id = "1cae9f92-5fd7-4504-b363-9bc45015adaa"
    response = connection.alerts.get_details(alert_id)
    assert response.status_code == 200


def test_resolve(connection):
    alert_id = "1cae9f92-5fd7-4504-b363-9bc45015adaa"
    response = connection.alerts.resolve(alert_id)
    assert response.status_code == 200


def test_reopen(connection):
    alert_id = "1cae9f92-5fd7-4504-b363-9bc45015adaa"
    response = connection.alerts.reopen(alert_id)
    assert response.status_code == 200
