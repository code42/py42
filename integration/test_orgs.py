import pytest

SKIP_TEST_MESSAGE = "Changes system state."


@pytest.mark.skip(SKIP_TEST_MESSAGE)
def test_block():
    pass


def test_get_agent_full_disk_access_states(connection):
    response = connection.orgs.get_agent_full_disk_access_states(2689)
    assert response.status_code == 200


def test_get_by_id(connection):
    response = connection.orgs.get_by_id(2689)
    assert response.status_code == 200


def test_get_page(connection):
    response = connection.orgs.get_page(1)
    assert response.status_code == 200


@pytest.mark.skip("Changes system state.")
def test_create_org():
    pass


def test_get_agent_state(connection):
    response = connection.orgs.get_agent_state(2689, "fullDiskAccess")
    assert response.status_code == 200


def test_get_by_uid(connection):
    response = connection.orgs.get_by_uid(890854247383106706)
    assert response.status_code == 200


@pytest.mark.skip(SKIP_TEST_MESSAGE)
def test_reactivate():
    pass


@pytest.mark.skip(SKIP_TEST_MESSAGE)
def test_deactivate():
    pass


def test_get_all(connection):
    response_gen = connection.orgs.get_all()
    for response in response_gen:
        assert response.status_code == 200


def test_get_current(connection):
    response = connection.orgs.get_current()
    assert response.status_code == 200


@pytest.mark.skip(SKIP_TEST_MESSAGE)
def test_unblock():
    pass
