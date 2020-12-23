role = "Desktop User"


def test_add_role(connection, new_user):
    response = connection.users.add_role(new_user["userId"], role)
    assert response.status_code == 200


def test_deactivate(connection, new_user):
    response = connection.users.deactivate(new_user["userId"])
    assert response.status_code == 201


def test_get_by_uid(connection, new_user):
    response = connection.users.get_by_uid(new_user["userUid"])
    assert response.status_code == 200


def test_get_roles(connection, new_user):
    response = connection.users.get_roles(new_user["userId"])
    assert response.status_code == 200


def test_unblock(connection, new_user):
    response = connection.users.unblock(new_user["userId"])
    assert response.status_code == 204


def test_block(connection, new_user):
    response = connection.users.block(new_user["userId"])
    assert response.status_code == 201


def test_get_all(connection):
    response_gen = connection.users.get_all()
    for response in response_gen:
        assert response.status_code == 200


def test_get_by_username(connection, new_user):
    response = connection.users.get_by_username(new_user["username"])
    assert response.status_code == 200


def test_get_scim_data_by_uid(connection, new_user):
    response = connection.users.get_scim_data_by_uid(new_user["userUid"])
    assert response.status_code == 200


def test_change_org_assignment(connection, new_user, org):
    response = connection.users.change_org_assignment(
        new_user["userId"], org["parentOrgId"]
    )
    assert response.status_code == 204


def test_get_available_roles(connection):
    response = connection.users.get_available_roles()
    assert response.status_code == 200


def test_get_current(connection):
    response = connection.users.get_current()
    assert response.status_code == 200


def test_reactivate(connection, new_user):
    response = connection.users.get_roles(new_user["userId"])
    assert response.status_code == 200


def test_get_by_id(connection, new_user):
    response = connection.users.get_by_id(new_user["userId"])
    assert response.status_code == 200


def test_get_page(connection):
    response = connection.users.get_page(1)
    assert response.status_code == 200


def test_remove_role(connection, new_user):
    response = connection.users.remove_role(new_user["userId"], role)
    assert response.status_code == 204
