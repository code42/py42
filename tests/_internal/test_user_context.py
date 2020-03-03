import pytest
from requests import Response

from py42._internal.clients.administration import AdministrationClient
from py42._internal.user_context import UserContext

_GET_CURRENT_USER = """
{
    "data":
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
            }
        },
    "error":null,
    "warnings":null
}
"""


class TestUserContext(object):
    @pytest.fixture
    def successful_administration_client(self, mocker):
        mock_administration_client = mocker.MagicMock(spec=AdministrationClient)
        mock_response = mocker.MagicMock(spec=Response)
        mock_response.status_code = 200
        mock_response.text = _GET_CURRENT_USER
        mock_administration_client.get_current_tenant.return_value = mock_response
        return mock_administration_client

    def test_get_current_tenant_id_returns_tenant_id_from_administration_client_get_current_tenant(
        self, successful_administration_client
    ):
        expected = "00999888-7776-6655-5444-333222111000"
        actual = UserContext(successful_administration_client).get_current_tenant_id()
        assert actual == expected

    def test_get_current_tenant_id_when_administration_client_throws_also_throws(self, mocker):
        administration_client = mocker.MagicMock(spec=AdministrationClient)

        def mock_get_current_tenant():
            raise Exception("Mock error!")

        administration_client.get_current_tenant.side_effect = mock_get_current_tenant

        with pytest.raises(Exception) as e:
            _ = UserContext(administration_client).get_current_tenant_id()

        assert (
            e.value.args[0]
            == "An error occurred while trying to retrieve the current tenant ID, caused by: Mock error!"
        )
