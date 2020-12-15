import os

import pytest

import py42.sdk as _sdk

HOST_URL = "https://console.us.code42.com"


@pytest.fixture(scope="session")
def connection():
    return _sdk.from_local_account(
        HOST_URL, os.environ["C42_USER"], os.environ["C42_PW"]
    )
