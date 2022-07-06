from py42.choices import Choices as _Choices
from py42.sdk.queries.fileevents.util import (
    FileEventFilterStringField as _FileEventFilterStringField,
)
from py42.sdk.queries.fileevents.util import (
    FileEventFilterTimestampField as _FileEventFilterTimestampField,
)


class Category(_FileEventFilterStringField, _Choices):
    """V2 filter class that filters events by category of the observed file.

    Available file categories are provided as class attributes:
        - :attr:`file.Category.AUDIO`
        - :attr:`file.Category.DOCUMENT`
        - :attr:`file.Category.EXECUTABLE`
        - :attr:`file.Category.IMAGE`
        - :attr:`file.Category.PDF`
        - :attr:`file.Category.PRESENTATION`
        - :attr:`file.Category.SCRIPT`
        - :attr:`file.Category.SOURCE_CODE`
        - :attr:`file.Category.SPREADSHEET`
        - :attr:`file.Category.VIDEO`
        - :attr:`file.Category.VIRTUAL_DISK_IMAGE`
        - :attr:`file.Category.ZIP`

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

    _term = "file.category"


class Name(_FileEventFilterStringField):
    """V2 filter class that filters events by the name of the observed file."""

    _term = "file.name"


class Owner(_FileEventFilterStringField):
    """V2 filter class that filters events by the owner of the observed file."""

    _term = "file.owner"


class Directory(_FileEventFilterStringField):
    """V2 filter class that filters events by directory of the observed file."""

    _term = "file.directory"


class Size(_FileEventFilterTimestampField):
    """V2 filter class that filters events by size in bytes of the observed file.

    Size ``value`` must be bytes.
    """

    _term = "file.sizeInBytes"


class MD5(_FileEventFilterStringField):
    """V2 filter class that filters events by the MD5 hash of the observed file."""

    _term = "file.hash.md5"


class SHA256(_FileEventFilterStringField):
    """V2 filter class that filters events by SHA256 hash of the observed file."""

    _term = "file.hash.sha256"


class DirectoryId(_FileEventFilterStringField):
    """V2 filter class that filters events by the directory ID of the observed file."""

    _term = "file.directoryId"


class CloudDriveId(_FileEventFilterStringField):
    """V2 filter class that filters event by the cloud drive ID of the observed file."""

    _term = "file.cloudDriveId"


class MimeTypeByBytes(_FileEventFilterStringField):
    """V2 filter class that filters event by the mime type (by bytes) of the observed file"""

    _term = "file.mimeTypeByBytes"


class CategoryByBytes(_FileEventFilterStringField):
    """V2 filter class that filters event by the category (by bytes) of the observed file"""

    _term = "file.categoryByBytes"


class MimeTypeByExtension(_FileEventFilterStringField):
    """V2 filter class that filters event by the mime type (by extension) of the observed file"""

    _term = "file.mimeTypeByExtension"


class CategoryByExtension(_FileEventFilterStringField):
    """V2 filter class that filters event by the category (by bytes) of the observed file"""

    _term = "file.categoryByExtension"


class Created(_FileEventFilterTimestampField):
    """V2 filter class that filters events by the creation timestamp of the observed file."""

    _term = "file.created"


class Modified(_FileEventFilterTimestampField):
    """V2 filter class that filters events by the modification timestamp of the observed file."""

    _term = "file.modified"


class Id(_FileEventFilterStringField):
    """V2 filter class that filters events by the ID of the observed file."""

    _term = "file.id"


class Url(_FileEventFilterStringField):
    """V2 filter class that filters events by the URL of the observed file."""

    _term = "file.url"


class Classification(_FileEventFilterStringField):
    """V2 filter class that filters events by the classification of the observed file."""

    _term = "file.classifications"
