from py42.choices import Choices as _Choices
from py42.sdk.queries.fileevents.util import (
    FileEventFilterStringField as _FileEventFilterStringField,
)
from py42.sdk.queries.query_filter import (
    QueryFilterStringField as _QueryFilterStringField,
)


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


class RemovableMediaCapacity(_FileEventFilterStringField):
    """V2 filter class that filters events based on the capacity of the connected hardware as reported
    by the operating system (applies to ``removable media`` events only).
    """

    _term = "source.removableMedia.capacity"


class RemovableMediaBusType(_FileEventFilterStringField):
    """V2 filter class that filters events based on the bus type of the connected hardware as reported
    by the operating system (applies to ``removable media`` events only).
    """

    _term = "source.removableMedia.busType"


class Category(_FileEventFilterStringField, _Choices):
    """
    V2 filter class that filters events based on source category.

    Available options are provided as class attributes:
        - :attr:`source.Category.BUSINESS_TOOLS`
        - :attr:`source.Category.CLOUD_STORAGE`
        - :attr:`source.Category.DEVICE`
        - :attr:`source.Category.EMAIL`
        - :attr:`source.Category.MESSAGING`
        - :attr:`source.Category.MULTIPLE_POSSIBILITIES`
        - :attr:`source.Category.SOCIAL_MEDIA`
        - :attr:`source.Category.SOURCE_CODE_REPOSITORY`
        - :attr:`source.Category.UNCATEGORIZED`
        - :attr:`source.Category.UNKNOWN`
        - :attr:`source.category.BUSINESS_INTELLIGENCE_TOOLS`
        - :attr:`source.category.CIVIL_SERVICES`
        - :attr:`source.category.CLOUD_COMPUTING`
        - :attr:`source.category.CODING_TOOLS`
        - :attr:`source.category.CONTRACT_MANAGEMENT`
        - :attr:`source.category.CRM_TOOLS`
        - :attr:`source.category.DESIGN_TOOLS`
        - :attr:`source.category.E_COMMERCE`
        - :attr:`source.category.FILE_CONVERSION_TOOLS`
        - :attr:`source.category.FINANCIAL_SERVICES`
        - :attr:`source.category.HEALTHCARE_AND_INSURANCE`
        - :attr:`source.category.HR_TOOLS`
        - :attr:`source.category.IMAGE_HOSTING`
        - :attr:`source.category.IT_SERVICES`
        - :attr:`source.category.JOB_LISTINGS`
        - :attr:`source.category.LEARNING_PLATFORMS`
        - :attr:`source.category.MARKETING_TOOLS`
        - :attr:`source.category.PDF_MANAGER`
        - :attr:`source.category.PHOTO_PRINTING`
        - :attr:`source.category.PRODUCTIVITY_TOOLS`
        - :attr:`source.category.PROFESSIONAL_SERVICES`
        - :attr:`source.category.REAL_ESTATE`
        - :attr:`source.category.SALES_TOOLS`
        - :attr:`source.category.SEARCH_ENGINE`
        - :attr:`source.category.SHIPPING`
        - :attr:`source.category.SOFTWARE`
        - :attr:`source.category.TRAVEL`
        - :attr:`source.category.WEB_HOSTING`
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
    BUSINESS_INTELLIGENCE_TOOLS = "Business Intelligence Tools"
    CIVIL_SERVICES = "Civil Services"
    CLOUD_COMPUTING = "Cloud Computing"
    CODING_TOOLS = "Coding Tools"
    CONTRACT_MANAGEMENT = "Contract Management"
    CRM_TOOLS = "CRM Tools"
    DESIGN_TOOLS = "Design Tools"
    E_COMMERCE = "E-commerce"
    FILE_CONVERSION_TOOLS = "File Conversion Tools"
    FINANCIAL_SERVICES = "Financial Services"
    HEALTHCARE_AND_INSURANCE = "Healthcare & Insurance"
    HR_TOOLS = "HR Tools"
    IMAGE_HOSTING = "Image Hosting"
    IT_SERVICES = "IT Services"
    JOB_LISTINGS = "Job Listings"
    LEARNING_PLATFORMS = "Learning Platforms"
    MARKETING_TOOLS = "Marketing Tools"
    PDF_MANAGER = "PDF Manager"
    PHOTO_PRINTING = "Photo Printing"
    PRODUCTIVITY_TOOLS = "Productivity Tools"
    PROFESSIONAL_SERVICES = "Professional Services"
    REAL_ESTATE = "Real Estate"
    SALES_TOOLS = "Sales Tools"
    SEARCH_ENGINE = "Search Engine"
    SHIPPING = "Shipping"
    SOFTWARE = "Software"
    TRAVEL = "Travel"
    WEB_HOSTING = "Web Hosting"


class Name(_FileEventFilterStringField):
    """V2 filter class that filters events based on source name."""

    _term = "source.name"


class TabTitles(_FileEventFilterStringField):
    """V2 filter class that filters events based on source tab titles (for 'browser or other app' events)."""

    _term = "source.tabs.title"


class TabUrls(_FileEventFilterStringField):
    """V2 filter class that filters events based on source tab URLs (for 'browser or other app' events)."""

    _term = "source.tabs.url"


class TabTitleErrors(_FileEventFilterStringField):
    """V2 filter class that filters events based on source tab title errors (for 'browser or other app' events)."""

    _term = "source.tabs.titleError"


class TabUrlErrors(_FileEventFilterStringField):
    """V2 filter class that filters events based on source tab URL Errors (for 'browser or other app' events)."""

    _term = "source.tabs.urlError"


class OperatingSystem(_FileEventFilterStringField):
    """V2 filter class that filters events by the operating system of the source device."""

    _term = "source.operatingSystem"


class PrivateIpAddress(_FileEventFilterStringField):
    """V2 filter class that filters events by private (LAN) IP address of the source device."""

    _term = "source.privateIp"


class IpAddress(_FileEventFilterStringField):
    """V2 filter class that filters events by public (WAN) IP address of the source device."""

    _term = "source.ip"


class Domain(_FileEventFilterStringField):
    """V2 filter class that filters events by the domain of the source device."""

    _term = "source.domain"
