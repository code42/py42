from py42.sdk.queries.query_filter import QueryFilterBooleanField


class TrustedActivity(QueryFilterBooleanField):
    """Class that filters events based on whether activity can be trusted."""

    _term = u"trusted"


class RemoteActivity(QueryFilterBooleanField):
    """Class that filters events based on whether the activity was remote
    (took place outside of corporate IP range)."""

    _term = u"remoteActivity"
