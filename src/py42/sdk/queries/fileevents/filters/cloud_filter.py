from py42.sdk.queries.fileevents.file_event_query import FileEventFilterStringField
from py42.sdk.queries.query_filter import QueryFilterBooleanField


class Actor(FileEventFilterStringField):
    _term = u"actor"


class DirectoryID(FileEventFilterStringField):
    _term = u"directoryId"


class Shared(QueryFilterBooleanField):
    _term = u"shared"


class SharedWith(FileEventFilterStringField):
    _term = u"sharedWith"


class SharingTypeAdded(FileEventFilterStringField):
    _term = u"sharingTypeAdded"

    SHARED_VIA_LINK = u"SharedViaLink"
    IS_PUBLIC = u"IsPublic"
