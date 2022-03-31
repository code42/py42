from py42.choices import Choices
from py42.sdk.queries.fileevents.file_event_query import FileEventFilterStringField
from py42.sdk.queries.fileevents.file_event_query import FileEventFilterTimestampField


class EventObserver(FileEventFilterStringField, Choices):
    """Class that filters events by event source.

    Available observer types are provided as class attributes:
        - :attr:`Observer.ENDPOINT`
        - :attr:`Observer.GOOGLE_DRIVE`
        - :attr:`Observer.ONE_DRIVE`
        - :attr:`Observer.BOX`
        - :attr:`Observer.GMAIL`
        - :attr:`Observer.OFFICE_365`

    Example::

        filter = Observer.is_in([Observer.ENDPOINT, Observer.BOX])

    """

    _term = "event.observer"

    ENDPOINT = "Endpoint"
    GOOGLE_DRIVE = "GoogleDrive"
    ONE_DRIVE = "OneDrive"
    BOX = "Box"
    GMAIL = "Gmail"
    OFFICE_365 = "Office365"


class EventInserted(FileEventFilterTimestampField):
    """Class that filters events based on the timestamp of when the event was actually added to the
    event store (which can be after the event occurred on the device itself).

    `value` must be a POSIX timestamp. (see the :ref:`Dates <anchor_dates>` section of the Basics
    user guide for details on timestamp arguments in py42)
    """

    _term = "event.inserted"


class EventAction(FileEventFilterStringField, Choices):
    """Class that filters events based on event action.

    """

    _term = "event.action"

    # Exposure Type in v1
    REMOVABLE_MEDIA_CREATED = "removable-media-created"
    REMOVABLE_MEDIA_MODIFIED = "removable-media-modified"
    REMOVABLE_MEDIA_DELETED = "removable-media-deleted"
    SYNC_APP_CREATED = "sync-app-created"
    SYNC_APP_MODIFIED = "sync-app-modified"
    SYNC_APP_DELETED = "sync-app-deleted"
    FILE_SHARED_LINK = "file-shared-link"
    FILE_SHARED_DOMAIN = "file-shared-domain"
    FILE_SHARED_DIRECT = "file-shared-direct"

    # Event Type in v1
    FILE_CREATED = "file-created"
    FILE_DELETED = "file-deleted"
    FILE_DOWNLOADED = "file-downloaded"
    FILE_EMAILED = "file-emailed"
    FILE_MODIFIED = "file-modified"
    FILE_PRINTED = "file-printed"
    APPLICATION_READ = "application-read"
