import pytest

from py42._internal.user_context import UserContext


@pytest.fixture
def user_context(mocker):
    client = mocker.MagicMock(spec=UserContext)
    client.get_current_tenant_id.return_value = "00000000-0000-0000-0000-000000000000"
    return client
