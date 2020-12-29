import pytest


@pytest.mark.integration
def test_get_current_tenant(connection):
    response = connection.usercontext.get_current_tenant_id()
    assert type(response) == str
    assert len(response) == 36
