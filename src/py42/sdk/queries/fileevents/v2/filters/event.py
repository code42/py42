from py42.choices import Choices as _Choices
from py42.sdk.queries.fileevents.util import (
    FileEventFilterStringField as _FileEventFilterStringField,
)
from py42.sdk.queries.fileevents.util import (
    FileEventFilterTimestampField as _FileEventFilterTimestampField,
)


class Observer(_FileEventFilterStringField, _Choices):
    """V2 filter class that filters events by event observer.

    Available event observer types are provided as class attributes:
        - :attr:`event.Observer.ENDPOINT`
        - :attr:`event.Observer.GOOGLE_DRIVE`
        - :attr:`event.Observer.ONE_DRIVE`
        - :attr:`event.Observer.BOX`
        - :attr:`event.Observer.GMAIL`
        - :attr:`event.Observer.OFFICE_365`

    Example::
        filter = Event.Observer.is_in([event.Observer.ENDPOINT, event.Observer.BOX])

    """

    _term = "event.observer"

    ENDPOINT = "Endpoint"
    GOOGLE_DRIVE = "GoogleDrive"
    ONE_DRIVE = "OneDrive"
    BOX = "Box"
    GMAIL = "Gmail"
    OFFICE_365 = "Office365"


class Inserted(_FileEventFilterTimestampField):
    """V2 filter class that filters events based on the timestamp of when the event was actually added to the
    event store (which can be after the event occurred on the device itself).

    `value` must be a POSIX timestamp. (see the :ref:`Dates <anchor_dates>` section of the Basics
    user guide for details on timestamp arguments in py42)
    """

    _term = "event.inserted"


class Action(_FileEventFilterStringField, _Choices):
    """V2 filter class that filters events based on event action."""

    _term = "event.action"

    # Exposure Type in v1
    REMOVABLE_MEDIA_CREATED = "removable-media-created"
    REMOVABLE_MEDIA_MODIFIED = "removable-media-modified"
    REMOVABLE_MEDIA_DELETED = "removable-media-deleted"
    SYNC_APP_CREATED = "sync-app-created"
    SYNC_APP_MODIFIED = "sync-app-modified"
    SYNC_APP_DELETED = "sync-app-deleted"
    FILE_SHARED = "file-shared"

    # Event Type in v1
    FILE_CREATED = "file-created"
    FILE_DELETED = "file-deleted"
    FILE_DOWNLOADED = "file-downloaded"
    FILE_EMAILED = "file-emailed"
    FILE_MODIFIED = "file-modified"
    FILE_PRINTED = "file-printed"
    APPLICATION_READ = "application-read"


class Id(_FileEventFilterStringField):
    """V2 filter class that filters events by event ID."""

    _term = "event.id"


class ShareType(_FileEventFilterStringField):
    """V2 filter class that filters events by share type."""

    _term = "event.shareType"

    PUBLIC_LINK_SHARE = "Anyone with the link"
    DOMAIN_SHARE = "Anyone in your organization"
    DIRECT_USER_SHARE = "Shared with specific people"
