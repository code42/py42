from py42.sdk.queries.fileevents.file_event_query import FileEventFilterStringField
from py42.sdk.queries.query_filter import QueryFilterBooleanField
from py42.util import get_attribute_keys_from_class


class Actor(FileEventFilterStringField):
    """Class that filters events by the cloud service username of the event originator
    (applies to cloud data source events only).
    """

    _term = "actor"


class DirectoryID(FileEventFilterStringField):
    """Class that filters events by unique identifier of the cloud drive or folder where the event
     occurred (applies to cloud data source events only).
    """

    _term = "directoryId"


class Shared(QueryFilterBooleanField):
    """Class that filters events by the shared status of the file at the time the event occurred
    (applies to cloud data source events only).
    """

    _term = "shared"


class SharedWith(FileEventFilterStringField):
    """Class that filters events by the list of users who had been granted access to the file at the
    time of the event (applies to cloud data source events only).
    """

    _term = "sharedWith"


class SharingTypeAdded(FileEventFilterStringField):
    """Class that filters results to include events where a file's sharing permissions were
    changed to a value that increases exposure (applies to cloud data source events only).

    Available options provided as class attributes:
        - :attr:`SharingTypeAdded.SHARED_VIA_LINK`
        - :attr:`SharingTypeAdded.IS_PUBLIC`
        - :attr:`SharingTypeAdded.OUTSIDE_TRUSTED_DOMAIN`
    """

    _term = "sharingTypeAdded"

    SHARED_VIA_LINK = "SharedViaLink"
    IS_PUBLIC = "IsPublic"
    OUTSIDE_TRUSTED_DOMAIN = "OutsideTrustedDomains"

    @staticmethod
    def choices():
        return get_attribute_keys_from_class(SharingTypeAdded)
