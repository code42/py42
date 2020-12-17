def test_get_current_tenant(connection):
    response = connection.usercontext.get_current_tenant_id()
    assert response == "1d71796f-af5b-4231-9d8e-df6434da4663"
