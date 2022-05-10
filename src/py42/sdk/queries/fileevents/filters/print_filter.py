from py42.sdk.queries.fileevents.file_event_query import FileEventFilterStringField


class Printer(FileEventFilterStringField):
    """V1 filter class that filters events by printer name."""

    _term = "printerName"


class PrintJobName(FileEventFilterStringField):
    """V1 filter class that filters events by print job name."""

    _term = "printJobName"
