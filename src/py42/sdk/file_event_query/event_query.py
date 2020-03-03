from py42._internal.filters.file_event_filter import _FileEventFilterStringField
from py42._internal.filters.query_filter import _QueryFilterTimestampField


class EventTimestamp(_QueryFilterTimestampField):
    _term = u"eventTimestamp"


class EventType(_FileEventFilterStringField):
    _term = u"eventType"

    CREATED = u"CREATED"
    MODIFIED = u"MODIFIED"
    DELETED = u"DELETED"
    READ_BY_APP = u"READ_BY_APP"


class InsertionTimestamp(_QueryFilterTimestampField):
    _term = u"insertionTimestamp"


class Source(_FileEventFilterStringField):
    _term = u"source"
