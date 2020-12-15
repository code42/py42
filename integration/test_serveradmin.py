import pytest


@pytest.mark.skip("Failing with 403.")
def test_get_alert_log(connection):
    response = connection.serveradmin.get_alert_log()
    assert response.status_code == 200


def test_get_current_tenant(connection):
    response = connection.serveradmin.get_current_tenant()
    assert response.status_code == 200


@pytest.mark.skip("Failing with 403.")
def test_get_diagnostics(connection):
    response = connection.users.get_diagnostics()
    assert response.status_code == 200
