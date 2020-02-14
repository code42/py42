import pytest

from py42._internal.customer import Customer


@pytest.fixture
def customer(mocker):
    client = mocker.MagicMock(spec=Customer)
    client.get_current_tenant_id.return_value = "00000000-0000-0000-0000-000000000000"
    return client
