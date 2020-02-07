from py42._internal.base_classes import BaseDetectionClient


class DepartingEmployeeClient(BaseDetectionClient):
    def add_departing_employee(
        self,
        tenant_id,
        user_name,
        notes=None,
        departure_date=None,
        alerts_enabled=True,
        cloud_user_names=None,
    ):
        data = {
            u"tenantId": tenant_id,
            u"userName": user_name,
            u"notes": notes,
            u"departureDate": departure_date,
            u"alertsEnables": alerts_enabled,
            u"cloudUserNames": cloud_user_names,
        }
        uri = u"/departingemployee/create"
        return self._session.post(uri, data=data)
