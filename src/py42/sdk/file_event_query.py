# -*- coding: utf-8 -*-

from py42._internal.base_classes import BaseQuery
from py42._internal.compat import str
from py42._internal.query_filter import (
    _QueryFilterTimestampField,
    _QueryFilterStringFieldWithExists,
    _QueryFilterStringFieldWithExistsAndContains,
    FilterGroup,
    _QueryFilterBooleanField,
)


class Actor(_QueryFilterStringFieldWithExists):
    _term = u"actor"


class DeviceUsername(_QueryFilterStringFieldWithExists):
    _term = u"deviceUserName"


class EventTimestamp(_QueryFilterTimestampField):
    _term = u"eventTimestamp"


class EventType(_QueryFilterStringFieldWithExists):
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


class ExposureType(_QueryFilterStringFieldWithExists):
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


class FileName(_QueryFilterStringFieldWithExists):
    _term = u"fileName"


class FileOwner(_QueryFilterStringFieldWithExists):
    _term = u"fileOwner"


class FilePath(_QueryFilterStringFieldWithExists):
    _term = u"filePath"


class InsertionTimestamp(_QueryFilterTimestampField):
    _term = u"insertionTimestamp"


class MD5(_QueryFilterStringFieldWithExists):
    _term = u"md5Checksum"


class OSHostname(_QueryFilterStringFieldWithExists):
    _term = u"osHostName"


class PrivateIPAddress(_QueryFilterStringFieldWithExists):
    _term = u"privateIpAddresses"


class ProcessName(_QueryFilterStringFieldWithExists):
    _term = u"processName"


class ProcessOwner(_QueryFilterStringFieldWithExists):
    _term = u"processOwner"


class PublicIPAddress(_QueryFilterStringFieldWithExists):
    _term = u"publicIpAddress"


class RemovableMediaName(_QueryFilterStringFieldWithExists):
    _term = u"removableMediaName"


class SHA256(_QueryFilterStringFieldWithExists):
    _term = u"sha256Checksum"


class Shared(_QueryFilterBooleanField):
    _term = u"shared"


class SharedWith(_QueryFilterStringFieldWithExistsAndContains):
    _term = u"sharedWith"


class Source(_QueryFilterStringFieldWithExists):
    _term = u"source"


class TabURL(_QueryFilterStringFieldWithExists):
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
