from py42.choices import Choices
from py42.sdk.queries.fileevents.util import _FileEventFilterStringField
from py42.sdk.queries.query_filter import _QueryFilterStringField


class Source:
    class EmailSender(_QueryFilterStringField):
        """V2 filter class that filters events based on the email's sender (applies to email events only)."""

        _term = "source.email.sender"

    class EmailFrom(_QueryFilterStringField):
        """V2 filter class that filters events based on the display name of the email's sender, as it appears in
        the \"From:\" field in the email (applies to email events only).
        """

        _term = "source.email.from"

    class RemovableMediaName(_FileEventFilterStringField):
        """V2 filter class that filters events based on the name of the removable media involved in the exposure
        (applies to ``removable media`` events only).
        """

        _term = "source.removableMedia.name"

    class RemovableMediaVendor(_FileEventFilterStringField):
        """V2 filter class that filters events based on the vendor of the removable media device involved in the
        exposure (applies to ``removable media`` events only).
        """

        _term = "source.removableMedia.vendor"

    class RemovableMediaMediaName(_FileEventFilterStringField):
        """V2 filter class that filters events based on the name of the removable media (as reported by the
        vendor/device, usually very similar to RemovableMediaName) involved in the exposure (applies to
        ``removable media`` events only).
        """

        _term = "source.removableMedia.mediaName"

    class RemovableMediaVolumeName(_FileEventFilterStringField):
        """V2 filter class that filters events based on the name of the formatted volume (as reported by the
        operating system) of the removable media device involved in the exposure (applies to
        ``removable media`` events only).
        """

        _term = "source.removableMedia.volumeName"

    class RemovableMediaPartitionID(_FileEventFilterStringField):
        """V2 filter class that filters events based on the unique identifier assigned (by the operating system)
        to the removable media involved in the exposure (applies to ``removable media`` events only).
        """

        _term = "source.removableMedia.partitionId"

    class RemovableMediaSerialNumber(_FileEventFilterStringField):
        """V2 filter class that filters events based on the serial number of the connected hardware as reported
        by the operating system (applies to ``removable media`` events only).
        """

        _term = "source.removableMedia.serialNumber"

    class Category(_FileEventFilterStringField, Choices):
        """
        V2 filter class that filters events based on source category.

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

        _term = "source.category"

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

    class Name(_FileEventFilterStringField):
        """V2 filter class that filters events based on source name."""

        _term = "source.name"

    class TabTitles(_FileEventFilterStringField):
        """V2 filter class that filters events based on source tab titles (for 'browser or other app' events)."""

        _term = "source.tabs.title"

    class TabUrls(_FileEventFilterStringField):
        """V2 filter class that filters events based on source tab URLs (for 'browser or other app' events)."""

        _term = "source.tabs.url"

    class OperatingSystem(_FileEventFilterStringField):
        """V2 filter class that filters events by the operating system of the source device."""

        _term = "source.operatingSystem"

    class PrivateIpAddress(_FileEventFilterStringField):
        """V2 filter class that filters events by private (LAN) IP address of the source device."""

        _term = "destination.privateIp"

    class IpAddress(_FileEventFilterStringField):
        """V2 filter class that filters events by public (WAN) IP address of the source device."""

        _term = "source.ip"
