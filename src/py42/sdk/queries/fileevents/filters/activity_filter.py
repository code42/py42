from py42.sdk.queries.query_filter import (
    QueryFilterBooleanField as _QueryFilterBooleanField,
)


class TrustedActivity(_QueryFilterBooleanField):
    """V1 filter class that filters events based on whether activity can be trusted."""

    _term = "trusted"


class RemoteActivity(_QueryFilterBooleanField):
    """V1 filter class that filters events based on whether the activity was remote
    (took place outside of corporate IP range)."""

    _term = "remoteActivity"
