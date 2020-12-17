

new_user = ""
role = ""


def test_create_user(connection):
    response = connection.users.create_user(new_user)
    assert response.status_code == 200


def test_add_role(connection):
    response = connection.users.add_role(313294, role)
    assert response.status_code == 200


def test_deactivate(connection):
    response = connection.users.deactivate(313294)
    assert response.status_code == 200


def test_get_by_uid(connection):
    response = connection.users.get_by_uid(977332095391193583)
    assert response.status_code == 200


def test_get_roles(connection):
    response = connection.users.get_roles(313294)
    assert response.status_code == 200


def test_unblock(connection):
    response = connection.users.unblock(313294)
    assert response.status_code == 200


def test_block(connection):
    response = connection.users.block(313294)
    assert response.status_code == 200


def test_get_all(connection):
    response_gen = connection.users.get_all()
    for response in response_gen:
        assert response.status_code == 200


def test_get_by_username(connection):
    response = connection.users.get_by_username("test-hardcoded@test.com")
    assert response.status_code == 200


def test_get_scim_data_by_uid(connection):
    response = connection.users.get_scim_data_by_uid(977332095391193583)
    assert response.status_code == 200


def test_change_org_assignment(connection):
    response = connection.users.change_org_assignment(313294, 2689)
    assert response.status_code == 204


def test_get_available_roles(connection):
    response = connection.users.get_available_roles()
    assert response.status_code == 200


def test_get_current(connection):
    response = connection.users.get_current()
    assert response.status_code == 200


def test_reactivate(connection):
    response = connection.users.get_roles(313294)
    assert response.status_code == 200


def test_get_by_id(connection):
    response = connection.users.get_by_id(313294)
    assert response.status_code == 200


def test_get_page(connection):
    response = connection.users.get_page(1)
    assert response.status_code == 200


def test_remove_role(connection):
    response = connection.users.remove_role(313294, role)
    assert response.status_code == 200
