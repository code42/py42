import json

from py42.clients import BaseClient
from py42.clients.detectionlists import _PAGE_NUM
from py42.clients.detectionlists import _PAGE_SIZE
from py42.clients.util import get_all_pages


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
            return self._add_high_risk_employee(tenant_id, user_id)

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

    def get_page(
        self,
        filter_type=None,
        sort_key=None,
        sort_direction=None,
        page_num=_PAGE_NUM,
        page_size=_PAGE_SIZE,
    ):
        """Gets a single page of High Risk Employees.

        Args:
            filter_type (str, optional): Valid filter types. Defaults to None.
            sort_key (str, optional): Sort results based by field. Defaults to None.
            sort_direction (str. optional): ``ASC`` or ``DESC``. Defaults to None.
            page_num (str or int, optional): The page number to request. Defaults to 1.
            page_size (str or int, optional): The items to have per page. Defaults to 100.

        Returns:
            :class:`py42.response.Py42Response`
        """

        return self._get_page(
            tenant_id=self._user_context.get_current_tenant_id(),
            filter_type=filter_type,
            sort_key=sort_key,
            sort_direction=sort_direction,
            page_num=page_num,
            page_size=page_size,
        )

    def get_all(self, filter_type=u"OPEN", sort_key=None, sort_direction=None):
        """Searches High Risk Employee list. Filter results by filter_type.

        Args:
            filter_type (str, optional): Valid filter types. Defaults to "OPEN".
            sort_key (str, optional): Sort results based by field. Defaults to None.
            sort_direction (str, optional): ``ASC`` or ``DESC``. Defaults to None.

        Returns:
            generator: An object that iterates over :class:`py42.response.Py42Response` objects
            that each contain a page of users.
        """

        return get_all_pages(
            self._get_page,
            u"items",
            tenant_id=self._user_context.get_current_tenant_id(),
            filter_type=filter_type,
            sort_key=sort_key,
            sort_direction=sort_direction,
            page_size=_PAGE_SIZE,
        )

    def _get_page(
        self,
        tenant_id,
        filter_type=None,
        sort_key=None,
        sort_direction=None,
        page_num=None,
        page_size=None,
    ):
        # This method is meant to called in `get_all()` and handles paging through
        # `util.get_all_pages()`. It exists separately than `get_page()` because of
        # the tenant ID parameter and trying to avoid it.
        data = {
            u"tenantId": tenant_id,
            u"filterType": filter_type,
            u"pgNum": page_num,
            u"pgSize": page_size,
            u"srtKey": sort_key,
            u"srtDirection": sort_direction,
        }
        uri = self._make_uri(u"/search")
        return self._session.post(uri, data=json.dumps(data))
