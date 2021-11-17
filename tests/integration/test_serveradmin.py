import pytest
from tests.integration.conftest import assert_successful_response


@pytest.mark.integration
class TestServerAdmin:
    def test_get_current_tenant(self, connection):
        response = connection.serveradmin.get_current_tenant()
        assert_successful_response(response)
