from py42.choices import Choices as _Choices
from py42.sdk.queries.fileevents.util import (
    FileEventFilterComparableField as _FileEventFilterComparableField,
)
from py42.sdk.queries.fileevents.util import (
    FileEventFilterStringField as _FileEventFilterStringField,
)


class FileCategory(_FileEventFilterStringField, _Choices):
    """V1 filter class that filters events by category of the file observed.

    Available file categories are provided as class attributes:
        - :attr:`FileCategory.AUDIO`
        - :attr:`FileCategory.DOCUMENT`
        - :attr:`FileCategory.EXECUTABLE`
        - :attr:`FileCategory.IMAGE`
        - :attr:`FileCategory.PDF`
        - :attr:`FileCategory.PRESENTATION`
        - :attr:`FileCategory.SCRIPT`
        - :attr:`FileCategory.SOURCE_CODE`
        - :attr:`FileCategory.SPREADSHEET`
        - :attr:`FileCategory.VIDEO`
        - :attr:`FileCategory.VIRTUAL_DISK_IMAGE`
        - :attr:`FileCategory.ZIP`

    """

    _term = "fileCategory"

    AUDIO = "Audio"
    DOCUMENT = "Document"
    EXECUTABLE = "Executable"
    IMAGE = "Image"
    PDF = "Pdf"
    PRESENTATION = "Presentation"
    SCRIPT = "Script"
    SOURCE_CODE = "SourceCode"
    SPREADSHEET = "Spreadsheet"
    VIDEO = "Video"
    VIRTUAL_DISK_IMAGE = "VirtualDiskImage"
    ZIP = "Archive"


class FileName(_FileEventFilterStringField):
    """V1 filter class that filters events by the name of the file observed."""

    _term = "fileName"


class FileOwner(_FileEventFilterStringField):
    """V1 filter class that filters events by the owner of the file observed."""

    _term = "fileOwner"


class FilePath(_FileEventFilterStringField):
    """V1 filter class that filters events by path of the file observed."""

    _term = "filePath"


class FileSize(_FileEventFilterComparableField):
    """V1 filter class that filters events by size of the file observed.

    Size ``value`` must be bytes.
    """

    _term = "fileSize"


class MD5(_FileEventFilterStringField):
    """V1 filter class that filters events by the MD5 hash of the file observed."""

    _term = "md5Checksum"


class SHA256(_FileEventFilterStringField):
    """V1 filter class that filters events by SHA256 hash of the file observed."""

    _term = "sha256Checksum"
