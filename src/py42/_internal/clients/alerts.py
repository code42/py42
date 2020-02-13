import json

from py42._internal.compat import str
from py42._internal.base_classes import BaseClient


class AlertClient(BaseClient):
    _base_uri = u"/svc/api/v1/"
    _tenant_id = None

    def __init__(self, session, administration_client):
        super(AlertClient, self).__init__(session)
        self._administration = administration_client

    def search_alerts(self, query):
        query = str(query)
        uri = self._get_uri(u"query-alerts")
        return self._default_session.post(uri, data=query)

    def get_alert_details(self, alert_ids, tenant_id=None):
        tenant_id = tenant_id if tenant_id else self._get_current_tenant_id()
        uri = self._get_uri(u"query-details")
        data = {u"tenantId": tenant_id, u"alertIds": alert_ids}
        return self._default_session.post(uri, data=json.dumps(data))

    def resolve_alert(self, alert_ids, tenant_id=None, reason=None):
        tenant_id = tenant_id if tenant_id else self._get_current_tenant_id()
        reason = reason if reason else u""
        uri = self._get_uri(u"resolve-alert")
        data = {u"tenantId": tenant_id, u"alertIds": alert_ids, u"reason": reason}
        return self._default_session.post(uri, json.dumps(data))

    def _get_uri(self, resource_name):
        return u"{0}{1}".format(self._base_uri, resource_name)

    def _get_current_tenant_id(self):
        if self._tenant_id is None:
            self._tenant_id = self._administration.get_current_tenant_id()
        return self._tenant_id
