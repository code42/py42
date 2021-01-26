import pytest
from tests.integration.conftest import assert_successful_response


@pytest.mark.integration
class TestServerAdmin:
    @pytest.mark.skip("Requires on prem connection.")
    def test_get_alert_log(self, connection):
        response = connection.serveradmin.get_alert_log()
        assert_successful_response(response)

    def test_get_current_tenant(self, connection):
        response = connection.serveradmin.get_current_tenant()
        assert_successful_response(response)

    @pytest.mark.skip("Requires on prem connection..")
    def test_get_diagnostics(self, connection):
        response = connection.serveradmin.get_diagnostics()
        assert_successful_response(response)
