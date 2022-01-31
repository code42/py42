from py42.sdk.queries.fileevents.file_event_query import FileEventFilterStringField


class SourceCategory(FileEventFilterStringField):
    """Class that filters events by the source category."""

    _term = "sourceCategory"


class SourceName(FileEventFilterStringField):
    """Class that filters events by the source name."""

    _term = "sourceName"


class SourceTabTitles(FileEventFilterStringField):
    """Class that filters events by the source tab titles."""

    _term = "sourceTabTitles"


class SourceTabUrls(FileEventFilterStringField):
    """Class that filters events by the source tab URLs."""

    _term = "sourceTabUrls"
