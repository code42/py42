from py42.sdk.queries.fileevents.util import (
    FileEventFilterStringField as _FileEventFilterStringField,
)


class Printer(_FileEventFilterStringField):
    """V1 filter class that filters events by printer name."""

    _term = "printerName"


class PrintJobName(_FileEventFilterStringField):
    """V1 filter class that filters events by print job name."""

    _term = "printJobName"
