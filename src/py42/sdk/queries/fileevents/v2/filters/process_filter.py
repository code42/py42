from py42.sdk.queries.fileevents.file_event_query import FileEventFilterStringField


class ProcessName(FileEventFilterStringField):
    """V2 filter class that filters events based on the process name involved in the exposure (applies to
    ``read by browser or other app`` events only).
    """

    _term = "process.executable"


class ProcessOwner(FileEventFilterStringField):
    """V2 filter class that filters events based on the process owner that was involved in the exposure
    (applies to ``read by browser or other app`` events only).
    """

    _term = "process.owner"
