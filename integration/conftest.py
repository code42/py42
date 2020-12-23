import os
from datetime import datetime

import pytest

import py42.sdk as _sdk


def pytest_addoption(parser):
    parser.addini("host_url", "Application/enviroment to connect to")


@pytest.fixture
def host(request):
    return request.config.getini("host_url")


@pytest.fixture(scope="session")
def connection(host):
    return _sdk.from_local_account(
        host, os.environ["C42_USER"], os.environ["C42_PW"]
    )


@pytest.fixture(scope="session")
def new_user(connection):
    new_user = "integration_" + str(int(datetime.now().timestamp())) + "_@test.com"
    org_uid = "890854247383106706"
    response = connection.users.create_user(org_uid, new_user, new_user)
    assert response.status_code == 200
    return response
