from py42._internal.filters.file_event_filter import _FileEventFilterStringField


class DirectoryID(_FileEventFilterStringField):
    _term = u"directoryId"


class Actor(_FileEventFilterStringField):
    _term = u"actor"


class SharedWith(_FileEventFilterStringField):
    _term = u"sharedWith"
