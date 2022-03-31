from py42.choices import Choices
from py42.sdk.queries.fileevents.file_event_query import FileEventFilterStringField
from py42.sdk.queries.query_filter import QueryFilterStringField


class Destination(QueryFilterStringField):
    """ Class that filters events based on the destination name. """

    _term = "destination.name"


class EmailSubject(QueryFilterStringField):
    """Class that filters events based on the email's subject (applies to email events only)."""

    _term = "destination.email.subject"


class EmailRecipients(QueryFilterStringField):
    """Class that filters events based on the email's recipient list (applies to email events only)."""

    _term = "destination.email.recipients"


class DestinationPrivateIPAddress(FileEventFilterStringField):
    """Class that filters events by private (LAN) IP address of the destination device."""

    _term = "destination.privateIp"


class DestinationIPAddress(FileEventFilterStringField):
    """Class that filters events by public (WAN) IP address of the destination device."""

    _term = "destination.ip"


class DestinationUserEmail(FileEventFilterStringField):
    """Class that filters events by the signed in user email of the destination device."""

    _term = "destination.user.email"


class DestinationTabUrls(FileEventFilterStringField):
    """Class that filters events based on all the URLs of the browser tabs at the time the file
    contents were read by the browser (applies to ``read by browser or other app`` events only).
    """

    _term = "destination.tabs.url"


class DestinationTabTitles(FileEventFilterStringField):
    """Class that filters events based on the name of all the browser tabs or application windows that were
    open when a browser or other app event occurred (applies to ``read by browser or other app``
    events only).
    """

    _term = "destination.tabs.title"


class DestinationCategory(FileEventFilterStringField, Choices):
    """Class that filters events based on the category of the file event destination.

    Available options are provided as class attributes:
        - :attr:`DestinationCategory.CLOUD_STORAGE`
        - :attr:`DestinationCategory.DEVICE`
        - :attr:`DestinationCategory.EMAIL`
        - :attr:`DestinationCategory.MESSAGING`
        - :attr:`DestinationCategory.MULTIPLE_POSSIBILITIES`
        - :attr:`DestinationCategory.SOCIAL_MEDIA`
        - :attr:`DestinationCategory.SOURCE_CODE_REPOSITORY`
        - :attr:`DestinationCategory.UNCATEGORIZED`
        - :attr:`DestinationCategory.UNKNOWN`
    """

    _term = "destination.category"

    CLOUD_STORAGE = "Cloud Storage"
    DEVICE = "Device"
    EMAIL = "Email"
    MESSAGING = "Messaging"
    MULTIPLE_POSSIBILITIES = "Multiple Possibilities"
    SOCIAL_MEDIA = "Social Media"
    SOURCE_CODE_REPOSITORY = "Source Code Repository"
    UNCATEGORIZED = "Uncategorized"
    UNKNOWN = "Unknown"


class Printer(FileEventFilterStringField):
    """Class that filters events by printer name."""

    _term = "destination.printerName"


class PrintJobName(FileEventFilterStringField):
    """Class that filters events by print job name."""

    _term = "destination.printJobName"


class DestinationOperatingSystem(FileEventFilterStringField):
    """Class that filters events by the operating system of the destination device."""

    _term = "destination.operatingSystem"
