import json

from py42._internal.compat import str
from py42._internal.base_classes import BaseClient
from py42._internal.clients.util import get_all_pages
import py42.settings as settings
from py42.util import convert_timestamp_to_str


class DepartingEmployeeClient(BaseClient):
    _uri_prefix = u"/svc/api/v1/departingemployee/{0}"

    def __init__(self, session, user_context):
        super(DepartingEmployeeClient, self).__init__(session)
        self._user_context = user_context

    def create_departing_employee(
        self,
        username,
        tenant_id=None,
        notes=None,
        departure_epoch=None,
        alerts_enabled=True,
        cloud_usernames=None,
    ):
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
            u"alertsEnabled": alerts_enabled,
            u"cloudUsernames": cloud_usernames,
        }
        uri = self._uri_prefix.format(u"create")
        return self._default_session.post(uri, data=json.dumps(data))

    def resolve_departing_employee(self, case_id, tenant_id=None):
        tenant_id = tenant_id if tenant_id else self._user_context.get_current_tenant_id()
        uri = self._uri_prefix.format(u"resolve")
        data = {u"caseId": case_id, u"tenantId": tenant_id}
        return self._default_session.post(uri, data=json.dumps(data))

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
            u"pgSize": page_size,
            u"pgNum": page_num,
            u"departingOnOrAfter": departing_on_or_after_date,
            u"srtKey": sort_key,
            u"srtDirection": sort_direction,
        }
        return self._default_session.post(uri, data=json.dumps(data))

    def get_all_departing_employees(
        self,
        tenant_id=None,
        departing_on_or_after_epoch=None,
        sort_key=u"CREATED_AT",
        sort_direction=u"DESC",
    ):
        return get_all_pages(
            self._get_departing_employees_page,
            100,
            u"cases",
            tenant_id=tenant_id,
            departing_on_or_after_epoch=departing_on_or_after_epoch,
            sort_key=sort_key,
            sort_direction=sort_direction,
        )

    def toggle_alerts(self, tenant_id=None, alerts_enabled=True):
        tenant_id = tenant_id if tenant_id else self._user_context.get_current_tenant_id()
        uri = self._uri_prefix.format(u"togglealerts")
        data = {u"tenantId": tenant_id, u"alertsEnabled": alerts_enabled}
        return self._default_session.post(uri, data=json.dumps(data))

    def get_case_by_username(self, username, tenant_id=None):
        tenant_id = tenant_id if tenant_id else self._user_context.get_current_tenant_id()
        case_id = self._get_case_id_from_username(tenant_id, username)
        return self.get_case_by_id(case_id, tenant_id)

    def get_case_by_id(self, case_id, tenant_id=None):
        tenant_id = tenant_id if tenant_id else self._user_context.get_current_tenant_id()
        uri = self._uri_prefix.format(u"details")
        data = {u"tenantId": tenant_id, u"caseId": case_id}
        return self._default_session.post(uri, data=json.dumps(data))

    def update_case(
        self,
        case_id,
        tenant_id=None,
        display_name=None,
        notes=None,
        departure_epoch=None,
        alerts_enabled=None,
        status=None,
        cloud_usernames=None,
    ):
        tenant_id = tenant_id if tenant_id else self._user_context.get_current_tenant_id()

        # The behavior of the `update` API is to clear values that are not provided.
        # Therefore, we get current values first as to prevent clearing them when not provided.
        case = self._get_case_by_id(case_id)

        changed_status = status is not None and status != case.get(u"status")
        changed_alerts_enabled = alerts_enabled is not None and alerts_enabled != case.get(
            u"alertsEnabled"
        )

        display_name = display_name if display_name else case.get(u"displayName")
        notes = notes if notes else case.get(u"notes")
        departure_date = (
            convert_timestamp_to_str(departure_epoch)
            if departure_epoch
            else case.get(u"departureDate")
        )
        alerts_enabled = alerts_enabled if changed_alerts_enabled else case.get(u"alertsEnabled")
        status = status if changed_status else case.get(u"status")
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
        return self._default_session.post(uri, data=json.dumps(data))

    def _get_case_id_from_username(self, tenant_id, username):
        case = self._get_case_from_username(tenant_id, username)
        if case is not None:
            return case.get(u"caseId")

    def _get_case_from_username(self, tenant_id, username):
        matches = None
        for page in self._get_all_departing_employees(tenant_id):
            matches = [c for c in page if c.get(u"userName") == username]
            if matches:
                break
        return matches[0] if matches else None

    def _get_all_departing_employees(self, tenant_id):
        for page in self.get_all_departing_employees(tenant_id):
            yield json.loads(page.text).get(u"cases")

    def _get_case_by_id(self, case_id):
        response = self.get_case_by_id(case_id)
        if response:
            return json.loads(str(response.text))
