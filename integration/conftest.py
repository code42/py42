import os
from datetime import datetime

import pytest

import py42.sdk as _sdk

HOST_URL = "https://console.us.code42.com"


@pytest.fixture(scope="session")
def connection():
    return _sdk.from_local_account(
        HOST_URL, os.environ["C42_USER"], os.environ["C42_PW"]
    )


@pytest.fixture(scope="session")
def new_user(connection):
    new_user = "integration_" + str(int(datetime.now().timestamp())) + "_@test.com"
    org_uid = "890854247383106706"
    response = connection.users.create_user(org_uid, new_user, new_user)
    assert response.status_code == 200
    return response
