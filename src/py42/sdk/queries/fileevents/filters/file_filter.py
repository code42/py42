from py42.sdk.queries.fileevents.file_event_query import (
    FileEventFilterComparableField,
    FileEventFilterStringField,
)
from py42.sdk.queries.query_filter import QueryFilterStringField


class FileCategory(QueryFilterStringField):
    """Class that filters events by category of the file observed."""

    _term = u"fileCategory"


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
