from py42.choices import Choices as _Choices
from py42.sdk.queries.fileevents.util import (
    FileEventFilterStringField as _FileEventFilterStringField,
)
from py42.sdk.queries.query_filter import QueryFilterBooleanField


class Actor(_FileEventFilterStringField):
    """V1 filter class that filters events by the cloud service username of the event originator
    (applies to cloud data source events only).
    """

    _term = "actor"


class DirectoryID(_FileEventFilterStringField):
    """V1 filter class that filters events by unique identifier of the cloud drive or folder where the event
    occurred (applies to cloud data source events only).
    """

    _term = "directoryId"


class Shared(QueryFilterBooleanField):
    """V1 filter class that filters events by the shared status of the file at the time the event occurred
    (applies to cloud data source events only).
    """

    _term = "shared"


class SharedWith(_FileEventFilterStringField):
    """V1 filter class that filters events by the list of users who had been granted access to the file at the
    time of the event (applies to cloud data source events only).
    """

    _term = "sharedWith"


class SharingTypeAdded(_FileEventFilterStringField, _Choices):
    """V1 filter class that filters results to include events where a file's sharing permissions were
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
