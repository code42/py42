from py42.sdk.queries.fileevents.file_event_query import FileEventFilterComparableField
from py42.sdk.queries.fileevents.file_event_query import FileEventFilterStringField
from py42.util import get_attribute_keys_from_class


class FileCategory(FileEventFilterStringField):
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

    @staticmethod
    def choices():
        return get_attribute_keys_from_class(FileCategory)


class FileName(FileEventFilterStringField):
    """Class that filters events by the name of the file observed."""

    _term = u"fileName"


class FileOwner(FileEventFilterStringField):
    """Class that filters events by the owner of the file observed."""

    _term = u"fileOwner"


class FilePath(FileEventFilterStringField):
    """Class that filters events by path of the file observed."""

    _term = u"filePath"


class FileSize(FileEventFilterComparableField):
    """Class that filters events by size of the file observed.

    Size ``value`` must be bytes.
    """

    _term = u"fileSize"


class MD5(FileEventFilterStringField):
    """Class that filters events by the MD5 hash of the file observed."""

    _term = u"md5Checksum"


class SHA256(FileEventFilterStringField):
    """Class that filters events by SHA256 hash of the file observed."""

    _term = u"sha256Checksum"
