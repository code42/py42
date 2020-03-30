from py42.sdk.queries.fileevents.file_event_query import FileEventFilterStringField
from py42.sdk.queries.query_filter import QueryFilterTimestampField


class EventTimestamp(QueryFilterTimestampField):
    """Class that filters events based on the timestamp event occurred."""

    _term = u"eventTimestamp"


class EventType(FileEventFilterStringField):
    """Class that filters file events based on event type."""

    _term = u"eventType"

    CREATED = u"CREATED"
    MODIFIED = u"MODIFIED"
    DELETED = u"DELETED"
    READ_BY_APP = u"READ_BY_APP"


class InsertionTimestamp(QueryFilterTimestampField):
    """Class that filters events based on the timestamp the event was actually added to the event
    store (which can be after the event occurred on the device itself).
    """

    _term = u"insertionTimestamp"


class Source(FileEventFilterStringField):
    _term = u"source"
