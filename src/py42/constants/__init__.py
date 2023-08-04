from py42.choices import Choices
from py42.clients.cases import CaseStatus
from py42.clients.trustedactivities import TrustedActivityType
from py42.clients.watchlists import WatchlistType


class SortDirection(Choices):
    """Constants available to set Code42 request `sort_direction` when sorting returned lists in responses.

    * ``ASC``
    * ``DESC``
    """

    DESC = "DESC"
    ASC = "ASC"
