import logging
import sys


class _DebugSettings:
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


sys.modules[__name__] = _DebugSettings()
