import os
from datetime import datetime

import pytest

import py42.sdk as _sdk

timestamp = str(int(datetime.utcnow().timestamp()))


def pytest_addoption(parser):
    parser.addini("host_url", "Application/enviroment to connect to")


@pytest.fixture(scope='session')
def host(request):
    return request.config.getini("host_url")


@pytest.fixture(scope="session")
def connection(host):
    return _sdk.from_local_account(
        host, os.environ["C42_USER"], os.environ["C42_PW"]
    )


@pytest.fixture(scope="session")
def new_user(connection):
    new_user = "integration_user_{}_@test.com".format(timestamp)
    org_uid = "890854247383106706"
    response = connection.users.create_user(org_uid, new_user, new_user)
    assert response.status_code == 200
    return response


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
