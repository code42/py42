from py42.sdk.queries.fileevents.file_event_query import FileEventFilterStringField
from py42.sdk.queries.query_filter import QueryFilterStringField


class FileCategory(QueryFilterStringField):
    _term = u"fileCategory"


class FileName(FileEventFilterStringField):
    _term = u"fileName"


class FileOwner(FileEventFilterStringField):
    _term = u"fileOwner"


class FilePath(FileEventFilterStringField):
    _term = u"filePath"


class MD5(FileEventFilterStringField):
    _term = u"md5Checksum"


class SHA256(FileEventFilterStringField):
    _term = u"sha256Checksum"
