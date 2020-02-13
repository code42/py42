import json

from py42._internal.base_classes import BaseClient
from py42.util import get_obj_from_response


class AlertClient(BaseClient):
    _base_uri = u"/svc/api/v1/"
    _tenant_id = None

    def __init__(self, session, administration_client):
        super(AlertClient, self).__init__(session)
        self._administration = administration_client

    def get_all_alerts(
        self,
        tenant_id=None,
        groups=None,
        group_clause=u"AND",
        page_num=1,
        page_size=10,
        sort_key=u"CreatedAt",
        sort_direction=u"DESC",
    ):
        tenant_id = tenant_id if tenant_id else self._get_current_tenant_id()
        groups = groups if groups else []
        uri = self._get_uri(u"query-alerts")

        data = {
            u"tenantId": tenant_id,
            u"groups": groups,
            u"groupClause":group_clause,
            u"pgNum": page_num,
            u"pgSize": page_size,
            u"srtKey": sort_key,
            u"srtDirection": sort_direction,
        }
        return self._default_session.post(uri, data=json.dumps(data))

    def resolve_alert(self):
        pass

    def _get_uri(self, resource_name):
        return u"{0}{1}".format(self._base_uri, resource_name)

    def _get_current_tenant_id(self):
        if self._tenant_id is None:
            response = self._administration.get_current_tenant()
            tenant = get_obj_from_response(response, u"data")
            self._tenant_id = tenant.get(u"tenantUid")
        return self._tenant_id

    @staticmethod
    def _get_default_query():
        _filter = {u"term": u"State", u"operator": u"IS", u"value": u"OPEN"}
        return [{u"filters": [_filter], u"filterClause": u"AND"}]
