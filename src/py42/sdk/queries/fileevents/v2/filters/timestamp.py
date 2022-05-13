from py42.choices import Choices as _Choices
from py42.sdk.queries.fileevents.util import (
    FileEventFilterTimestampField as _FileEventFilterTimestampField,
)


class Timestamp(_FileEventFilterTimestampField, _Choices):
    """V2 filter class that filters events based on the timestamp of the event that occurred.

    Available event timestamp constants are provided as class attributes, These
    constants should be used only with class method `within_the_last`:

        - :attr:`timestamp.Timestamp.FIFTEEN_MINUTES`
        - :attr:`timestamp.Timestamp.ONE_HOUR`
        - :attr:`timestamp.Timestamp.THREE_HOURS`
        - :attr:`timestamp.Timestamp.TWELVE_HOURS`
        - :attr:`timestamp.Timestamp.ONE_DAY`
        - :attr:`timestamp.Timestamp.THREE_DAYS`
        - :attr:`timestamp.Timestamp.SEVEN_DAYS`
        - :attr:`timestamp.Timestamp.FOURTEEN_DAYS`
        - :attr:`timestamp.Timestamp.THIRTY_DAYS`

    Example::
        filter = timestamp.Timestamp.within_the_last(EventTimestamp.SEVEN_DAYS)
    """

    _term = "@timestamp"

    FIFTEEN_MINUTES = "PT15M"
    ONE_HOUR = "PT1H"
    THREE_HOURS = "PT3H"
    TWELVE_HOURS = "PT12H"
    ONE_DAY = "P1D"
    THREE_DAYS = "P3D"
    SEVEN_DAYS = "P7D"
    FOURTEEN_DAYS = "P14D"
    THIRTY_DAYS = "P30D"
