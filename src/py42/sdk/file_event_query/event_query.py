from py42._internal.filters.file_event_filter import _FileEventFilterStringField
from py42._internal.filters.query_filter import _QueryFilterTimestampField, FilterGroup


class EventTimestamp(_QueryFilterTimestampField):
    _term = u"eventTimestamp"


class EventType(_FileEventFilterStringField):
    _term = u"eventType"

    class EventTypeEnum(object):
        def __init__(self, value):
            self._value = value

        def __repr__(self):
            return self._value

    CREATED = EventTypeEnum(u"CREATED")
    MODIFIED = EventTypeEnum(u"MODIFIED")
    DELETED = EventTypeEnum(u"DELETED")
    READ_BY_APP = EventTypeEnum(u"READ_BY_APP")

    @classmethod
    def eq(cls, value):
        # type: (EventTypeEnum) -> FilterGroup
        return super(EventType, cls).eq(str(value))

    @classmethod
    def not_eq(cls, value):
        # type: (EventTypeEnum) -> FilterGroup
        return super(EventType, cls).not_eq(str(value))

    @classmethod
    def is_in(cls, value_list):
        # type: (iter[EventTypeEnum]) -> FilterGroup
        return super(EventType, cls).is_in([str(value) for value in value_list])

    @classmethod
    def not_in(cls, value_list):
        # type: (iter[EventTypeEnum]) -> FilterGroup
        return super(EventType, cls).not_in([str(value) for value in value_list])


class InsertionTimestamp(_QueryFilterTimestampField):
    _term = u"insertionTimestamp"


class Source(_FileEventFilterStringField):
    _term = u"source"
