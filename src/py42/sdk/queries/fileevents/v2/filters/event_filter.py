from py42.choices import Choices
from py42.sdk.queries.fileevents.file_event_query import FileEventFilterStringField
from py42.sdk.queries.fileevents.file_event_query import FileEventFilterTimestampField


class EventObserver(FileEventFilterStringField, Choices):
    """V2 filter class that filters events by event observer.

    Available event observer types are provided as class attributes:
        - :attr:`EventObserver.ENDPOINT`
        - :attr:`EventObserver.GOOGLE_DRIVE`
        - :attr:`EventObserver.ONE_DRIVE`
        - :attr:`EventObserver.BOX`
        - :attr:`EventObserver.GMAIL`
        - :attr:`EventObserver.OFFICE_365`

    Example::

        filter = EventObserver.is_in([EventObserver.ENDPOINT, EventObserver.BOX])

    """

    _term = "event.observer"

    ENDPOINT = "Endpoint"
    GOOGLE_DRIVE = "GoogleDrive"
    ONE_DRIVE = "OneDrive"
    BOX = "Box"
    GMAIL = "Gmail"
    OFFICE_365 = "Office365"


class EventInserted(FileEventFilterTimestampField):
    """V2 filter class that filters events based on the timestamp of when the event was actually added to the
    event store (which can be after the event occurred on the device itself).

    `value` must be a POSIX timestamp. (see the :ref:`Dates <anchor_dates>` section of the Basics
    user guide for details on timestamp arguments in py42)
    """

    _term = "event.inserted"


class EventAction(FileEventFilterStringField, Choices):
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


class EventId(FileEventFilterStringField):
    """V2 filter class that filters events by event ID."""

    _term = "event.id"


class EventShareType(FileEventFilterStringField):
    """V2 filter class that filters events by share type."""

    _term = "event.shareType"

    PUBLIC_LINK_SHARE = "Anyone with the link"
    DOMAIN_SHARE = "Anyone in your organization"
    DIRECT_USER_SHARE = "Shared with specific people"
