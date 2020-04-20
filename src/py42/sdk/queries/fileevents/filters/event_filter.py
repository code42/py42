from py42.sdk.queries.fileevents.file_event_query import FileEventFilterStringField
from py42.sdk.queries.query_filter import QueryFilterTimestampField


class EventTimestamp(QueryFilterTimestampField):
    """Class that filters events based on the timestamp of the event that occurred."""

    _term = u"eventTimestamp"


class EventType(FileEventFilterStringField):
    """Class that filters file events based on event type.

    Available event types are provided as class attributes:

        - :attr:`EventType.CREATED`
        - :attr:`EventType.DELETED`
        - :attr:`EventType.EMAILED`
        - :attr:`EventType.MODIFIED`
        - :attr:`EventType.READ_BY_APP`

    Example::

        filter = EventType.isin([EventType.READ_BY_APP, EventType.EMAILED])

    """

    _term = u"eventType"

    CREATED = u"CREATED"
    MODIFIED = u"MODIFIED"
    DELETED = u"DELETED"
    READ_BY_APP = u"READ_BY_APP"
    EMAILED = u"EMAILED"


class InsertionTimestamp(QueryFilterTimestampField):
    """Class that filters events based on the timestamp of when the event was actually added to the
    event store (which can be after the event occurred on the device itself).

    `value` must be a POSIX timestamp. (see the :ref:`Dates <anchor_dates>` section of the Basics
    user guide for details on timestamp arguments in py42)
    """

    _term = u"insertionTimestamp"


class Source(FileEventFilterStringField):
    _term = u"source"
