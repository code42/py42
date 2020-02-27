from py42._internal.filters.file_event_filter import _FileEventFilterStringField
from py42._internal.filters.query_filter import _QueryFilterStringField


class FileCategory(_QueryFilterStringField):
    _term = u"fileCategory"


class FileName(_FileEventFilterStringField):
    _term = u"fileName"


class FileOwner(_FileEventFilterStringField):
    _term = u"fileOwner"


class FilePath(_FileEventFilterStringField):
    _term = u"filePath"


class MD5(_FileEventFilterStringField):
    _term = u"md5Checksum"


class SHA256(_FileEventFilterStringField):
    _term = u"sha256Checksum"
