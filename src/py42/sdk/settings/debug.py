# Used by py42.debug to determine whether a debug statement should be printed
# The level is set by py42.sdk.settings.debug_level
NONE = 0
INFO = 1
DEBUG = 2
TRACE = 3

level = NONE


def will_print_for(statement_level):
    return (NONE <= statement_level <= TRACE) and level >= statement_level
