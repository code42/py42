from warnings import warn

from py42.choices import Choices
from py42.exceptions import Py42BadRequestError
from py42.exceptions import Py42NotFoundError
from py42.exceptions import Py42UserNotOnListError
from py42.services import BaseService
from py42.services.detectionlists import _DetectionListFilters
from py42.services.detectionlists import _PAGE_SIZE
from py42.services.detectionlists import handle_user_already_added_error
from py42.services.util import get_all_pages


class HighRiskEmployeeFilters(_DetectionListFilters, Choices):
    """Deprecated. Use :class:`~py42.clients.watchlists.WatchlistsClient` and :class:`~py42.clients.userriskprofile.UserRiskProfileClient` instead. Constants available for filtering High Risk Employee search results.

    * ``OPEN``
    * ``EXFILTRATION_30_DAYS``
    * ``EXFILTRATION_24_HOURS``
    """


class HighRiskEmployeeService(BaseService):
    """`Deprecated. Use :class:`~py42.clients.watchlists.WatchlistsClient` and :class:`~py42.clients.userriskprofile.UserRiskProfileClient` instead. A service for interacting with High Risk Employee APIs."""

    _resource = "v2/highriskemployee"

    def __init__(self, connection, user_context, user_profile_service):
        super().__init__(connection)
        self._user_context = user_context
        self._user_profile_service = user_profile_service

    def _make_uri(self, action):
        return f"{self._resource}{action}"

    def _add_high_risk_employee(self, tenant_id, user_id):
        data = {"tenantId": tenant_id, "userId": user_id}
        uri = self._make_uri("/add")
        return self._connection.post(uri, json=data)

    def add(self, user_id):
        """Deprecated. Use watchlists instead. Adds a user to the High Risk Employee detection list.

        Raises a :class:`Py42UserAlreadyAddedError` when a user already exists in the High Risk Employee
        detection list.
        `REST Documentation <https://developer.code42.com/api/#operation/HighRiskEmployeeControllerV2_AddEmployee>`__

        Args:
            user_id (str or int): The Code42 userUid of the user you want to add to the High Risk
                Employee detection list.

        Returns:
            :class:`py42.response.Py42Response`
        """
        warn(
            "Detection lists are deprecated. Use watchlists instead.",
            DeprecationWarning,
            stacklevel=2,
        )
        tenant_id = self._user_context.get_current_tenant_id()
        try:
            return self._add_high_risk_employee(tenant_id, user_id)
        except Py42BadRequestError as err:
            handle_user_already_added_error(err, user_id, "high-risk-employee list")
            raise

    def set_alerts_enabled(self, enabled=True):
        """Deprecated. Enables alerts.
        `Rest Documentation <https://developer.code42.com/api/#operation/HighRiskEmployeeControllerV2_SetAlertState>`__

        Args:
            enabled (bool): Whether to enable alerts for all users.

        Returns:
            :class:`py42.response.Py42Response`
        """
        warn("This method is deprecated.", DeprecationWarning, stacklevel=2)
        data = {
            "tenantId": self._user_context.get_current_tenant_id(),
            "alertsEnabled": enabled,
        }
        uri = self._make_uri("/setalertstate")
        return self._connection.post(uri, json=data)

    def remove(self, user_id):
        """Deprecated. Use watchlists instead. Removes a user from the High Risk Employee detection list.
        `Rest Documentation <https://developer.code42.com/api/#operation/HighRiskEmployeeControllerV2_RemoveUser>`__

        Args:
            user_id (str or int): The Code42 userUid of the user you want to add to the High Risk
                Employee detection list.

        Returns:
            :class:`py42.response.Py42Response`
        """
        warn(
            "Detection lists are deprecated. Use watchlists instead.",
            DeprecationWarning,
            stacklevel=2,
        )
        data = {
            "tenantId": self._user_context.get_current_tenant_id(),
            "userId": user_id,
        }
        uri = self._make_uri("/remove")
        try:
            return self._connection.post(uri, json=data)
        except Py42NotFoundError as err:
            raise Py42UserNotOnListError(err, user_id, "high-risk-employee")

    def get(self, user_id):
        """Deprecated. Use userriskprofile.get_by_id() instead. Gets user information.
        `Rest Documentation <https://developer.code42.com/api/#operation/HighRiskEmployeeControllerV2_GetEmployee>`__

        Args:
            user_id (str or int): The Code42 userUid of the user has been added to the High Risk
                Employee detection list.

        Returns:
            :class:`py42.response.Py42Response`
        """
        warn(
            "This method is deprecated. Use userriskprofile.get_by_id() instead.",
            DeprecationWarning,
            stacklevel=2,
        )
        data = {
            "tenantId": self._user_context.get_current_tenant_id(),
            "userId": user_id,
        }
        uri = self._make_uri("/get")
        return self._connection.post(uri, json=data)

    def get_all(
        self,
        filter_type=HighRiskEmployeeFilters.OPEN,
        sort_key=None,
        sort_direction=None,
        page_size=_PAGE_SIZE,
    ):
        """Deprecated. Use userriskprofile.get_all() instead. Searches High Risk Employee list. Filter results by filter_type.
        `Rest Documentation <https://developer.code42.com/api/#operation/HighRiskEmployeeControllerV2_Search>`__

        Args:
            filter_type (str, optional): Constants available at
                :class:`py42.constants.HighRiskEmployeeFilters`.
                Defaults to ``OPEN``.
            sort_key (str, optional): Sort results based by field. Defaults to None.
            sort_direction (str, optional): ``ASC`` or ``DESC``. Constants available at
                :class:`py42.constants.SortDirection`. Defaults to None.
            page_size (int, optional): The number of high risk employees to return
                per page. Defaults to 100.

        Returns:
            generator: An object that iterates over :class:`py42.response.Py42Response` objects
            that each contain a page of users.
        """
        warn(
            "This method is deprecated. Use userriskprofile.get_all() instead.",
            DeprecationWarning,
            stacklevel=2,
        )

        return get_all_pages(
            self.get_page,
            "items",
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
        """Deprecated. Use userriskprofile.get_page() instead. Gets a single page of High Risk Employees.

        Args:
            page_num (int): The page number to request.
            filter_type (str, optional): Constants available at
                :class:`py42.constants.HighRiskEmployeeFilters`.
                Defaults to "OPEN".
            sort_key (str, optional): Sort results based by field. Defaults to None.
            sort_direction (str. optional): ``ASC`` or ``DESC``. Constants available at
                :class:`py42.constants.SortDirection`. Defaults to None.
            page_size (int, optional): The number of high risk employees to return
                per page. Defaults to 100.

        Returns:
            :class:`py42.response.Py42Response`
        """

        warn(
            "This method is deprecated. Use userriskprofile.get_page() instead.",
            DeprecationWarning,
            stacklevel=2,
        )

        data = {
            "tenantId": self._user_context.get_current_tenant_id(),
            "filterType": filter_type,
            "pgNum": page_num,
            "pgSize": page_size,
            "srtKey": sort_key,
            "srtDirection": sort_direction,
        }
        uri = self._make_uri("/search")
        return self._connection.post(uri, json=data)
