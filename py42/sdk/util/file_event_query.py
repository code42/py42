from py42._internal.file_event_filter import FilterGroup, FileEventFilter
from datetime import datetime


class _FileEventFilterStringField(FileEventFilter):
    @classmethod
    def eq(cls, value):
        # type: (str) -> FilterGroup
        return FilterGroup([cls("IS", value)])

    @classmethod
    def not_eq(cls, value):
        # type: (str) -> FilterGroup
        return FilterGroup([cls("IS_NOT", value)])

    @classmethod
    def is_in(cls, value_list):
        # type: (iter[str]) -> FilterGroup
        return FilterGroup(([cls("IS", value) for value in value_list]),
                           filter_clause="OR")

    @classmethod
    def not_in(cls, value_list):
        # type: (iter[str]) -> FilterGroup
        return FilterGroup(([cls("IS_NOT", value) for value in value_list]))


class _FileEventFilterTimestampField(FileEventFilter):

    @staticmethod
    def _to_timestamp_string(int_value):
        # "2018-12-01T00:00:00.000Z"
        return datetime.fromtimestamp(int_value).strftime("%Y-%m-%dT%H:%M:%S.000Z")

    @classmethod
    def on_or_after(cls, value):
        formatted_timestamp = cls._to_timestamp_string(value)
        return FilterGroup([cls("ON_OR_AFTER", formatted_timestamp)])

    @classmethod
    def on_or_before(cls, value):
        formatted_timestamp = cls._to_timestamp_string(value)
        return FilterGroup([cls("ON_OR_BEFORE", formatted_timestamp)])

    @classmethod
    def in_range(cls, start_value, end_value):
        formatted_start_time = cls._to_timestamp_string(start_value)
        formatted_end_time = cls._to_timestamp_string(end_value)
        return FilterGroup([cls("ON_OR_AFTER", formatted_start_time), cls("ON_OR_BEFORE", formatted_end_time)])


class MD5(_FileEventFilterStringField):
    _term = "md5Checksum"


class SHA256(_FileEventFilterStringField):
    _term = "sha256Checksum"


class OSHostname(_FileEventFilterStringField):
    _term = "osHostName"


class DeviceUsername(_FileEventFilterStringField):
    _term = "deviceUserName"


class FileName(_FileEventFilterStringField):
    _term = "fileName"


class FilePath(_FileEventFilterStringField):
    _term = "filePath"


class PublicIPAddress(_FileEventFilterStringField):
    _term = "publicIpAddress"


class PrivateIPAddress(_FileEventFilterStringField):
    _term = "privateIpAddresses"


class EventTimestamp(_FileEventFilterTimestampField):
    _term = "eventTimestamp"


class EventType(_FileEventFilterStringField):
    _term = "eventType"

    class EventTypeEnum(object):
        def __init__(self, value):
            self._value = value

        def __repr__(self):
            return self._value

    CREATED = EventTypeEnum("CREATED")
    MODIFIED = EventTypeEnum("MODIFIED")
    DELETED = EventTypeEnum("DELETED")
    READ_BY_APP = EventTypeEnum("READ_BY_APP")

    @classmethod
    def eq(cls, value):
        # type: (EventTypeEnum) -> FilterGroup
        return super(EventType, cls).eq(repr(value))

    @classmethod
    def not_eq(cls, value):
        # type: (EventTypeEnum) -> FilterGroup
        return super(EventType, cls).not_eq(repr(value))

    @classmethod
    def is_in(cls, value_list):
        # type: (iter[EventTypeEnum]) -> FilterGroup
        return super(EventType, cls).is_in([repr(value) for value in value_list])

    @classmethod
    def not_in(cls, value_list):
        # type: (iter[EventTypeEnum]) -> FilterGroup
        return super(EventType, cls).not_in([repr(value) for value in value_list])


class ExposureType(_FileEventFilterStringField):
    _term = "exposure"

    class ExposureTypeEnum(object):
        def __init__(self, value):
            self._value = value

        def __repr__(self):
            return self._value

    SHARED_VIA_LINK = ExposureTypeEnum("SharedViaLink")
    SHARED_TO_DOMAIN = ExposureTypeEnum("SharedToDomain")
    APPLICATION_READ = ExposureTypeEnum("ApplicationRead")
    CLOUD_STORAGE = ExposureTypeEnum("CloudStorage")
    REMOVABLE_MEDIA = ExposureTypeEnum("RemovableMedia")
    IS_PUBLIC = ExposureTypeEnum("IsPublic")

    @classmethod
    def any(cls):
        return cls.is_in([cls.SHARED_VIA_LINK, cls.SHARED_TO_DOMAIN, cls.APPLICATION_READ, cls.CLOUD_STORAGE,
                          cls.REMOVABLE_MEDIA, cls.IS_PUBLIC])

    @classmethod
    def eq(cls, value):
        # type: (ExposureTypeEnum) -> FilterGroup
        return super(ExposureType, cls).eq(repr(value))

    @classmethod
    def not_eq(cls, value):
        # type: (ExposureTypeEnum) -> FilterGroup
        return super(ExposureType, cls).not_eq(repr(value))

    @classmethod
    def is_in(cls, value_list):
        # type: (iter[ExposureTypeEnum]) -> FilterGroup
        return super(ExposureType, cls).is_in([repr(value) for value in value_list])

    @classmethod
    def not_in(cls, value_list):
        # type: (iter[ExposureTypeEnum]) -> FilterGroup
        return super(ExposureType, cls).not_in([repr(value) for value in value_list])
