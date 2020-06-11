import logging
import sys

from py42.__version__ import __version__

proxies = None

# Controls whether we verify the server's certificate.
# True, False, or a path to a CA bundle to use.
verify_ssl_certs = True

items_per_page = 500

_custom_user_suffix = u""
_python_version = u"{0}.{1}.{2}".format(
    sys.version_info[0], sys.version_info[1], sys.version_info[2]
)


def get_user_agent_string():
    return u"py42 {0} python {1}{2}".format(__version__, _python_version, _custom_user_suffix)


def set_user_agent_suffix(suffix):
    global _custom_user_suffix
    _custom_user_suffix = u" {0}".format(suffix)


class DebugSettings(object):
    INFO = logging.INFO
    DEBUG = logging.DEBUG
    TRACE = logging.DEBUG
    NONE = logging.NOTSET

    def __init__(self):
        self.logger = logging.getLogger("py42")
        self.logger.addHandler(logging.StreamHandler(sys.stderr))

    @property
    def level(self):
        return self.logger.level

    @level.setter
    def level(self, level):
        self.logger.setLevel(level)


debug = DebugSettings()
