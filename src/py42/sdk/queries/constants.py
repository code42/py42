from py42.exceptions import Py42Error


class CustomConstant(object):
    def choices(self):
        return [
            attr
            for attr in dir(self)
            if not callable(self.__getattribute__(attr)) and not attr.startswith(u"_")
        ]

    def __setattr__(self, key, value):
        raise Py42Error("{0} is a constant, cannot be modified.".format(key))


class EventObservedIn(CustomConstant):
    _term = u""

    FIFTEEN_MINUTE = u"PT15M"
    ONE_HOUR = u"PT1H"
    THREE_HOUR = u"PT3H"
    TWELVE_HOUR = u"PT12H"
    ONE_DAY = u"P1D"
    THREE_DAY = u"P3D"
    SEVEN_DAY = u"P7D"
    FOURTEEN_DAY = u"P14D"
    THIRTY_DAY = u"P30D"


class Event(CustomConstant):
    _term = u""

    NEW_FILE = u"CREATED"
    NO_LONGER_OBSERVED = u"DELETED"
    EMAILED = u"EMAILED"
    MODIFIED = u"UPDATED"
    PRINTED = u"PRINTED"
    BROWSER_OR_APP_READ = "READ_BY_APP"


class Source(CustomConstant):
    _term = u""

    ENDPOINT = u"Endpoint"
    GOOGLE_DRIVE = u"GoogleDrive"
    ONE_DRIVE = u"OneDrive"
    BOX = u"Box"
    GMAIL = u"Gmail"
    OFFICE_365 = u"Office365"


class RiskIndicatorMimeType(CustomConstant):
    _term = u"mimeTypeMismatch"

    FILE_MISMATCH = True  # Verify expected  u"true"


class RiskIndicatorActiveHours(CustomConstant):
    _term = u"outsideActiveHours"

    OUTSIDE_ACTIVE_HOURS = True  # Verify expected u"true"


class ProcessUser(CustomConstant):
    _term = u"ProcessOwner"


class TrustedActivity(CustomConstant):
    _term = u"trusted"

    INCLUDE = True
    EXCLUDE = False


class Printer(CustomConstant):
    _term = u"printerName"


class PrintJobName(CustomConstant):
    _term = u"printJobName"


class FileName(CustomConstant):
    _term = u"fileName"


class FilePath(CustomConstant):
    _term = u"filePath"


class FileSize(CustomConstant):
    _term = u"fileSize"


class FileCategory(CustomConstant):
    _term = u"fileCategory"

    AUDIO = u"AUDIO"
    DOCUMENT = u"DOCUMENT"
    EXECUTABLE = u"EXECUTABLE"
    IMAGE = u"IMAGE"
    PDF = u"PDF"
    PRESENTATION = u"PRESENTATION"
    SCRIPT = u"SCRIPT"
    SOURCE_CODE = u"SOURCE_CODE"
    SPREADSHEET = u"SPREADSHEET"
    VIDEO = u"VIDEO"
    VIRTUAL_DISK_IMAGE = u"VIRTUAL_DISK_IMAGE"
    ZIP = u"ARCHIVE"


class FileOwner(CustomConstant):
    _term = u"fileOwner"


class MD5Checksum(CustomConstant):
    _term = u"md5Checksum"


class SHA256Checksum(CustomConstant):
    _term = u"sha256Checksum"


class DeviceHostName(CustomConstant):
    _term = u"osHostName"


class DeviceUserName(CustomConstant):
    _term = u"deviceUserName"


class DeviceSignedInUserName(CustomConstant):
    _term = u"operatingSystemUser"


class DevicePublicIPAddress(CustomConstant):
    _term = u"publicIpAddress"


class DevicePrivateIpAddress(CustomConstant):
    _term = u"privateIpAddress"


class RemoteActivity(CustomConstant):
    _term = u"remoteActivity"

    INCLUDE = True
    EXCLUDE = False


class CloudDirectory(CustomConstant):
    _term = u"directoryId"


class CloudActor(CustomConstant):
    _term = u"actor"


class CloudSharedWith(CustomConstant):
    _term = u"sharedWith"


class CloudShared(CustomConstant):
    _term = u"shared"


class CloudFileExposure(CustomConstant):
    _term = u"sharingTypeAdded"

    PUBLIC_VIA_DIRECT_LINK = u"SharedViaLink"
    OUTSIDE_TRUSTED_DOMAIN = u"OutsideTrustedDomains"
    PUBLIC_ON_THE_WEB = u"IsPublic"


class ExposureType(CustomConstant):
    _term = u"exposure"

    PUBLIC_VIA_DIRECT_LINK = u"IsPublic"
    OUTSIDE_TRUSTED_DOMAIN = u"SharedViaLink"
    PUBLIC_ON_THE_WEB = u"IsPublic"
    SHARED_WITH_CORPORATE_DOMAIN = u"OutsideTrustedDomains"
    ACTIVITY_ON_REMOVABLE_MEDIA = u"RemovableMedia"
    READ_BY_BROWSER_OR_OTHER_APP = u"ApplicationRead"
    SYNCED_TO_CLOUD_SERVICE = u"CloudStorage"


class DeviceVendor(CustomConstant):
    _term = u"removableMediaVendor"


class DeviceName(CustomConstant):
    _term = u"removableMediaName"


class DeviceMediaName(CustomConstant):
    _term = u"removableMediaMediaName"


class DeviceVolumeName(CustomConstant):
    _term = u"removableMediaVolumneName"


class DevicePartitionId(CustomConstant):
    _term = u"partitionId"


class DeviceSerialNumber(CustomConstant):
    _term = u"removableMediaSerialNumber"


class ExecutableName(CustomConstant):
    _term = u"processName"


class TabWindowTitle(CustomConstant):
    _term = u"windowTitle"


class TabURL(CustomConstant):
    _term = u"tabUrl"


class DeviceSyncDestination(CustomConstant):
    _term = u"syncDestination"

    APPLE_ICLOUD = u"ICloud"
    BOX = u"Box"
    BOD_DRIVE = u"BoxDrive"
    DROPBOX = u"Dropbox"
    GOOGLE_BACKUP_AND_SYNC = u"GoogleBackupAndSync"
    GOOGLE_DRIVE = u"GoogleDrive"
    OneDrive = u"OneDrive"


class FileSizeUnits(CustomConstant):
    _term = u"unit"
    # Event though the unit is passed the value is always passed in bytes.
    BYTES = u"b"
    KB = u"kb"
    MB = u"mb"
    GB = u"gb"
