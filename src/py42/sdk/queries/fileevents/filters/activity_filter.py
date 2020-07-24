from py42.sdk.queries.query_filter import QueryFilterBooleanField


class TrustedActivity(QueryFilterBooleanField):
    """Class that filters events based on whether activity can be trusted."""

    _term = u"trusted"


class RemoteActivity(QueryFilterBooleanField):
    """Class that filters events based on whether the remote activity can be trusted."""

    _term = u"remoteActivity"
