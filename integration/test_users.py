from datetime import datetime


new_user = "integration_" + str(int(datetime.now().timestamp())) + "_@test.com"
org_uid = "890854247383106706"
new_user_email = new_user
role = "Desktop User"
user_uid = 977332095391193583
user_id = 313294
update_org_id = 2689


def test_create_user(connection):
    response = connection.users.create_user(org_uid, new_user, new_user_email)
    assert response.status_code == 200


def test_add_role(connection):
    response = connection.users.add_role(user_id, role)
    assert response.status_code == 200


def test_deactivate(connection):
    response = connection.users.deactivate(user_id)
    assert response.status_code == 201


def test_get_by_uid(connection):
    response = connection.users.get_by_uid(user_uid)
    assert response.status_code == 200


def test_get_roles(connection):
    response = connection.users.get_roles(user_id)
    assert response.status_code == 200


def test_unblock(connection):
    response = connection.users.unblock(user_id)
    assert response.status_code == 204


def test_block(connection):
    response = connection.users.block(user_id)
    assert response.status_code == 201


def test_get_all(connection):
    response_gen = connection.users.get_all()
    for response in response_gen:
        assert response.status_code == 200


def test_get_by_username(connection):
    response = connection.users.get_by_username(new_user)
    assert response.status_code == 200


def test_get_scim_data_by_uid(connection):
    response = connection.users.get_scim_data_by_uid(user_uid)
    assert response.status_code == 200


def test_change_org_assignment(connection):
    response = connection.users.change_org_assignment(user_id, update_org_id)
    assert response.status_code == 204


def test_get_available_roles(connection):
    response = connection.users.get_available_roles()
    assert response.status_code == 200


def test_get_current(connection):
    response = connection.users.get_current()
    assert response.status_code == 200


def test_reactivate(connection):
    response = connection.users.get_roles(user_id)
    assert response.status_code == 200


def test_get_by_id(connection):
    response = connection.users.get_by_id(user_id)
    assert response.status_code == 200


def test_get_page(connection):
    response = connection.users.get_page(1)
    assert response.status_code == 200


def test_remove_role(connection):
    response = connection.users.remove_role(user_id, role)
    assert response.status_code == 204
