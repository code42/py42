from py42.sdk.queries.fileevents.file_event_query import FileEventFilterStringField
from py42.util import get_attribute_keys_from_class


class ExposureType(FileEventFilterStringField):
    """Class that filters events based on exposure type.

    Available options are provided as class attributes:
        - :attr:`ExposureType.SHARED_VIA_LINK`
        - :attr:`ExposureType.SHARED_TO_DOMAIN`
        - :attr:`ExposureType.APPLICATION_READ`
        - :attr:`ExposureType.CLOUD_STORAGE`
        - :attr:`ExposureType.REMOVABLE_MEDIA`
        - :attr:`ExposureType.IS_PUBLIC`
    """

    _term = "exposure"

    SHARED_VIA_LINK = "SharedViaLink"
    SHARED_TO_DOMAIN = "SharedToDomain"
    APPLICATION_READ = "ApplicationRead"
    CLOUD_STORAGE = "CloudStorage"
    REMOVABLE_MEDIA = "RemovableMedia"
    IS_PUBLIC = "IsPublic"
    OUTSIDE_TRUSTED_DOMAINS = "OutsideTrustedDomains"

    @staticmethod
    def choices():
        return get_attribute_keys_from_class(ExposureType)


class ProcessName(FileEventFilterStringField):
    """Class that filters events based on the process name involved in the exposure (applies to
    ``read by browser or other app`` events only).
    """

    _term = "processName"


class ProcessOwner(FileEventFilterStringField):
    """Class that filters events based on the process owner that was involved in the exposure
    (applies to ``read by browser or other app`` events only).
    """

    _term = "processOwner"


class RemovableMediaName(FileEventFilterStringField):
    """Class that filters events based on the name of the removable media involved in the exposure
    (applies to ``removable media`` events only).
    """

    _term = "removableMediaName"


class RemovableMediaVendor(FileEventFilterStringField):
    """Class that filters events based on the vendor of the removable media device involved in the
    exposure (applies to ``removable media`` events only).
    """

    _term = "removableMediaVendor"


class RemovableMediaMediaName(FileEventFilterStringField):
    """Class that filters events based on the name of the removable media (as reported by the
    vendor/device, usually very similar to RemovableMediaName) involved in the exposure (applies to
    ``removable media`` events only).
    """

    _term = "removableMediaMediaName"


class RemovableMediaVolumeName(FileEventFilterStringField):
    """Class that filters events based on the name of the formatted volume (as reported by the
    operating system) of the removable media device involved in the exposure (applies to
    ``removable media`` events only).
    """

    _term = "removableMediaVolumeName"


class RemovableMediaPartitionID(FileEventFilterStringField):
    """Class that filters events based on the unique identifier assigned (by the operating system)
    to the removable media involved in the exposure (applies to ``removable media`` events only).
    """

    _term = "removableMediaPartitionId"


class RemovableMediaSerialNumber(FileEventFilterStringField):
    """Class that filters events based on the serial number of the connected hardware as reported
    by the operating system (applies to ``removable media`` events only).
    """

    _term = "removableMediaSerialNumber"


class SyncDestination(FileEventFilterStringField):
    """Class that filters events based on the name of the cloud service the file is synced with
    (applies to ``synced to cloud service`` events only).

    Available options are provided as class attributes:
        - :attr:`SyncDestination.ICLOUD`
        - :attr:`SyncDestination.BOX`
        - :attr:`SyncDestination.BOX_DRIVE`
        - :attr:`SyncDestination.GOOGLE_DRIVE`
        - :attr:`SyncDestination.GOOGLE_BACKUP_AND_SYNC`
        - :attr:`SyncDestination.DROPBOX`
        - :attr:`SyncDestination.ONEDRIVE`
    """

    _term = "syncDestination"

    ICLOUD = "ICloud"
    BOX = "Box"
    BOX_DRIVE = "BoxDrive"
    GOOGLE_DRIVE = "GoogleDrive"
    GOOGLE_BACKUP_AND_SYNC = "GoogleBackupAndSync"
    DROPBOX = "Dropbox"
    ONEDRIVE = "OneDrive"

    @staticmethod
    def choices():
        return get_attribute_keys_from_class(SyncDestination)


class SyncDestinationUsername(FileEventFilterStringField):
    """Class that filters events based on the username associated with the cloud service
    the file is synced with (applies to ``synced to cloud service`` events only).
    """

    _term = "syncDestinationUsername"


class TabURL(FileEventFilterStringField):
    """Class that filters events based on all the URLs of the browser tabs at the time the file
    contents were read by the browser (applies to ``read by browser or other app`` events only).
    """

    _term = "tabUrls"


class WindowTitle(FileEventFilterStringField):
    """Class that filters events based on the name of all the browser tabs or application windows that were
    open when a browser or other app event occurred (applies to ``read by browser or other app``
    events only).
    """

    _term = "tabTitles"
