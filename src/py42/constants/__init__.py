from pycpg.choices import Choices


class SortDirection(Choices):
    """Constants available to set CrashPlan request `sort_direction` when sorting returned lists in responses.

    * ``ASC``
    * ``DESC``
    """

    DESC = "DESC"
    ASC = "ASC"
