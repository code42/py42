from py42.exceptions import Py42BadRequestError
from py42.exceptions import Py42NotFoundError
from py42.exceptions import Py42UserNotOnListError
from py42.services import BaseService
from py42.services.detectionlists import _DetectionListFilters
from py42.services.detectionlists import _PAGE_SIZE
from py42.services.detectionlists import handle_user_already_added_error
from py42.services.util import get_all_pages
from py42.util import get_attribute_keys_from_class


class HighRiskEmployeeFilters(_DetectionListFilters):
    """Constants available for filtering High Risk Employee search results."""

    @staticmethod
    def choices():
        return get_attribute_keys_from_class(HighRiskEmployeeFilters)


class HighRiskEmployeeService(BaseService):
    """A service for interacting with High Risk Employee APIs."""

    _resource = u"v2/highriskemployee"

    def __init__(self, connection, user_context, user_profile_service):
        super(HighRiskEmployeeService, self).__init__(connection)
        self._user_context = user_context
        self._user_profile_service = user_profile_service

    def _make_uri(self, action):
        return u"{}{}".format(self._resource, action)

    def _add_high_risk_employee(self, tenant_id, user_id):
        data = {u"tenantId": tenant_id, u"userId": user_id}
        uri = self._make_uri(u"/add")
        return self._connection.post(uri, json=data)

    def add(self, user_id):
        """Adds a user to the High Risk Employee detection list. Creates a detection list user
        profile if one didn't already exist.

        Raises a :class:`Py42BadRequestError` when a user already exists in the High Risk Employee
        detection list.

        Args:
            user_id (str or int): The Code42 userUid of the user you want to add to the High Risk
                Employee detection list.

        Returns:
            :class:`py42.response.Py42Response`
        """
        if self._user_profile_service.create_if_not_exists(user_id):
            tenant_id = self._user_context.get_current_tenant_id()
            try:
                return self._add_high_risk_employee(tenant_id, user_id)
            except Py42BadRequestError as err:
                handle_user_already_added_error(
                    err, user_id, u"high-risk-employee list"
                )
                raise

    def set_alerts_enabled(self, enabled=True):
        """Enables alerts.

        Args:
            enabled (bool): Whether to enable alerts for all users.

        Returns:
            :class:`py42.response.Py42Response`
        """
        data = {
            u"tenantId": self._user_context.get_current_tenant_id(),
            u"alertsEnabled": enabled,
        }
        uri = self._make_uri(u"/setalertstate")
        return self._connection.post(uri, json=data)

    def remove(self, user_id):
        """Removes a user from the High Risk Employee detection list.

        Args:
            user_id (str or int): The Code42 userUid of the user you want to add to the High Risk
                Employee detection list.

        Returns:
            :class:`py42.response.Py42Response`
        """
        data = {
            u"tenantId": self._user_context.get_current_tenant_id(),
            u"userId": user_id,
        }
        uri = self._make_uri(u"/remove")
        try:
            return self._connection.post(uri, json=data)
        except Py42NotFoundError as err:
            raise Py42UserNotOnListError(err, user_id, u"high-risk-employee")

    def get(self, user_id):
        """Gets user information.

        Args:
            user_id (str or int): The Code42 userUid of the user has been added to the High Risk
                Employee detection list.

        Returns:
            :class:`py42.response.Py42Response`
        """
        data = {
            u"tenantId": self._user_context.get_current_tenant_id(),
            u"userId": user_id,
        }
        uri = self._make_uri(u"/get")
        return self._connection.post(uri, json=data)

    def get_all(
        self,
        filter_type=HighRiskEmployeeFilters.OPEN,
        sort_key=None,
        sort_direction=None,
        page_size=_PAGE_SIZE,
    ):
        """Searches High Risk Employee list. Filter results by filter_type.

        Args:
            filter_type (str, optional): ``EXFILTRATION_30_DAYS``, ``EXFILTRATION_24_HOURS``,
                or ``OPEN``. Constants are available at
                :class:`py42.services.detectionlists.high_risk_employee.HighRiskEmployeeFilters`.
                Defaults to "OPEN".
            sort_key (str, optional): Sort results based by field. Defaults to None.
            sort_direction (str, optional): ``ASC`` or ``DESC``. Constants available at
                :class:`py42.constants.SortDirection`. Defaults to None.
            page_size (int, optional): The number of high risk employees to return
                per page. Defaults to 100.

        Returns:
            generator: An object that iterates over :class:`py42.response.Py42Response` objects
            that each contain a page of users.
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
        filter_type=HighRiskEmployeeFilters.OPEN,
        sort_key=None,
        sort_direction=None,
        page_size=_PAGE_SIZE,
    ):
        """Gets a single page of High Risk Employees.

        Args:
            page_num (int): The page number to request.
            filter_type (str, optional): ``EXFILTRATION_30_DAYS``, ``EXFILTRATION_24_HOURS``,
                or ``OPEN``. Constants are available at
                :class:`py42.services.detectionlists.high_risk_employee.HighRiskEmployeeFilters`.
                Defaults to "OPEN".
            sort_key (str, optional): Sort results based by field. Defaults to None.
            sort_direction (str. optional): ``ASC`` or ``DESC``. Constants available at
                :class:`py42.constants.SortDirection`. Defaults to None.
            page_size (int, optional): The number of high risk employees to return
                per page. Defaults to 100.

        Returns:
            :class:`py42.response.Py42Response`
        """

        data = {
            u"tenantId": self._user_context.get_current_tenant_id(),
            u"filterType": filter_type,
            u"pgNum": page_num,
            u"pgSize": page_size,
            u"srtKey": sort_key,
            u"srtDirection": sort_direction,
        }
        uri = self._make_uri(u"/search")
        return self._connection.post(uri, json=data)
