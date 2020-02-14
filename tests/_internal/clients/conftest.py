import pytest

from py42._internal.clients.administration import AdministrationClient


@pytest.fixture
def administration_client(mocker):
    client = mocker.MagicMock(spec=AdministrationClient)
    client.get_current_tenant_id.return_value = "00000000-0000-0000-0000-000000000000"
    return client
