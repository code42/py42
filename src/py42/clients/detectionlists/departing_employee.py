import json

from py42.clients import BaseClient
from py42.clients.util import get_all_pages


class DepartingEmployeeClient(BaseClient):
    """A client for interacting with Code42 Departing Employee APIs."""

    _uri_prefix = u"/svc/api/v2/departingemployee/{0}"

    def __init__(self, session, user_context, detection_list_user_client):
        super(DepartingEmployeeClient, self).__init__(session)
        self._user_context = user_context
        self._detection_list_user_client = detection_list_user_client

    def add(self, user_id, departure_date=None):
        """Adds a user to the Departing Employees list. Creates a detection list user profile if one
         didn't already exist.
        `REST Documentation <https://ecm-east.us.code42.com/svc/swagger/index.html?urls.primaryName=v2#/>`__

        Raises a :class:`Py42BadRequestError` when a user already exists in the Departing Employee
        detection list.

        Args:
            user_id (str or int): The Code42 userUid of the user you want to add to the departing
                employees list.
            departure_date (str, optional): Date in YYYY-MM-DD format. Date is treated as UTC. Defaults to None.

        Returns:
            :class:`py42.response.Py42Response`
        """
        if self._detection_list_user_client.create_if_not_exists(user_id):
            tenant_id = self._user_context.get_current_tenant_id()

            data = {u"tenantId": tenant_id, u"userId": user_id, u"departureDate": departure_date}
            uri = self._uri_prefix.format(u"add")
            return self._session.post(uri, data=json.dumps(data))

    def get(self, user_id):
        """Gets departing employee data of a user.
        `REST Documentation <https://ecm-east.us.code42.com/svc/swagger/index.html?urls.primaryName=v2#/>`__

        Args:
            user_id (str or int): The Code42 userUid of the user.

        Returns:
            :class:`py42.sdk.response.Py42Response`
        """
        tenant_id = self._user_context.get_current_tenant_id()
        uri = self._uri_prefix.format(u"get")
        data = {u"userId": user_id, u"tenantId": tenant_id}
        return self._session.post(uri, data=json.dumps(data))

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
        return self._session.post(uri, data=json.dumps(data))

    def _get_departing_employees_page(
        self,
        tenant_id=None,
        filter_type=None,
        sort_key=u"CREATED_AT",
        sort_direction=u"DESC",
        page_num=None,
        page_size=None,
    ):

        uri = self._uri_prefix.format(u"search")
        data = {
            u"tenantId": tenant_id,
            u"pgSize": 100,
            u"pgNum": page_num,
            u"filterType": filter_type,
            u"srtKey": sort_key,
            u"srtDirection": sort_direction,
        }
        return self._session.post(uri, data=json.dumps(data))

    def get_all(self, filter_type=u"OPEN", sort_key=u"CREATED_AT", sort_direction=u"DESC"):
        """Gets all Departing Employees.

        Args:
            filter_type (str, optional): Filter results by status. Defaults to "OPEN".
            sort_key (str, optional): Key to sort results on. Options: (``CREATED_AT``,
                ``DEPARTURE_DATE``, ``DISPLAY_NAME``, ``NUM_EVENTS``, ``TOTAL_BYTES``). Defaults to
                ``CREATED_AT``.
            sort_direction (str, optional): Sort direction. Options: (``ASC``, ``DESC``). Defaults
                to ``DESC``.

        Returns:
            generator: An object that iterates over :class:`py42.response.Py42Response` objects
            that each contain a page of departing employees.
        """
        return get_all_pages(
            self._get_departing_employees_page,
            u"items",
            tenant_id=self._user_context.get_current_tenant_id(),
            filter_type=filter_type,
            sort_key=sort_key,
            sort_direction=sort_direction,
        )

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
        return self._session.post(uri, data=json.dumps(data))

    def update_departure_date(self, user_id, departure_date):
        """Add or modify details of an existing Departing Employee case.
        `REST Documentation <https://ecm-east.us.code42.com/svc/swagger/index.html?urls.primaryName=v2#/>`__

        Args:
            user_id (str): The Code42 userUid of the user.
            departure_date (date): Date in YYYY-MM-DD format. Date is treated as UTC.

        Returns:
            :class:`py42.sdk.response.Py42Response`
        """

        tenant_id = self._user_context.get_current_tenant_id()

        uri = self._uri_prefix.format(u"update")
        data = {u"tenantId": tenant_id, u"userId": user_id, u"departureDate": departure_date}
        return self._session.post(uri, data=json.dumps(data))
