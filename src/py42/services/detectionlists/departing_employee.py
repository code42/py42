from datetime import datetime

from deprecated.sphinx import deprecated

from py42.choices import Choices
from py42.exceptions import Py42BadRequestError
from py42.exceptions import Py42NotFoundError
from py42.exceptions import Py42UserNotOnListError
from py42.services import BaseService
from py42.services.detectionlists import _DetectionListFilters
from py42.services.detectionlists import _PAGE_SIZE
from py42.services.detectionlists import handle_user_already_added_error
from py42.services.util import get_all_pages
from py42.clients.watchlists import WatchlistType

_DATE_FORMAT = "%Y-%m-%d"


class DepartingEmployeeFilters(_DetectionListFilters, Choices):
    """DEPRECATED TODO
    Constants available for filtering Departing Employee search results.

    * ``OPEN``
    * ``EXFILTRATION_30_DAYS``
    * ``EXFILTRATION_24_HOURS``
    * ``LEAVING_TODAY``
    """

    LEAVING_TODAY = "LEAVING_TODAY"


class DepartingEmployeeService(BaseService):
    """DEPRECATED # TODO
    A service for interacting with Code42 Departing Employee APIs."""

    _uri_prefix = "v2/departingemployee/{0}"

    _CREATED_AT = "CREATED_AT"

    def __init__(self, session, user_context, user_profile_service, watchlist_service, user_risk_profile_service):
        super().__init__(session)
        self._user_context = user_context
        self._user_profile_service = user_profile_service
        self._watchlist_service = watchlist_service
        self._user_risk_profile_service = user_risk_profile_service

    def add(self, user_id, departure_date=None):
        """DEPRECATED # TODO
        Adds a user to the Departing Employees list.
        `REST Documentation <https://developer.code42.com/api/#operation/DepartingEmployeeControllerV2_AddEmployee>`__

        Raises a :class:`Py42UserAlreadyAddedError` when a user already exists in the Departing Employee \
            detection list.

        Args:
            user_id (str or int): The Code42 userUid of the user you want to add to the departing \
                employees list.
            departure_date (str or datetime, optional): Date in yyyy-MM-dd format or instance of datetime. \
                Date is treated as UTC. Defaults to None.

        Returns:
            :class:`py42.response.Py42Response`
        """

        # if datetime instance, convert to string.
        if isinstance(departure_date, datetime):
            departure_date = departure_date.strftime(_DATE_FORMAT)

        # add user to Departing Employees watchlist
        self._watchlist_service.add_included_users_by_watchlist_type([user_id], WatchlistType.DEPARTING_EMPLOYEE)

        # update user risk profile with departing date
        self._user_risk_profile_service.update(user_id, end_date=departure_date, paths="endDate")

    def remove(self, user_id):
        """DEPRECATED # TODO
        Removes a user from the Departing Employees list.
        `REST Documentation <https://developer.code42.com/api/#operation/DepartingEmployeeControllerV2_RemoveUser>`__

        Args:
            user_id (str or int): The Code42 userUid of the user.

        Returns:
            :class:`py42.response.Py42Response`
        """

        # remove user from Departing Employees watchlist
        return self._watchlist_service.delete_included_users_by_watchlist_type([user_id], WatchlistType.DEPARTING_EMPLOYEE)

    def get(self, user_id):
        """DEPRECATED # TODO
        Gets departing employee data of a user.
        `REST Documentation <https://developer.code42.com/api/#operation/DepartingEmployeeControllerV2_GetEmployee>`__

        Args:
            user_id (str or int): The Code42 userUid of the user.

        Returns:
            :class:`py42.response.Py42Response`
        """
        return self._user_risk_profile_service.get(user_id)

    def get_all(
        self,
        filter_type=DepartingEmployeeFilters.OPEN,
        sort_key=_CREATED_AT,
        sort_direction="DESC",
        page_size=_PAGE_SIZE,
    ):
        """DEPRECATED # TODO
        Gets all Departing Employees.

        Args:
            filter_type (str, optional): Constants available at
                :class:`py42.constants.DepartingEmployeeFilters`.
                Defaults to "OPEN".
            sort_key (str, optional): Sort results based by field. Defaults to "CREATED_AT".
            sort_direction (str, optional): ``ASC`` or ``DESC``. Defaults to "DESC".
            page_size (int, optional): The number of departing employees to return
                per page. Defaults to 100.

        Returns:
            generator: An object that iterates over :class:`py42.response.Py42Response` objects
            that each contain a page of departing employees.
        """
        return get_all_pages(
            self.get_page,
            "items",
            filter_type=filter_type,
            sort_key=sort_key,
            sort_direction=sort_direction,
            page_size=page_size or _PAGE_SIZE,
        )
        return

    def get_page(
        self,
        page_num,
        filter_type=DepartingEmployeeFilters.OPEN,
        sort_key=_CREATED_AT,
        sort_direction="DESC",
        page_size=_PAGE_SIZE,
    ):
        """DEPRECATED # TODO
        Gets a single page of Departing Employees.

        Args:
            page_num (int): The page number to request.
            filter_type (str, optional): Constants available at
                :class:`py42.constants.DepartingEmployeeFilters`.
                Defaults to "OPEN".
            sort_key (str, optional): Sort results based by field. Defaults to "CREATED_AT".
            sort_direction (str. optional): ``ASC`` or ``DESC``. Defaults to "DESC".
            page_size (int, optional): The number of departing employees to return
                per page. Defaults to 100.

        Returns:
            :class:`py42.response.Py42Response`
        """

        uri = self._uri_prefix.format("search")
        data = {
            "tenantId": self._user_context.get_current_tenant_id(),
            "pgSize": page_size,
            "pgNum": page_num,
            "filterType": filter_type,
            "srtKey": sort_key,
            "srtDirection": sort_direction,
        }
        return self._connection.post(uri, json=data)

    def set_alerts_enabled(self, alerts_enabled=True):
        """DEPRECATED # TODO
        Enable or disable email alerting on Departing Employee exposure events.
        `REST Documentation <https://developer.code42.com/api/#operation/DepartingEmployeeControllerV2_SetAlertState>`__

        Args:
            alerts_enabled (bool): Set alerting to on (True) or off (False). Defaults to True.

        Returns:
            :class:`py42.response.Py42Response`
        """
        tenant_id = self._user_context.get_current_tenant_id()
        uri = self._uri_prefix.format("setalertstate")
        data = {"tenantId": tenant_id, "alertsEnabled": alerts_enabled}
        return self._connection.post(uri, json=data)

    def update_departure_date(self, user_id, departure_date):
        """DEPRECATED # TODO
        Add or modify details of an existing Departing Employee case.
        `REST Documentation <https://developer.code42.com/api/#operation/DepartingEmployeeControllerV2_UpdateDepartureDate>`__

        Args:
            user_id (str): The Code42 userUid of the user.
            departure_date (str or datetime): Date in yyyy-MM-dd format or instance of datetime.
                Date is treated as UTC.

        Returns:
            :class:`py42.response.Py42Response`
        """

        tenant_id = self._user_context.get_current_tenant_id()
        if isinstance(departure_date, datetime):
            departure_date = departure_date.strftime(_DATE_FORMAT)
        uri = self._uri_prefix.format("update")
        data = {
            "tenantId": tenant_id,
            "userId": user_id,
            "departureDate": departure_date,
        }
        return self._connection.post(uri, json=data)
