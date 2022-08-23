from py42.choices import Choices as _Choices
from py42.sdk.queries.fileevents.util import (
    FileEventFilterStringField as _FileEventFilterStringField,
)
from py42.sdk.queries.query_filter import (
    QueryFilterStringField as _QueryFilterStringField,
)


class Name(_QueryFilterStringField):
    """V2 filter class that filters events based on the destination name."""

    _term = "destination.name"


class EmailSubject(_QueryFilterStringField):
    """V2 filter class that filters events based on the email's subject (applies to email events only)."""

    _term = "destination.email.subject"


class EmailRecipients(_QueryFilterStringField):
    """V2 filter class that filters events based on the email's recipient list (applies to email events only)."""

    _term = "destination.email.recipients"


class PrivateIpAddress(_FileEventFilterStringField):
    """V2 filter class that filters events by private (LAN) IP address of the destination device."""

    _term = "destination.privateIp"


class IpAddress(_FileEventFilterStringField):
    """V2 filter class that filters events by public (WAN) IP address of the destination device."""

    _term = "destination.ip"


class UserEmail(_FileEventFilterStringField):
    """V2 filter class that filters events by the signed in user email of the destination device."""

    _term = "destination.user.email"


class TabUrls(_FileEventFilterStringField):
    """V2 filter class that filters events based on all the URLs of the browser tabs at the time the file
    contents were read by the browser (applies to ``read by browser or other app`` events only).
    """

    _term = "destination.tabs.url"


class TabTitles(_FileEventFilterStringField):
    """V2 filter class that filters events based on the name of all the browser tabs or application windows that were
    open when a browser or other app event occurred (applies to ``read by browser or other app``
    events only).
    """

    _term = "destination.tabs.title"


class Category(_FileEventFilterStringField, _Choices):
    """V2 filter class that filters events based on the category of the file event destination.

    Available options are provided as class attributes:
        - :attr:`destination.category.CLOUD_STORAGE`
        - :attr:`destination.category.DEVICE`
        - :attr:`destination.category.EMAIL`
        - :attr:`destination.category.MESSAGING`
        - :attr:`destination.category.MULTIPLE_POSSIBILITIES`
        - :attr:`destination.category.SOCIAL_MEDIA`
        - :attr:`destination.category.SOURCE_CODE_REPOSITORY`
        - :attr:`destination.category.UNCATEGORIZED`
        - :attr:`destination.category.UNKNOWN`
        - :attr:`destination.category.BUSINESS_INTELLIGENCE_TOOLS`
        - :attr:`destination.category.CIVIL_SERVICES`
        - :attr:`destination.category.CLOUD_COMPUTING`
        - :attr:`destination.category.CODING_TOOLS`
        - :attr:`destination.category.CONTRACT_MANAGEMENT`
        - :attr:`destination.category.CRM_TOOLS`
        - :attr:`destination.category.DESIGN_TOOLS`
        - :attr:`destination.category.E_COMMERCE`
        - :attr:`destination.category.FILE_CONVERSION_TOOLS`
        - :attr:`destination.category.FINANCIAL_SERVICES`
        - :attr:`destination.category.HEALTHCARE_AND_INSURANCE`
        - :attr:`destination.category.HR_TOOLS`
        - :attr:`destination.category.IMAGE_HOSTING`
        - :attr:`destination.category.IT_SERVICES`
        - :attr:`destination.category.JOB_LISTINGS`
        - :attr:`destination.category.LEARNING_PLATFORMS`
        - :attr:`destination.category.MARKETING_TOOLS`
        - :attr:`destination.category.PDF_MANAGER`
        - :attr:`destination.category.PHOTO_PRINTING`
        - :attr:`destination.category.PRODUCTIVITY_TOOLS`
        - :attr:`destination.category.PROFESSIONAL_SERVICES`
        - :attr:`destination.category.REAL_ESTATE`
        - :attr:`destination.category.SALES_TOOLS`
        - :attr:`destination.category.SEARCH_ENGINE`
        - :attr:`destination.category.SHIPPING`
        - :attr:`destination.category.SOFTWARE`
        - :attr:`destination.category.TRAVEL`
        - :attr:`destination.category.WEB_HOSTING`
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


class PrinterName(_FileEventFilterStringField):
    """V2 filter class that filters events by printer name."""

    _term = "destination.printerName"


class PrintJobName(_FileEventFilterStringField):
    """V2 filter class that filters events by print job name."""

    _term = "destination.printJobName"


class OperatingSystem(_FileEventFilterStringField):
    """V2 filter class that filters events by the operating system of the destination device."""

    _term = "destination.operatingSystem"


class PrintedFilesBackupPath(_FileEventFilterStringField):
    """V2 filter class that filters events by the printed file backup path."""

    _term = "destination.printedFilesBackupPath"


class TabTitleErrors(_FileEventFilterStringField):
    """V2 filter class that filters events based on destination tab title errors (for 'browser or other app' events)."""

    _term = "destination.tabs.titleError"


class TabUrlErrors(_FileEventFilterStringField):
    """V2 filter class that filters events based on destination tab URL Errors (for 'browser or other app' events)."""

    _term = "destination.tabs.urlError"


class RemovableMediaName(_FileEventFilterStringField):
    """V2 filter class that filters events based on the name of the removable media involved in the exposure
    (applies to ``removable media`` events only).
    """

    _term = "destination.removableMedia.name"


class RemovableMediaVendor(_FileEventFilterStringField):
    """V2 filter class that filters events based on the vendor of the removable media device involved in the
    exposure (applies to ``removable media`` events only).
    """

    _term = "destination.removableMedia.vendor"


class RemovableMediaMediaName(_FileEventFilterStringField):
    """V2 filter class that filters events based on the name of the removable media (as reported by the
    vendor/device, usually very similar to RemovableMediaName) involved in the exposure (applies to
    ``removable media`` events only).
    """

    _term = "destination.removableMedia.mediaName"


class RemovableMediaVolumeName(_FileEventFilterStringField):
    """V2 filter class that filters events based on the name of the formatted volume (as reported by the
    operating system) of the removable media device involved in the exposure (applies to
    ``removable media`` events only).
    """

    _term = "destination.removableMedia.volumeName"


class RemovableMediaPartitionID(_FileEventFilterStringField):
    """V2 filter class that filters events based on the unique identifier assigned (by the operating system)
    to the removable media involved in the exposure (applies to ``removable media`` events only).
    """

    _term = "destination.removableMedia.partitionId"


class RemovableMediaSerialNumber(_FileEventFilterStringField):
    """V2 filter class that filters events based on the serial number of the connected hardware as reported
    by the operating system (applies to ``removable media`` events only).
    """

    _term = "destination.removableMedia.serialNumber"


class RemovableMediaCapacity(_FileEventFilterStringField):
    """V2 filter class that filters events based on the capacity of the connected hardware as reported
    by the operating system (applies to ``removable media`` events only).
    """

    _term = "destination.removableMedia.capacity"


class RemovableMediaBusType(_FileEventFilterStringField):
    """V2 filter class that filters events based on the bus type of the connected hardware as reported
    by the operating system (applies to ``removable media`` events only).
    """

    _term = "destination.removableMedia.busType"
