import json

from py42.clients import BaseClient
from py42.clients.util import get_all_pages
from py42.util import convert_timestamp_to_str


class DepartingEmployeeClient(BaseClient):
    """A client for interacting with Code42 Departing Employee APIs."""

    _uri_prefix = u"/svc/api/v1/departingemployee/{0}"

    def __init__(self, session, user_context):
        super(DepartingEmployeeClient, self).__init__(session)
        self._user_context = user_context

    def create(
        self, username, tenant_id=None, notes=None, departure_epoch=None, cloud_usernames=None
    ):
        """Adds a user to Departing Employees.
        `REST Documentation <https://ecm-default.prod.ffs.us2.code42.com/svc/swagger/index.html#/DepartingEmployeeCase/DepartingEmployeeCase_Create>`__

        Args:
            username (str): The username of the departing employee.
            tenant_id (str, optional): The identifier of the Customer tenant the user is in.
                Defaults to None (the tenant_id of SDK authorization user will be used).
            notes (str, optional): Optional descriptive information. Defaults to None.
            departure_epoch (int, optional): Employee departure date as POSIX timestamp. Defaults
                to None.
            cloud_usernames (list, optional): List of alternate usernames for this user from
                external data sources being searched by Forensic File Search (Google Drive, Box,
                OneDrive, Gmail, Office 365). Defaults to None.

        Returns:
            :class:`py42.response.Py42Response`
        """

        tenant_id = tenant_id if tenant_id else self._user_context.get_current_tenant_id()
        cloud_usernames = cloud_usernames if cloud_usernames else []
        departure_date = (
            convert_timestamp_to_str(departure_epoch) if departure_epoch else departure_epoch
        )
        data = {
            u"userName": username,
            u"tenantId": tenant_id,
            u"notes": notes,
            u"departureDate": departure_date,
            u"alertsEnabled": True,
            u"cloudUsernames": cloud_usernames,
        }
        uri = self._uri_prefix.format(u"create")
        return self._session.post(uri, data=json.dumps(data))

    def resolve(self, case_id, tenant_id=None):
        """Removes a user from Departing Employees.
        `REST Documentation <https://ecm-default.prod.ffs.us2.code42.com/svc/swagger/index.html#/DepartingEmployeeCase/DepartingEmployeeCase_ResolveCase>`__

        Args:
            case_id (str): The identifier of the Departing Employee.
            tenant_id (str, optional): The identifier of the Customer tenant the case is in.
                Defaults to None (the tenant_id of SDK authorization user will be used).

        Returns:
            :class:`py42.response.Py42Response`
        """

        tenant_id = tenant_id if tenant_id else self._user_context.get_current_tenant_id()
        uri = self._uri_prefix.format(u"resolve")
        data = {u"caseId": case_id, u"tenantId": tenant_id}
        return self._session.post(uri, data=json.dumps(data))

    def _get_departing_employees_page(
        self,
        tenant_id=None,
        departing_on_or_after_epoch=None,
        sort_key=u"CREATED_AT",
        sort_direction=u"DESC",
        page_num=None,
        page_size=None,
    ):

        tenant_id = tenant_id if tenant_id else self._user_context.get_current_tenant_id()
        departing_on_or_after_date = (
            convert_timestamp_to_str(departing_on_or_after_epoch)
            if departing_on_or_after_epoch
            else departing_on_or_after_epoch
        )
        uri = self._uri_prefix.format(u"search")
        data = {
            u"tenantId": tenant_id,
            u"pgSize": 100,
            u"pgNum": page_num,
            u"departingOnOrAfter": departing_on_or_after_date,
            u"srtKey": sort_key,
            u"srtDirection": sort_direction,
        }
        return self._session.post(uri, data=json.dumps(data))

    def get_all(
        self,
        tenant_id=None,
        departing_on_or_after_epoch=None,
        sort_key=u"CREATED_AT",
        sort_direction=u"DESC",
    ):
        """Gets all Departing Employees.

        Args:
            tenant_id (str, optional): The identifier of the Customer tenant. Defaults to None (the
                tenant_id of SDK authorization user will be used).
            departing_on_or_after_epoch (int, optional): Filter results by the departure date of
                employee, requires a POSIX timestamp. Defaults to None.
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
            u"cases",
            tenant_id=tenant_id,
            departing_on_or_after_epoch=departing_on_or_after_epoch,
            sort_key=sort_key,
            sort_direction=sort_direction,
        )

    def toggle_alerts(self, tenant_id=None, alerts_enabled=True):
        """Enable or disable email alerting on Departing Employee exposure events.
        `REST Documentation <https://ecm-default.prod.ffs.us2.code42.com/svc/swagger/index.html#/DepartingEmployeeCase/DepartingEmployeeCase_ToggleAlerts>`__

        Args:
            tenant_id (str, optional): The identifier of the Customer tenant. Defaults to None (the
                tenant_id of SDK authorization user will be used).
            alerts_enabled (bool): Set alerting to on (True) or off (False). Defaults to True.

        Returns:
            :class:`py42.response.Py42Response`
        """
        tenant_id = tenant_id if tenant_id else self._user_context.get_current_tenant_id()
        uri = self._uri_prefix.format(u"togglealerts")
        data = {u"tenantId": tenant_id, u"alertsEnabled": alerts_enabled}
        return self._session.post(uri, data=json.dumps(data))

    def get_by_username(self, username, tenant_id=None):
        """Gets Departing Employee case detail for a given user.

        Arguments:
            username (str): Username of the Departing Employee to retrieve case info on.
            tenant_id (str, optional): The identifier of the Customer tenant the case is in.
                Defaults to None (the tenant_id of SDK authorization user will be used).

        Returns:
            :class:`py42.response.Py42Response`: A response containing the Departing Employee case.
        """
        tenant_id = tenant_id if tenant_id else self._user_context.get_current_tenant_id()
        case_id = self._get_case_id_from_username(tenant_id, username)
        return self.get_by_id(case_id, tenant_id)

    def get_by_id(self, case_id, tenant_id=None):
        """Gets details about a Departing Employee case.
        `REST Documentation <https://ecm-default.prod.ffs.us2.code42.com/svc/swagger/index.html#/DepartingEmployeeCase/DepartingEmployeeCase_Details>`__

        Args:
            case_id (str): Identifier of the Departing Employee case.
            tenant_id (str, optional): The identifier of the Customer tenant the case is in.
                Defaults to None (the tenant_id of SDK authorization user will be used).

        Returns:
            :class:`py42.response.Py42Response`: A response containing the Departing Employee case.
        """
        tenant_id = tenant_id if tenant_id else self._user_context.get_current_tenant_id()
        uri = self._uri_prefix.format(u"details")
        data = {u"tenantId": tenant_id, u"caseId": case_id}
        return self._session.post(uri, data=json.dumps(data))

    def update(
        self,
        case_id,
        tenant_id=None,
        display_name=None,
        notes=None,
        departure_epoch=None,
        cloud_usernames=None,
    ):
        """Add or modify details of an existing Departing Employee case.
        `REST Documentation <https://ecm-default.prod.ffs.us2.code42.com/svc/swagger/index.html#/DepartingEmployeeCase/DepartingEmployeeCase_Update>`__

        Args:
            case_id (str): Identifier of the Departing Employee case.
            tenant_id (str, optional): The identifier of the Customer tenant the case is in.
                Defaults to None (the tenant_id of SDK authorization user will be used).
            display_name (str, optional): The display name for the Departing Employee case. This
                defaults to username when adding a new Departing Employee, so it can be used to make
                the UI more user-friendly if your Organization has usernames that don't correspond
                to real names. Defaults to None.
            notes (str, optional): Optional descriptive information. Defaults to None.
            departure_epoch (int, optional): Employee departure date as POSIX timestamp. Defaults
                to None.
            cloud_usernames (list, optional): List of alternate usernames for this user from
                external data sources being searched by Forensic File Search (Google Drive, Box,
                OneDrive, Gmail, Office 365). Defaults to None.

        Returns:
                :class:`py42.response.Py42Response`
        """

        tenant_id = tenant_id if tenant_id else self._user_context.get_current_tenant_id()

        # The behavior of the `update` API is to clear values that are not provided.
        # Therefore, we get current values first as to prevent clearing them when not provided.
        case = json.loads(self._get_case_by_id(case_id).text)

        display_name = display_name if display_name else case.get(u"displayName")
        notes = notes if notes else case.get(u"notes")
        departure_date = (
            convert_timestamp_to_str(departure_epoch)
            if departure_epoch
            else case.get(u"departureDate")
        )
        alerts_enabled = case.get(u"alertsEnabled")
        status = case.get(u"status")
        cloud_usernames = cloud_usernames if cloud_usernames else case.get(u"cloudUsernames")

        uri = self._uri_prefix.format(u"update")
        data = {
            u"tenantId": tenant_id,
            u"caseId": case_id,
            u"displayName": display_name,
            u"notes": notes,
            u"departureDate": departure_date,
            u"alertsEnabled": alerts_enabled,
            u"status": status,
            u"cloudUsernames": cloud_usernames,
        }
        return self._session.post(uri, data=json.dumps(data))

    def _get_case_id_from_username(self, tenant_id, username):
        case = self._get_case_from_username(tenant_id, username)
        if case is not None:
            return case.get(u"caseId")

    def _get_case_from_username(self, tenant_id, username):
        matches = None
        for page in self._get_all_departing_employees(tenant_id):
            matches = [c for c in page if c[u"userName"] == username]
            if matches:
                break
        return matches[0] if matches else None

    def _get_all_departing_employees(self, tenant_id):
        for page in self.get_all(tenant_id):
            yield page[u"cases"]

    def _get_case_by_id(self, case_id):
        return self.get_by_id(case_id)
