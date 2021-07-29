from py42.util import get_attribute_keys_from_class


class SortDirection:
    """Code42 request `sort_direction` constants for sorting returned lists in responses."""

    DESC = "DESC"
    ASC = "ASC"

    @staticmethod
    def choices():
        return get_attribute_keys_from_class(SortDirection)
