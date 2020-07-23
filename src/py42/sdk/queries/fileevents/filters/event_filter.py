from py42.sdk.queries.fileevents.file_event_query import FileEventFilterStringField
from py42.sdk.queries.query_filter import filter_attributes
from py42.sdk.queries.query_filter import QueryFilterTimestampField


class EventTimestamp(QueryFilterTimestampField):
    """Class that filters events based on the timestamp of the event that occurred.

    Example::
        filter = EventTimestamp.within_the_period(EventTimestamp.SEVEN_DAYS)
    """

    _term = u"eventTimestamp"

    FIFTEEN_MINUTES = u"PT15M"
    ONE_HOUR = u"PT1H"
    THREE_HOURS = u"PT3H"
    TWELVE_HOURS = u"PT12H"
    ONE_DAY = u"P1D"
    THREE_DAYS = u"P3D"
    SEVEN_DAYS = u"P7D"
    FOURTEEN_DAYS = u"P14D"
    THIRTY_DAYS = u"P30D"

    @staticmethod
    def choices():
        return filter_attributes(EventTimestamp)


class EventType(FileEventFilterStringField):
    """Class that filters file events based on event type.

    Available event types are provided as class attributes:

        - :attr:`EventType.CREATED`
        - :attr:`EventType.DELETED`
        - :attr:`EventType.EMAILED`
        - :attr:`EventType.MODIFIED`
        - :attr:`EventType.READ_BY_APP`
        - :attr:`EventType.PRINTED`

    Example::

        filter = EventType.isin([EventType.READ_BY_APP, EventType.EMAILED])

    """

    _term = u"eventType"

    CREATED = u"CREATED"
    MODIFIED = u"UPDATED"
    DELETED = u"DELETED"
    READ_BY_APP = u"READ_BY_APP"
    EMAILED = u"EMAILED"
    PRINTED = u"PRINTED"

    @staticmethod
    def choices():
        return filter_attributes(EventType)


class InsertionTimestamp(QueryFilterTimestampField):
    """Class that filters events based on the timestamp of when the event was actually added to the
    event store (which can be after the event occurred on the device itself).

    `value` must be a POSIX timestamp. (see the :ref:`Dates <anchor_dates>` section of the Basics
    user guide for details on timestamp arguments in py42)
    """

    _term = u"insertionTimestamp"


class Source(FileEventFilterStringField):
    """Class that filters events by event source.

    Available event types are provided as class attributes:
        - :attr:`Source.ENDPOINT`
        - :attr:`Source.GOOGLE_DRIVE`
        - :attr:`Source.ONE_DRIVE`
        - :attr:`Source.BOX`
        - :attr:`Source.GMAIL`
        - :attr:`Source.OFFICE_365`

    """

    _term = u"source"

    ENDPOINT = u"Endpoint"
    GOOGLE_DRIVE = u"GoogleDrive"
    ONE_DRIVE = u"OneDrive"
    BOX = u"Box"
    GMAIL = u"Gmail"
    OFFICE_365 = u"Office365"

    @staticmethod
    def choices():
        return filter_attributes(Source)
