from py42.sdk.queries.fileevents.file_event_query import FileEventFilterStringField
from py42.sdk.queries.query_filter import QueryFilterTimestampField


class EventTimestamp(QueryFilterTimestampField):
    _term = u"eventTimestamp"


class EventType(FileEventFilterStringField):
    _term = u"eventType"

    CREATED = u"CREATED"
    MODIFIED = u"MODIFIED"
    DELETED = u"DELETED"
    READ_BY_APP = u"READ_BY_APP"


class InsertionTimestamp(QueryFilterTimestampField):
    _term = u"insertionTimestamp"


class Source(FileEventFilterStringField):
    _term = u"source"
