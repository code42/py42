from py42.sdk.queries.fileevents.file_event_query import FileEventFilterStringField


class ExposureType(FileEventFilterStringField):
    _term = u"exposure"

    SHARED_VIA_LINK = u"SharedViaLink"
    SHARED_TO_DOMAIN = u"SharedToDomain"
    APPLICATION_READ = u"ApplicationRead"
    CLOUD_STORAGE = u"CloudStorage"
    REMOVABLE_MEDIA = u"RemovableMedia"
    IS_PUBLIC = u"IsPublic"


class ProcessName(FileEventFilterStringField):
    _term = u"processName"


class ProcessOwner(FileEventFilterStringField):
    _term = u"processOwner"


class RemovableMediaName(FileEventFilterStringField):
    _term = u"removableMediaName"


class SyncDestination(FileEventFilterStringField):
    _term = u"syncDestination"


class TabURL(FileEventFilterStringField):
    _term = u"tabUrl"


class WindowTitle(FileEventFilterStringField):
    _term = u"windowTitle"
