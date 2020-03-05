from py42._internal.filters.file_event_filter import _FileEventFilterStringField
from py42._internal.filters.query_filter import _QueryFilterBooleanField


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

    SHARED_VIA_LINK = u"SharedViaLink"
    IS_PUBLIC = u"IsPublic"
