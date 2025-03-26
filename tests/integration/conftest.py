import os
from datetime import datetime

import pytest

import pycpg.sdk as _sdk
from pycpg.util import convert_datetime_to_epoch


def pytest_addoption(parser):
    parser.addini("device_id", "Device id that exists in the system.")
    parser.addini(
        "user_uid", "The UID of the user to get plan storage information for."
    )
    parser.addini("device_guid", "Device guid from which archival was done.")
    parser.addini("destination_device_guid", "Device guid to which archival was done.")
    parser.addini("archive_guid", "Guid of the archival.")
    parser.addini("path", "Complete path of the file with filename which was archived.")


@pytest.fixture(scope="session")
def connection():
    host = os.environ.get("CPG_HOST") or "http://127.0.0.1:4200"
    user = os.environ.get("CPG_USER") or "test.user@example.com"
    pw = os.environ.get("CPG_PW") or "password"
    return _get_sdk(host, user, pw)


def _get_sdk(host, user, pw):
    try:
        return _sdk.from_local_account(host, user, pw)
    except Exception as err:
        pytest.exit(
            f"Failed to init SDK for integration tests: {err}",
            returncode=1,
        )


@pytest.fixture(scope="session")
def api_client_connection():
    host = os.environ.get("CPG_HOST") or "http://127.0.0.1:4200"
    client = os.environ.get("CPG_API_CLIENT_ID") or "client_id"
    secret = os.environ.get("CPG_API_CLIENT_SECRET") or "secret"
    return _get_api_client_sdk(host, client, secret)


def _get_api_client_sdk(host, client, secret):
    try:
        return _sdk.from_api_client(host, client, secret)
    except Exception as err:
        pytest.exit(
            f"Failed to init API client SDK for integration tests: {err}",
            returncode=1,
        )


@pytest.fixture(scope="session")
def timestamp():
    return convert_datetime_to_epoch(datetime.utcnow())


@pytest.fixture(scope="session")
def org(connection, timestamp):
    orgs_gen = connection.orgs.get_all()
    orgs = next(orgs_gen)
    # Assumption: Parent org always exists.
    org = orgs["orgs"][0]  # The first record is always the parent org
    new_org = f"integration test org {timestamp}"
    response = connection.orgs.create_org(new_org, parent_org_uid=org["orgUid"])
    assert response.status_code == 200
    return response


@pytest.fixture(scope="session")
def new_user(connection, org, timestamp):
    new_user = f"integration_user_{timestamp}_@test.com"
    response = connection.users.create_user(org["orgUid"], new_user, new_user)
    assert response.status_code == 200
    return response


@pytest.fixture(scope="session")
def device(request, connection):
    device_id = request.config.getini("device_id")
    return connection.devices.get_by_id(device_id)


def assert_successful_response(response):
    assert 200 <= response.status_code < 300
