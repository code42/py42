import pytest

from py42._internal.user_context import UserContext

TENANT_ID_FROM_RESPONSE = "00000000-0000-0000-0000-000000000000"


@pytest.fixture
def user_context(mocker):
    client = mocker.MagicMock(spec=UserContext)
    client.get_current_tenant_id.return_value = TENANT_ID_FROM_RESPONSE
    return client
