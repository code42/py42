from datetime import datetime

from py42.exceptions import Py42BadRequestError
from py42.exceptions import Py42NotFoundError
from py42.exceptions import Py42UserNotOnListError
from py42.services import BaseService
from py42.services.detectionlists import _DetectionListFilters
from py42.services.detectionlists import _PAGE_SIZE
from py42.services.detectionlists import handle_user_already_added_error
from py42.services.util import get_all_pages
from py42.util import get_attribute_keys_from_class

_DATE_FORMAT = "%Y-%m-%d"


class DepartingEmployeeFilters(_DetectionListFilters):
    """Constants available for filtering Departing Employee search results."""

    LEAVING_TODAY = u"LEAVING_TODAY"

    @staticmethod
    def choices():
        return get_attribute_keys_from_class(DepartingEmployeeFilters)


class DepartingEmployeeService(BaseService):
    """A service for interacting with Code42 Departing Employee APIs."""

    _uri_prefix = u"v2/departingemployee/{0}"

    _CREATED_AT = u"CREATED_AT"

    def __init__(self, session, user_context, user_profile_service):
        super(DepartingEmployeeService, self).__init__(session)
        self._user_context = user_context
        self._user_profile_service = user_profile_service

    def add(self, user_id, departure_date=None):
        """Adds a user to the Departing Employees list. Creates a detection list user profile if one \
            didn't already exist.
        `REST Documentation <https://ecm-east.us.code42.com/svc/swagger/index.html?urls.primaryName=v2#/>`__

        Raises a :class:`Py42BadRequestError` when a user already exists in the Departing Employee \
            detection list.

        Args:
            user_id (str or int): The Code42 userUid of the user you want to add to the departing \
                employees list.
            departure_date (str or datetime, optional): Date in yyyy-MM-dd format or instance of datetime.
                Date is treated as UTC. Defaults to None.

        Returns:
            :class:`py42.response.Py42Response`
        """
        if isinstance(departure_date, datetime):
            departure_date = departure_date.strftime(_DATE_FORMAT)
        if self._user_profile_service.create_if_not_exists(user_id):
            tenant_id = self._user_context.get_current_tenant_id()
            data = {
                u"tenantId": tenant_id,
                u"userId": user_id,
                u"departureDate": departure_date,
            }
            uri = self._uri_prefix.format(u"add")
            try:
                return self._connection.post(uri, json=data)
            except Py42BadRequestError as err:
                handle_user_already_added_error(
                    err, user_id, u"departing-employee list"
                )
                raise

    def remove(self, user_id):
        """Removes a user from the Departing Employees list.
        `REST Documentation <https://ecm-east.us.code42.com/svc/swagger/index.html?urls.primaryName=v2#/>`__

        Args:
            user_id (str or int): The Code42 userUid of the user.

        Returns:
            :class:`py42.response.Py42Response`
        """

        tenant_id = self._user_context.get_current_tenant_id()
        uri = self._uri_prefix.format(u"remove")
        data = {u"userId": user_id, u"tenantId": tenant_id}
        try:
            return self._connection.post(uri, json=data)
        except Py42NotFoundError as err:
            raise Py42UserNotOnListError(err, user_id, u"departing-employee")

    def get(self, user_id):
        """Gets departing employee data of a user.
        `REST Documentation <https://ecm-east.us.code42.com/svc/swagger/index.html?urls.primaryName=v2#/>`__

        Args:
            user_id (str or int): The Code42 userUid of the user.

        Returns:
            :class:`py42.response.Py42Response`
        """
        tenant_id = self._user_context.get_current_tenant_id()
        uri = self._uri_prefix.format(u"get")
        data = {u"userId": user_id, u"tenantId": tenant_id}
        return self._connection.post(uri, json=data)

    def get_all(
        self,
        filter_type=DepartingEmployeeFilters.OPEN,
        sort_key=_CREATED_AT,
        sort_direction=u"DESC",
        page_size=_PAGE_SIZE,
    ):
        """Gets all Departing Employees.

        Args:
            filter_type (str, optional): ``EXFILTRATION_30_DAYS``, ``EXFILTRATION_24_HOURS``,
                ``OPEN``, or ``LEAVING_TODAY``. Constants are available at
                :class:`py42.services.detectionlists.departing_employee.DepartingEmployeeFilters`.
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
            u"items",
            filter_type=filter_type,
            sort_key=sort_key,
            sort_direction=sort_direction,
            page_size=page_size or _PAGE_SIZE,
        )

    def get_page(
        self,
        page_num,
        filter_type=DepartingEmployeeFilters.OPEN,
        sort_key=_CREATED_AT,
        sort_direction=u"DESC",
        page_size=_PAGE_SIZE,
    ):
        """Gets a single page of Departing Employees.

        Args:
            page_num (int): The page number to request.
            filter_type (str, optional): ``EXFILTRATION_30_DAYS``, ``EXFILTRATION_24_HOURS``,
                ``OPEN``, or ``LEAVING_TODAY``. Constants are available at
                :class:`py42.services.detectionlists.departing_employee.DepartingEmployeeFilters`.
                Defaults to "OPEN".
            sort_key (str, optional): Sort results based by field. Defaults to "CREATED_AT".
            sort_direction (str. optional): ``ASC`` or ``DESC``. Defaults to "DESC".
            page_size (int, optional): The number of departing employees to return
                per page. Defaults to 100.

        Returns:
            :class:`py42.response.Py42Response`
        """

        uri = self._uri_prefix.format(u"search")
        data = {
            u"tenantId": self._user_context.get_current_tenant_id(),
            u"pgSize": page_size,
            u"pgNum": page_num,
            u"filterType": filter_type,
            u"srtKey": sort_key,
            u"srtDirection": sort_direction,
        }
        return self._connection.post(uri, json=data)

    def set_alerts_enabled(self, alerts_enabled=True):
        """Enable or disable email alerting on Departing Employee exposure events.
        `REST Documentation <https://ecm-east.us.code42.com/svc/swagger/index.html?urls.primaryName=v2#/>`__

        Args:
            alerts_enabled (bool): Set alerting to on (True) or off (False). Defaults to True.

        Returns:
            :class:`py42.response.Py42Response`
        """
        tenant_id = self._user_context.get_current_tenant_id()
        uri = self._uri_prefix.format(u"setalertstate")
        data = {u"tenantId": tenant_id, u"alertsEnabled": alerts_enabled}
        return self._connection.post(uri, json=data)

    def update_departure_date(self, user_id, departure_date):
        """Add or modify details of an existing Departing Employee case.
        `REST Documentation <https://ecm-east.us.code42.com/svc/swagger/index.html?urls.primaryName=v2#/>`__

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
        uri = self._uri_prefix.format(u"update")
        data = {
            u"tenantId": tenant_id,
            u"userId": user_id,
            u"departureDate": departure_date,
        }
        return self._connection.post(uri, json=data)
