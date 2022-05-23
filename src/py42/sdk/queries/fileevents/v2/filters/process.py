from py42.sdk.queries.fileevents.util import (
    FileEventFilterStringField as _FileEventFilterStringField,
)


class Executable(_FileEventFilterStringField):
    """V2 filter class that filters events based on the process name involved in the exposure (applies to
    ``read by browser or other app`` events only).
    """

    _term = "process.executable"


class Owner(_FileEventFilterStringField):
    """V2 filter class that filters events based on the process owner that was involved in the exposure
    (applies to ``read by browser or other app`` events only).
    """

    _term = "process.owner"
