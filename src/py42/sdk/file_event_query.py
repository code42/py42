# -*- coding: utf-8 -*-

from py42._internal.base_classes import BaseQuery
from py42._internal.compat import str
from py42._internal.filters.query_filter import _QueryFilterStringField, _QueryFilterTimestampField, FilterGroup
from py42._internal.filters.file_event_filter import _FileEventFilterStringField


class Actor(_FileEventFilterStringField):
    _term = u"actor"


class DeviceUsername(_FileEventFilterStringField):
    _term = u"deviceUserName"


class DirectoryID(_FileEventFilterStringField):
    _term = u"directoryId"


class EmailSender(_FileEventFilterStringField):
    _term = u"emailSender"


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


class FileCategory(_QueryFilterStringField):
    _term = u"fileCategory"


class FileName(_FileEventFilterStringField):
    _term = u"fileName"


class FileOwner(_FileEventFilterStringField):
    _term = u"fileOwner"


class FilePath(_FileEventFilterStringField):
    _term = u"filePath"


class InsertionTimestamp(_QueryFilterTimestampField):
    _term = u"insertionTimestamp"


class MD5(_FileEventFilterStringField):
    _term = u"md5Checksum"


class OSHostname(_FileEventFilterStringField):
    _term = u"osHostName"


class PrivateIPAddress(_FileEventFilterStringField):
    _term = u"privateIpAddresses"


class ProcessName(_FileEventFilterStringField):
    _term = u"processName"


class ProcessOwner(_FileEventFilterStringField):
    _term = u"processOwner"


class PublicIPAddress(_FileEventFilterStringField):
    _term = u"publicIpAddress"


class RemovableMediaName(_FileEventFilterStringField):
    _term = u"removableMediaName"


class SHA256(_FileEventFilterStringField):
    _term = u"sha256Checksum"


class SharedWith(_FileEventFilterStringField):
    _term = u"sharedWith"


class Source(_FileEventFilterStringField):
    _term = u"source"


class TabURL(_FileEventFilterStringField):
    _term = u"tabUrl"


class FileEventQuery(BaseQuery):
    def __init__(self, *args, **kwargs):
        super(FileEventQuery, self).__init__(*args, **kwargs)
        self.sort_key = u"eventId"
        self.page_number = 1

    def __str__(self):
        groups_string = u",".join(str(group_item) for group_item in self._filter_group_list)
        json = u'{{"groupClause":"{0}", "groups":[{1}], "pgNum":{2}, "pgSize":{3}, "srtDir":"{4}", "srtKey":"{5}"}}'.format(
            self._group_clause,
            groups_string,
            self.page_number,
            self.page_size,
            self.sort_direction,
            self.sort_key,
        )
        return json
