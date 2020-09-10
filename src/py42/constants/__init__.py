from py42.util import get_attribute_keys_from_class


class SortDirection(object):
    """Code42 request `sort_direction` constants for sorting returned lists in responses."""

    DESC = u"DESC"
    ASC = u"ASC"

    @staticmethod
    def choices():
        return get_attribute_keys_from_class(SortDirection)
