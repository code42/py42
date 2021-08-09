from py42.choices import Choices


class SortDirection(Choices):
    """Code42 request `sort_direction` constants for sorting returned lists in responses."""

    DESC = "DESC"
    ASC = "ASC"
