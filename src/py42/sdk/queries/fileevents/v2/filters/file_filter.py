from py42.choices import Choices
from py42.sdk.queries.fileevents.file_event_query import FileEventFilterComparableField
from py42.sdk.queries.fileevents.file_event_query import FileEventFilterStringField


class FileCategory(FileEventFilterStringField, Choices):
    """Class that filters events by category of the file observed.

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


class FileName(FileEventFilterStringField):
    """Class that filters events by the name of the file observed."""

    _term = "file.name"


class FileOwner(FileEventFilterStringField):
    """Class that filters events by the owner of the file observed."""

    _term = "file.owner"


class FilePath(FileEventFilterStringField):
    """Class that filters events by path of the file observed."""

    _term = "file.directory"


class FileSize(FileEventFilterComparableField):
    """Class that filters events by size of the file observed.

    Size ``value`` must be bytes.
    """

    _term = "file.sizeInBytes"


class MD5(FileEventFilterStringField):
    """Class that filters events by the MD5 hash of the file observed."""

    _term = "file.hash.md5"


class SHA256(FileEventFilterStringField):
    """Class that filters events by SHA256 hash of the file observed."""

    _term = "file.hash.sha256"


class DirectoryId(FileEventFilterStringField):
    """Class that filters events by the directory ID of the file observed."""

    _term = "file.directoryId"
