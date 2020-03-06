import py42.debug_level as debug_level
import py42.settings as settings

# Used by py42.debug to determine whether a debug statement should be printed
# The level is set by py42.settings.debug_level
NONE = 0
INFO = 1
DEBUG = 2
TRACE = 3


def will_print_for(level):
    return (debug_level.NONE <= level <= debug_level.TRACE) and settings.debug_level >= level
