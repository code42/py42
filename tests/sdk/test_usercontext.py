import pytest

from py42.clients.administration import AdministrationClient
from py42.sdk.usercontext import UserContext

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


class TestUserContext(object):
    @pytest.fixture
    def successful_administration_client(self, mocker, py42_response):
        mock_administration_client = mocker.MagicMock(spec=AdministrationClient)
        py42_response.text = _GET_CURRENT_USER
        mock_administration_client.get_current_tenant.return_value = py42_response
        return mock_administration_client

    def test_get_current_tenant_id_returns_tenant_id_from_administration_client_get_current_tenant(
        self, successful_administration_client
    ):
        expected = "00999888-7776-6655-5444-333222111000"
        actual = UserContext(successful_administration_client).get_current_tenant_id()
        assert actual == expected
