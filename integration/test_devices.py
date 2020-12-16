import pytest


device_uid = "891804948033320117"


def test_block(connection):
    response = connection.devices.block(251691)
    assert response.status_code == 201


@pytest.mark.skip("Skip special case.")
def test_get_agent_full_disk_access_state(connection):
    response = connection.devices.get_agent_full_disk_access_state(device_uid)
    assert response.status_code == 200


def test_get_by_guid(connection):
    response = connection.devices.get_by_guid(device_uid)
    assert response.status_code == 200


def test_get_settings(connection):
    response = connection.devices.get_settings(device_uid)
    assert response.guid == device_uid


def test_deactivate(connection):
    response = connection.devices.deactivate(251691)
    assert response.status_code == 204


@pytest.mark.skip("Skip special case.")
def test_get_agent_state(connection):
    response = connection.devices.get_agent_state(device_uid, "fullDiskAccess")
    assert response.status_code == 200


def test_get_by_id(connection):
    response = connection.devices.get_by_id(49344)
    assert response.status_code == 200


def test_deauthorize(connection):
    response = connection.devices.deauthorize(251691)
    assert response.status_code == 204


def test_reactivate(connection):
    response = connection.devices.reactivate(251691)
    assert response.status_code == 204


def test_get_all(connection):
    response_gen = connection.devices.get_all()
    for response in response_gen:
        assert response.status_code == 200
        break


def test_get_page(connection):
    response = connection.devices.get_page(1)
    assert response.status_code == 200


def test_unblock(connection):
    response = connection.devices.unblock(251691)
    assert response.status_code == 204
