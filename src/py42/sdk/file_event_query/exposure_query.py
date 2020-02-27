from py42._internal.filters.file_event_filter import _FileEventFilterStringField
from py42._internal.filters.query_filter import FilterGroup


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


class ProcessName(_FileEventFilterStringField):
    _term = u"processName"


class ProcessOwner(_FileEventFilterStringField):
    _term = u"processOwner"


class RemovableMediaName(_FileEventFilterStringField):
    _term = u"removableMediaName"


class SyncDestination(_FileEventFilterStringField):
    _term = u"syncDestination"


class TabURL(_FileEventFilterStringField):
    _term = u"tabUrl"


class WindowTitle(_FileEventFilterStringField):
    _term = u"windowTitle"
