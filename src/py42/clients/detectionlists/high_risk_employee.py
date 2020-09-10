import json

from py42.clients import BaseClient
from py42.clients.detectionlists import _PAGE_SIZE
from py42.clients.detectionlists import handle_user_already_added_error
from py42.clients.util import get_all_pages
from py42.exceptions import Py42BadRequestError


class HighRiskEmployeeClient(BaseClient):
    """A client for interacting with High Risk Employee APIs."""

    _api_version = u"v2"
    _uri_prefix = u"/svc/api/{}".format(_api_version)
    _resource = u"/highriskemployee"

    def __init__(self, session, user_context, detection_list_user_client):
        super(HighRiskEmployeeClient, self).__init__(session)
        self._user_context = user_context
        self._detection_list_user_client = detection_list_user_client

    def _make_uri(self, action):
        return u"{}{}{}".format(self._uri_prefix, self._resource, action)

    def _add_high_risk_employee(self, tenant_id, user_id):

        data = {u"tenantId": tenant_id, u"userId": user_id}
        uri = self._make_uri(u"/add")
        return self._session.post(uri, data=json.dumps(data))

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
        if self._detection_list_user_client.create_if_not_exists(user_id):
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
        return self._session.post(uri, data=json.dumps(data))

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
        return self._session.post(uri, data=json.dumps(data))

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
        return self._session.post(uri, data=json.dumps(data))

    def get_all(self, filter_type=u"OPEN", sort_key=None, sort_direction=None):
        """Searches High Risk Employee list. Filter results by filter_type.

        Args:
            filter_type (str, optional): ``EXFILTRATION_30_DAYS``, ``EXFILTRATION_24_HOURS``,
                or ``OPEN``. Defaults to "OPEN".
            sort_key (str, optional): Sort results based by field. Defaults to None.
            sort_direction (str, optional): ``ASC`` or ``DESC``. Defaults to None.

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
            page_size=_PAGE_SIZE,
        )

    def get_page(
        self,
        page_num,
        filter_type=u"OPEN",
        sort_key=None,
        sort_direction=None,
        page_size=_PAGE_SIZE,
    ):
        """Gets a single page of High Risk Employees.

        Args:
            page_num (int): The page number to request.
            filter_type (str, optional): ``EXFILTRATION_30_DAYS``, ``EXFILTRATION_24_HOURS``,
                or ``OPEN``. Defaults to "OPEN".
            sort_key (str, optional): Sort results based by field. Defaults to None.
            sort_direction (str. optional): ``ASC`` or ``DESC``. Defaults to None.
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
        return self._session.post(uri, data=json.dumps(data))
