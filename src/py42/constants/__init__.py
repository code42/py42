from py42.choices import Choices
from py42.clients.cases import CaseStatus
from py42.clients.detectionlists import RiskTags
from py42.clients.trustedactivities import TrustedActivityType
from py42.clients.watchlists import WatchlistType
from py42.services.detectionlists.departing_employee import DepartingEmployeeFilters
from py42.services.detectionlists.high_risk_employee import HighRiskEmployeeFilters


class SortDirection(Choices):
    """Constants available to set Code42 request `sort_direction` when sorting returned lists in responses.

    * ``ASC``
    * ``DESC``
    """

    DESC = "DESC"
    ASC = "ASC"
