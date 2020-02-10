import json
from py42._internal.base_classes import BaseDetectionClient


class DepartingEmployeeClient(BaseDetectionClient):
    def create_departing_employee(
        self,
        user_name,
        tenant_id,
        notes=None,
        departure_date=None,
        alerts_enabled=True,
        cloud_usernames=None,
    ):
        data = {
            u"userName": user_name,
            u"tenantId": tenant_id,
            u"notes": notes,
            u"departureDate": departure_date,
            u"alertsEnabled": alerts_enabled,
            u"cloudUsernames": cloud_usernames,
        }

        uri = u"/svc/api/v1/departingemployee/create"
        return self._session.post(uri, data=json.dumps(data))

    def resolve_departing_employee(self, case_id, tenant_id):
        uri = u"/svc/api/v1/departingemployee/resolve"
        data = {u"caseId": case_id, u"tenantId": tenant_id}
        return self._session.post(uri, data=json.dumps(data))

    def search_departing_employees(
        self,
        tenant_id,
        page_size=None,
        page_num=None,
        departing_on_or_after=None,
        sort_key="CREATED_AT",
        sort_direction="DESC",
    ):
        uri = u"/svc/api/v1/departingemployee/search"
        data = {
            u"tenantId": tenant_id,
            u"pgSize": page_size,
            u"pgNum": page_num,
            u"departingOnOrAfter": departing_on_or_after,
            u"srtKey": sort_key,
            u"srtDirection": sort_direction,
        }
        return self._session.post(uri, data=json.dumps(data))

    def validate_user(self, user_name, tenant_id):
        uri = u"/svc/api/v1/departingemployee/validateuser"
        data = {u"userName": user_name, u"tenantId": tenant_id}
        return self._session.post(uri, data=json.dumps(data))
