import pytest


@pytest.mark.skip("Changes device state.")
def test_block():
    pass


@pytest.mark.skip("Failing")
def test_get_agent_full_disk_access_state(connection):
    response = connection.devices.get_agent_full_disk_access_state(891804948033320117)
    assert response.status_code == 200


def test_get_by_guid(connection):
    response = connection.devices.get_by_guid(891804948033320117)
    assert response.status_code == 200


def test_get_settings():
    pass


@pytest.mark.skip("Changes device state.")
def test_deactivate():
    pass


@pytest.mark.skip("Failing")
def test_get_agent_state(connection):
    response = connection.devices.get_agent_state(891804948033320117, "fullDiskAccess")
    assert response.status_code == 200


def test_get_by_id(connection):
    response = connection.devices.get_by_id(49344)
    assert response.status_code == 200


@pytest.mark.skip("Changes device state.")
def test_reactivate():
    pass


@pytest.mark.skip("Changes device state.")
def test_deauthorize():
    pass


def test_get_all(connection):
    response_gen = connection.devices.get_all()
    for response in response_gen:
        assert response.status_code == 200
        break


def test_get_page(connection):
    response = connection.devices.get_page(1)
    assert response.status_code == 200


def test_unblock():
    pass
