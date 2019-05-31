import sys
import py42.debug_level
from py42.__version__ import __version__

proxies = None

global_exception_message_receiver = None

# Controls whether we verify the server's certificate.
# True, False, or a path to a CA bundle to use.
verify_ssl_certs = True

debug_level = py42.debug_level.NONE

_custom_user_suffix = ""
_python_version = "{0}.{1}.{2}".format(sys.version_info[0], sys.version_info[1], sys.version_info[2])


def get_user_agent_string():
    return "py42 {0} python {1}{2}".format(__version__, _python_version, _custom_user_suffix)


def set_user_agent_suffix(suffix):
    py42.settings._custom_user_suffix = " " + suffix
