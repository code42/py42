from datetime import datetime

import pytest

from py42.exceptions import Py42ForbiddenError
from py42.exceptions import Py42InternalServerError


timestamp = str(int(datetime.now().timestamp()))
new_org = "integration test org {}".format(timestamp)
org_id = 2689
org_uid = 890854247383106706


def test_create_org(connection):
    with pytest.raises(Py42ForbiddenError):
        connection.orgs.create_org(new_org)


def test_get_agent_full_disk_access_states(connection):
    response = connection.orgs.get_agent_full_disk_access_states(org_id)
    assert response.status_code == 200


def test_get_by_id(connection):
    response = connection.orgs.get_by_id(org_id)
    assert response.status_code == 200


def test_get_page(connection):
    response = connection.orgs.get_page(1)
    assert response.status_code == 200


def test_get_agent_state(connection):
    response = connection.orgs.get_agent_state(org_id, "fullDiskAccess")
    assert response.status_code == 200


def test_get_by_uid(connection):
    response = connection.orgs.get_by_uid(org_uid)
    assert response.status_code == 200


def test_deactivate(connection):
    with pytest.raises(Py42ForbiddenError):
        connection.orgs.deactivate(org_id)


def test_reactivate(connection):
    with pytest.raises(Py42ForbiddenError):
        connection.orgs.reactivate(org_id)


def test_get_all(connection):
    response_gen = connection.orgs.get_all()
    for response in response_gen:
        assert response.status_code == 200


def test_get_current(connection):
    response = connection.orgs.get_current()
    assert response.status_code == 200


def test_block(connection):
    with pytest.raises(Py42InternalServerError):
        connection.orgs.block(org_id)


def test_unblock(connection):
    with pytest.raises(Py42ForbiddenError):
        connection.orgs.unblock(org_id)
