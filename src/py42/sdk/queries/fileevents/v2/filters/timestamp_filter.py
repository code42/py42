from py42.choices import Choices
from py42.sdk.queries.fileevents.file_event_query import FileEventFilterTimestampField


class EventTimestamp(FileEventFilterTimestampField, Choices):
    """Class that filters events based on the timestamp of the event that occurred.

    Available event timestamp constants are provided as class attributes, These
    constants should be used only with class method `within_the_last`:

        - :attr:`EventTimestamp.FIFTEEN_MINUTES`
        - :attr:`EventTimestamp.ONE_HOUR`
        - :attr:`EventTimestamp.THREE_HOURS`
        - :attr:`EventTimestamp.TWELVE_HOURS`
        - :attr:`EventTimestamp.ONE_DAY`
        - :attr:`EventTimestamp.THREE_DAYS`
        - :attr:`EventTimestamp.SEVEN_DAYS`
        - :attr:`EventTimestamp.FOURTEEN_DAYS`
        - :attr:`EventTimestamp.THIRTY_DAYS`

    Example::
        filter = EventTimestamp.within_the_last(EventTimestamp.SEVEN_DAYS)
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
