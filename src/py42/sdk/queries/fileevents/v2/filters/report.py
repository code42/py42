from py42.sdk.queries.fileevents.util import (
    FileEventFilterComparableField as _FileEventFilterComparableField,
)
from py42.sdk.queries.fileevents.util import (
    FileEventFilterStringField as _FileEventFilterStringField,
)


class ID(_FileEventFilterStringField):
    """V2 filter class that filters events by the ID of the report."""

    _term = "report.id"


class Name(_FileEventFilterStringField):
    """V2 filter class that filters events by the name of the report."""

    _term = "report.name"


class Description(_FileEventFilterStringField):
    """V2 filter class that filters events by the description of the report."""

    _term = "report.description"


class Headers(_FileEventFilterStringField):
    """V2 filter class that filters events by the header(s) of the report."""

    _term = "report.headers"


class Count(_FileEventFilterStringField, _FileEventFilterComparableField):
    """V2 filter class that filters events by the record count of the report."""

    _term = "report.count"


class Type(_FileEventFilterStringField):
    """V2 filter class that filters events by the type of the report.

    Available options are provided as class attributes:
        - :attr: `report.Type.AD_HOC`
        - :attr: `report.Type.SAVED`
    """

    _term = "report.type"

    AD_HOC = "REPORT_TYPE_AD_HOC"
    SAVED = "REPORT_TYPE_SAVED"
