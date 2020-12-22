from datetime import datetime

import pytest

timestamp = str(int(datetime.utcnow().timestamp()))
new_org = "integration test org {}".format(timestamp)


@pytest.fixture(scope="module")
def org(connection):
    orgs_gen = connection.orgs.get_all()
    orgs = next(orgs_gen)
    # Assumption: Parent org always exists.
    org = orgs["orgs"][0]  # The first record is always the parent org
    response = connection.orgs.create_org(new_org, parent_org_uid=org["orgUid"])
    assert response.status_code == 200
    return response


def test_get_agent_full_disk_access_states(connection, org):
    response = connection.orgs.get_agent_full_disk_access_states(org["orgId"])
    assert response.status_code == 200


def test_get_by_id(connection, org):
    response = connection.orgs.get_by_id(org["orgId"])
    assert response.status_code == 200


def test_get_page(connection):
    response = connection.orgs.get_page(1)
    assert response.status_code == 200


def test_get_agent_state(connection, org):
    response = connection.orgs.get_agent_state(org["orgId"], "fullDiskAccess")
    assert response.status_code == 200


def test_get_by_uid(connection, org):
    response = connection.orgs.get_by_uid(org["orgUid"])
    assert response.status_code == 200


def test_deactivate(connection, org):
    response = connection.orgs.deactivate(org["orgId"])
    assert response.status_code == 201


def test_reactivate(connection, org):
    response = connection.orgs.reactivate(org["orgId"])
    assert response.status_code == 204


def test_get_all(connection):
    response_gen = connection.orgs.get_all()
    for response in response_gen:
        assert response.status_code == 200


def test_get_current(connection):
    response = connection.orgs.get_current()
    assert response.status_code == 200


def test_block(connection, org):
    response = connection.orgs.block(org["orgId"])
    assert response.status_code == 201


def test_unblock(connection, org):
    response = connection.orgs.unblock(org["orgId"])
    assert response.status_code == 204
