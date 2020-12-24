import os
from datetime import datetime

import pytest

import py42.sdk as _sdk


def pytest_addoption(parser):
    parser.addini("host_url", "Application/enviroment to connect to.")
    parser.addini("alert_id", "Alert id that exists in the system.")
    parser.addini("device_id", "Device id that exists in the system.")
    parser.addini("observer_rule_id", "Observer rule id.")
    parser.addini("md5_hash", "MD5 hash of a file that exists on the device.")
    parser.addini("sha256_hash", "SHA256 hash of a file that exists on the device.")
    parser.addini(
        "user_uid", "The UID of the user to get plan storage information for."
    )
    parser.addini("device_guid", "Device guid from which archival was done.")
    parser.addini("destination_device_guid", "Device guid to which archival was done.")
    parser.addini("archive_guid", "Guid of the archival.")
    parser.addini("path", "Complete path of the file with filename which was archived.")
    parser.addini("file_data", "Content of the file during archival.")


@pytest.fixture(scope="session")
def host(request):
    return request.config.getini("host_url")


@pytest.fixture(scope="session")
def alert_id(request):
    return request.config.getini("alert_id")


@pytest.fixture(scope="session")
def observer_id(request):
    return request.config.getini("observer_rule_id")


@pytest.fixture(scope="session")
def connection(host):
    return _sdk.from_local_account(host, os.environ["C42_USER"], os.environ["C42_PW"])


@pytest.fixture(scope="session")
def timestamp():
    return str(int(datetime.utcnow().timestamp()))


@pytest.fixture(scope="session")
def org(connection, timestamp):
    orgs_gen = connection.orgs.get_all()
    orgs = next(orgs_gen)
    # Assumption: Parent org always exists.
    org = orgs["orgs"][0]  # The first record is always the parent org
    new_org = "integration test org {}".format(timestamp)
    response = connection.orgs.create_org(new_org, parent_org_uid=org["orgUid"])
    assert response.status_code == 200
    return response


@pytest.fixture(scope="session")
def new_user(connection, org, timestamp):
    new_user = "integration_user_{}_@test.com".format(timestamp)
    response = connection.users.create_user(org["orgUid"], new_user, new_user)
    assert response.status_code == 200
    return response


@pytest.fixture(scope="session")
def device(request, connection):
    device_id = request.config.getini("device_id")
    return connection.devices.get_by_id(device_id)
