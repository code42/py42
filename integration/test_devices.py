import pytest


@pytest.mark.skip("Failing with 403.")
def test_block(connection):
    response = connection.devices.block(891804948033320117)
    assert response.status_code == 201


@pytest.mark.skip("Failing with 404.")
def test_get_agent_full_disk_access_state(connection):
    response = connection.devices.get_agent_full_disk_access_state(891804948033320117)
    assert response.status_code == 200


def test_get_by_guid(connection):
    response = connection.devices.get_by_guid(891804948033320117)
    assert response.status_code == 200


def test_get_settings(connection):
    response = connection.devices.get_settings(891804948033320117)
    assert response.status_code == 200


@pytest.mark.skip("Failing with 403.")
def test_deactivate(connection):
    response = connection.devices.deactivate(891804948033320117)
    assert response.status_code == 200


@pytest.mark.skip("Failing with 404.")
def test_get_agent_state(connection):
    response = connection.devices.get_agent_state(891804948033320117, "fullDiskAccess")
    assert response.status_code == 200


def test_get_by_id(connection):
    response = connection.devices.get_by_id(49344)
    assert response.status_code == 200


@pytest.mark.skip("Failing with 403.")
def test_deauthorize(connection):
    response = connection.devices.deauthorize(891804948033320117)
    assert response.status_code == 201


@pytest.mark.skip("Failing with 403.")
def test_reactivate(connection):
    response = connection.devices.reactivate(891804948033320117)
    assert response.status_code == 201


def test_get_all(connection):
    response_gen = connection.devices.get_all()
    for response in response_gen:
        assert response.status_code == 200
        break


def test_get_page(connection):
    response = connection.devices.get_page(1)
    assert response.status_code == 200


@pytest.mark.skip("Failing with 403.")
def test_unblock(connection):
    response = connection.devices.unblock(891804948033320117)
    assert response.status_code == 201
