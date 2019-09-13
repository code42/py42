import py42.debug_level as debug_level
import py42.settings as settings


def will_print_for(level):
    return (debug_level.NONE <= level <= debug_level.TRACE) and settings.debug_level >= level
