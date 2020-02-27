from py42._internal.filters.query_filter import _QueryFilterBooleanField
from py42._internal.filters.file_event_filter import _FileEventFilterStringField


class Actor(_FileEventFilterStringField):
    _term = u"actor"


class DirectoryID(_FileEventFilterStringField):
    _term = u"directoryId"


class Shared(_QueryFilterBooleanField):
    _term = u"shared"


class SharedWith(_FileEventFilterStringField):
    _term = u"sharedWith"


class SharingTypeAdded(_FileEventFilterStringField):
    _term = u"sharingTypeAdded"

    class SharingTypeAddedEnum(object):
        def __init__(self, value):
            self._value = value

        def __repr__(self):
            return self._value

    SHARED_VIA_LINK = SharingTypeAddedEnum(u"SharedViaLink")
    IS_PUBLIC = SharingTypeAddedEnum(u"IsPublic")
