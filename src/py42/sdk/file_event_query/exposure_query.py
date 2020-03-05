from py42._internal.filters.file_event_filter import _FileEventFilterStringField


class ExposureType(_FileEventFilterStringField):
    _term = u"exposure"

    SHARED_VIA_LINK = u"SharedViaLink"
    SHARED_TO_DOMAIN = u"SharedToDomain"
    APPLICATION_READ = u"ApplicationRead"
    CLOUD_STORAGE = u"CloudStorage"
    REMOVABLE_MEDIA = u"RemovableMedia"
    IS_PUBLIC = u"IsPublic"


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
