from py42.sdk.queries.fileevents.file_event_query import FileEventFilterStringField
from py42.sdk.queries.query_filter import QueryFilterBooleanField


class Actor(FileEventFilterStringField):
    """Class that filters events by the cloud service username of the event originator
    (applies to cloud data source events only).
    """

    _term = u"actor"


class DirectoryID(FileEventFilterStringField):
    """Class that filters events by unique identifier of the cloud drive or folder where the event
     occurred (applies to cloud data source events only).
    """

    _term = u"directoryId"


class Shared(QueryFilterBooleanField):
    """Class that filters events by the shared status of the file at the time the event occurred
    (applies to cloud data source events only).
    """

    _term = u"shared"


class SharedWith(FileEventFilterStringField):
    """Class that filters events by the list of users who had been granted access to the file at the
    time of the event (applies to cloud data source events only).
    """

    _term = u"sharedWith"


class SharingTypeAdded(FileEventFilterStringField):
    """Class that filters results to include events where a file's sharing permissions were
    increased to increase exposure (applies to cloud data source events only).

    Available options are:
        - :class:`SharingTypeAdded.SHARED_VIA_LINK`
        - :class:`SharingTypeAdded.IS_PUBLIC`
        - :class:`SharingTypeAdded.OUTSIDE_TRUSTED_DOMAIN`
    """

    _term = u"sharingTypeAdded"

    SHARED_VIA_LINK = u"SharedViaLink"
    IS_PUBLIC = u"IsPublic"
    OUTSIDE_TRUSTED_DOMAIN = u"OutsideTrustedDomains"
