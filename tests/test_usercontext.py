import pytest
from tests.conftest import create_mock_response

from py42.services.administration import AdministrationService
from py42.usercontext import UserContext

_GET_CURRENT_USER = """
{
    "name":"Test SaaS Cloud",
    "registrationKey":"1777444555888000",
    "deploymentModel":"PUBLIC",
    "maintenanceMode":false,
    "tenantUid":"00999888-7776-6655-5444-333222111000",
    "masterServicesAgreement":
    {
        "accepted":true,
        "acceptanceRequired":false
    },
    "error":null,
    "warnings":null
}
"""


class TestUserContext:
    @pytest.fixture
    def successful_administration_client(self, mocker):
        mock_administration_client = mocker.MagicMock(spec=AdministrationService)
        response = create_mock_response(mocker, _GET_CURRENT_USER)
        mock_administration_client.get_current_tenant.return_value = response
        return mock_administration_client

    def test_get_current_tenant_id_returns_tenant_id_from_administration_client_get_current_tenant(
        self, successful_administration_client
    ):
        expected = "00999888-7776-6655-5444-333222111000"
        actual = UserContext(successful_administration_client).get_current_tenant_id()
        assert actual == expected
