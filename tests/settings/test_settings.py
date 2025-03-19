import sys

import pytest

import pycpg.settings as settings
from pycpg.__version__ import __version__

DEFAULT_USER_AGENT_FORMAT = "pycpg/{0} python/{1}"


@pytest.fixture
def default_user_agent():
    python_version = (
        f"{sys.version_info[0]}.{sys.version_info[1]}.{sys.version_info[2]}"
    )
    pycpg_version = __version__
    default_user_agent = DEFAULT_USER_AGENT_FORMAT.format(pycpg_version, python_version)
    return default_user_agent


def test_get_user_agent_returns_correct_default_value(default_user_agent):
    assert settings.get_user_agent_string() == default_user_agent
    # reset settings to default
    settings.set_user_agent_suffix("")


def test_get_user_agent_returns_correct_value_after_setting_suffix(default_user_agent):
    settings.set_user_agent_suffix("example-suffix")
    assert settings.get_user_agent_string() == f"{default_user_agent} example-suffix"
    # reset settings to default
    settings.set_user_agent_suffix("")


def test_get_user_agent_returns_correct_value_after_setting_prefix(default_user_agent):
    settings.set_user_agent_prefix("example-prefix")
    assert settings.get_user_agent_string() == f"example-prefix {default_user_agent}"
    # reset settings to default
    settings.set_user_agent_prefix("")
