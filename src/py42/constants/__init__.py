from py42.sdk.queries.query_filter import filter_attributes


class SortDirection(object):
    """Code42 request `sort_direction` constants for sorting returned lists in responses."""

    DESC = u"DESC"
    ASC = u"ASC"

    @staticmethod
    def choices():
        return filter_attributes(SortDirection)
