from py42.sdk.queries.query_filter import filter_attributes
from py42.sdk.queries.fileevents.file_event_query import FileEventFilterStringField


class TrustedActivity(FileEventFilterStringField):
    """Class that filters events based on whether activity can be trusted.

        Available event types are provided as class attributes:
            - :attr:`FileCategory.INCLUDE`
            - :attr:`FileCategory.EXCLUDE`
    """

    _term = u"trusted"

    INCLUDE = True
    EXCLUDE = False

    @staticmethod
    def choices():
        return filter_attributes(TrustedActivity)


class RemoteActivity(FileEventFilterStringField):
    """Class that filters events based on whether the remote activity can be trusted.

        Available event types are provided as class attributes:
            - :attr:`FileCategory.INCLUDE`
            - :attr:`FileCategory.EXCLUDE`

    """

    _term = u"remoteActivity"

    INCLUDE = True
    EXCLUDE = False

    @staticmethod
    def choices():
        return filter_attributes(TrustedActivity)
