from py42.sdk.queries.fileevents.file_event_query import FileEventFilterStringField


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

    _term = u"exposure"

    SHARED_VIA_LINK = u"SharedViaLink"
    SHARED_TO_DOMAIN = u"SharedToDomain"
    APPLICATION_READ = u"ApplicationRead"
    CLOUD_STORAGE = u"CloudStorage"
    REMOVABLE_MEDIA = u"RemovableMedia"
    IS_PUBLIC = u"IsPublic"


class ProcessName(FileEventFilterStringField):
    """Class that filters events based on the process name involved in the exposure (applies to
    ``read by browser or other app`` events only).
    """

    _term = u"processName"


class ProcessOwner(FileEventFilterStringField):
    """Class that filters events based on the process owner that was involved in the exposure
    (applies to ``read by browser or other app`` events only).
    """

    _term = u"processOwner"


class RemovableMediaName(FileEventFilterStringField):
    """Class that filters events based on the name of the removable media involved in the exposure
    (applies to ``removable media`` events only).
    """

    _term = u"removableMediaName"


class RemovableMediaVendor(FileEventFilterStringField):
    """Class that filters events based on the vendor of the removable media device involved in the
    exposure (applies to ``removable media`` events only).
    """

    _term = u"removableMediaVendor"


class RemovableMediaMediaName(FileEventFilterStringField):
    """Class that filters events based on the name of the removable media (as reported by the
    vendor/device, usually very similar to RemovableMediaName) involved in the exposure (applies to
    ``removable media`` events only).
    """

    _term = u"removableMediaMediaName"


class RemovableMediaVolumeName(FileEventFilterStringField):
    """Class that filters events based on the name of the formatted volume (as reported by the
    operating system) of the removable media device involved in the exposure (applies to
    ``removable media`` events only).
    """

    _term = u"removableMediaVolumeName"


class RemovableMediaPartitionID(FileEventFilterStringField):
    """Class that filters events based on the unique identifier assigned (by the operating system)
    to the removable media involved in the exposure (applies to ``removable media`` events only).
    """

    _term = u"removableMediaPartitionId"


class RemovableMediaSerialNumber(FileEventFilterStringField):
    """Class that filters events based on the serial number of the connected hardware as reported
    by the operating system (applies to ``removable media`` events only).
    """

    _term = u"removableMediaSerialNumber"


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

    _term = u"syncDestination"

    ICLOUD = u"ICloud"
    BOX = u"Box"
    BOX_DRIVE = u"BoxDrive"
    GOOGLE_DRIVE = u"GoogleDrive"
    GOOGLE_BACKUP_AND_SYNC = u"GoogleBackupAndSync"
    DROPBOX = u"Dropbox"
    ONEDRIVE = u"OneDrive"


class TabURL(FileEventFilterStringField):
    """Class that filters events based on the URL of the active browser tab at the time the file
    contents were read by the browser (applies to ``read by browser or other app`` events only).
    """

    _term = u"tabUrl"


class WindowTitle(FileEventFilterStringField):
    """Class that filters events based on the name of the browser tab or application window that was
    open when a browser or other app event occurred (applies to ``read by browser or other app``
    events only).
    """

    _term = u"windowTitle"
