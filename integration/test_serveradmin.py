import pytest


@pytest.mark.integration
class TestServerAdmin():

    @pytest.mark.skip("Requires on prem connection.")
    def test_get_alert_log(self, connection):
        response = connection.serveradmin.get_alert_log()
        assert response.status_code == 200

    def test_get_current_tenant(self, connection):
        response = connection.serveradmin.get_current_tenant()
        assert response.status_code == 200

    @pytest.mark.skip("Requires on prem connection..")
    def test_get_diagnostics(self, connection):
        response = connection.serveradmin.get_diagnostics()
        assert response.status_code == 200
