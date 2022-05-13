from py42.choices import Choices as _Choices
from py42.sdk.queries.fileevents.util import (
    FileEventFilterStringField as _FileEventFilterStringField,
)


class SourceCategory(_FileEventFilterStringField, _Choices):
    """
    V1 filter class that filters events based on source category.

    Available options are provided as class attributes:
        - :attr:`SourceCategory.BUSINESS_TOOLS`
        - :attr:`SourceCategory.CLOUD_STORAGE`
        - :attr:`SourceCategory.DEVICE`
        - :attr:`SourceCategory.EMAIL`
        - :attr:`SourceCategory.MESSAGING`
        - :attr:`SourceCategory.MULTIPLE_POSSIBILITIES`
        - :attr:`SourceCategory.SOCIAL_MEDIA`
        - :attr:`SourceCategory.SOURCE_CODE_REPOSITORY`
        - :attr:`SourceCategory.UNCATEGORIZED`
        - :attr:`SourceCategory.UNKNOWN`
    """

    _term = "sourceCategory"

    BUSINESS_TOOLS = "Business Tools"
    CLOUD_STORAGE = "Cloud Storage"
    DEVICE = "Device"
    EMAIL = "Email"
    MESSAGING = "Messaging"
    MULTIPLE_POSSIBILITIES = "Multiple Possibilities"
    SOCIAL_MEDIA = "Social Media"
    SOURCE_CODE_REPOSITORY = "Source Code Repository"
    UNCATEGORIZED = "Uncategorized"
    UNKNOWN = "Unknown"


class SourceName(_FileEventFilterStringField):
    """V1 filter class that filters events based on source name."""

    _term = "sourceName"


class SourceTabTitles(_FileEventFilterStringField):
    """V1 filter class that filters events based on source tab titles (for 'browser or other app' events)."""

    _term = "sourceTabTitles"


class SourceTabUrls(_FileEventFilterStringField):
    """V1 filter class that filters events based on source tab URLs (for 'browser or other app' events)."""

    _term = "sourceTabUrls"
