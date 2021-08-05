import sys

from py42.__version__ import __version__

proxies = None

# Controls whether we verify the server's certificate.
# True, False, or a path to a CA bundle to use.
verify_ssl_certs = True

items_per_page = 500
security_events_per_page = 10000

_custom_user_suffix = ""
_python_version = f"{sys.version_info[0]}.{sys.version_info[1]}.{sys.version_info[2]}"


def get_user_agent_string():
    return "py42 {} python {}{}".format(
        __version__, _python_version, _custom_user_suffix
    )


def set_user_agent_suffix(suffix):
    global _custom_user_suffix
    _custom_user_suffix = f" {suffix}"
