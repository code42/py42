import os
from datetime import datetime

import pytest

import py42.sdk as _sdk

timestamp = str(int(datetime.utcnow().timestamp()))


def pytest_addoption(parser):
    parser.addini("host_url", "Application/enviroment to connect to.")
    parser.addini("alert_id", "Alert id that exists in the system.")
    parser.addini("device_id", "Device id that exists in the system.")
    parser.addini("observer_rule_id", "Observer rule id.")



@pytest.fixture(scope='session')
def host(request):
    return request.config.getini("host_url")


@pytest.fixture(scope='session')
def alert_id(request):
    return request.config.getini("alert_id")


@pytest.fixture(scope='session')
def observer_id(request):
    return request.config.getini("observer_rule_id")


@pytest.fixture(scope="session")
def connection(host):
    return _sdk.from_local_account(
        host, os.environ["C42_USER"], os.environ["C42_PW"]
    )


@pytest.fixture(scope="session")
def org(connection):
    orgs_gen = connection.orgs.get_all()
    orgs = next(orgs_gen)
    # Assumption: Parent org always exists.
    org = orgs["orgs"][0]  # The first record is always the parent org
    new_org = "integration test org {}".format(timestamp)
    response = connection.orgs.create_org(new_org, parent_org_uid=org["orgUid"])
    assert response.status_code == 200
    return response


@pytest.fixture(scope="session")
def new_user(connection, org):
    new_user = "integration_user_{}_@test.com".format(timestamp)
    response = connection.users.create_user(org['orgUid'], new_user, new_user)
    assert response.status_code == 200
    return response


@pytest.fixture(scope='session')
def device(request, connection):
    device_id = request.config.getini('device_id')
    return connection.devices.get_by_id(device_id)
