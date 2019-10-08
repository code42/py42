# -*- coding: utf-8 -*-

from py42._internal.compat import str
from py42._internal.file_event_filter import (
    _FileEventFilterStringField,
    _FileEventFilterTimestampField,
)


class MD5(_FileEventFilterStringField):
    _term = u"md5Checksum"


class SHA256(_FileEventFilterStringField):
    _term = u"sha256Checksum"


class OSHostname(_FileEventFilterStringField):
    _term = u"osHostName"


class DeviceUsername(_FileEventFilterStringField):
    _term = u"deviceUserName"


class FileName(_FileEventFilterStringField):
    _term = u"fileName"


class FilePath(_FileEventFilterStringField):
    _term = u"filePath"


class PublicIPAddress(_FileEventFilterStringField):
    _term = u"publicIpAddress"


class PrivateIPAddress(_FileEventFilterStringField):
    _term = u"privateIpAddresses"


class EventTimestamp(_FileEventFilterTimestampField):
    _term = u"eventTimestamp"


class InsertionTimestamp(_FileEventFilterTimestampField):
    _term = u"insertionTimestamp"


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


class ExposureType(_FileEventFilterStringField):
    _term = u"exposure"

    class ExposureTypeEnum(object):
        def __init__(self, value):
            self._value = value

        def __repr__(self):
            return self._value

    SHARED_VIA_LINK = ExposureTypeEnum(u"SharedViaLink")
    SHARED_TO_DOMAIN = ExposureTypeEnum(u"SharedToDomain")
    APPLICATION_READ = ExposureTypeEnum(u"ApplicationRead")
    CLOUD_STORAGE = ExposureTypeEnum(u"CloudStorage")
    REMOVABLE_MEDIA = ExposureTypeEnum(u"RemovableMedia")
    IS_PUBLIC = ExposureTypeEnum(u"IsPublic")

    @classmethod
    def eq(cls, value):
        # type: (ExposureTypeEnum) -> FilterGroup
        return super(ExposureType, cls).eq(str(value))

    @classmethod
    def not_eq(cls, value):
        # type: (ExposureTypeEnum) -> FilterGroup
        return super(ExposureType, cls).not_eq(str(value))

    @classmethod
    def is_in(cls, value_list):
        # type: (iter[ExposureTypeEnum]) -> FilterGroup
        return super(ExposureType, cls).is_in([str(value) for value in value_list])

    @classmethod
    def not_in(cls, value_list):
        # type: (iter[ExposureTypeEnum]) -> FilterGroup
        return super(ExposureType, cls).not_in([str(value) for value in value_list])


class FileEventQuery(object):
    def __init__(self, *args, **kwargs):
        # type: (iter[FilterGroup], any) -> None
        self._filter_group_list = list(args)
        self._group_clause = kwargs.get(u"group_clause", u"AND")
        self.page_number = 1
        self.page_size = 100
        self.sort_direction = u"asc"
        self.sort_key = u"eventId"

    def __str__(self):
        groups_string = ",".join(str(group_item) for group_item in self._filter_group_list)
        json = u'{{"groupClause":"{0}", "groups":[{1}], "pgNum":{2}, "pgSize":{3}, "srtDir":"{4}", "srtKey":"{5}"}}'.format(
            self._group_clause,
            groups_string,
            self.page_number,
            self.page_size,
            self.sort_direction,
            self.sort_key,
        )
        return json

    @classmethod
    def any(cls, *args):
        # type: (iter[FilterGroup]) -> FileEventQuery
        return cls(*args, group_clause=u"OR")

    @classmethod
    def all(cls, *args):
        # type: (iter[FilterGroup]) -> FileEventQuery
        return cls(*args)
