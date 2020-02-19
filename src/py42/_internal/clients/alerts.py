import json

from py42._internal.compat import str
from py42._internal.base_classes import BaseClient


class AlertClient(BaseClient):
    _uri_prefix = u"/svc/api/v1/{0}"

    def __init__(self, session, user_context):
        super(AlertClient, self).__init__(session)
        self._user_context = user_context

    def search_alerts(self, query):
        query = str(query)
        uri = self._uri_prefix.format(u"query-alerts")
        return self._default_session.post(uri, data=query)

    def get_query_details(self, alert_ids, tenant_id=None):
        if type(alert_ids) is not list:
            alert_ids = [alert_ids]
        tenant_id = tenant_id if tenant_id else self._user_context.get_current_tenant_id()
        uri = self._uri_prefix.format(u"query-details")
        data = {u"tenantId": tenant_id, u"alertIds": alert_ids}
        return self._default_session.post(uri, data=json.dumps(data))

    def resolve_alert(self, alert_ids, tenant_id=None, reason=None):
        if type(alert_ids) is not list:
            alert_ids = [alert_ids]
        tenant_id = tenant_id if tenant_id else self._user_context.get_current_tenant_id()
        reason = reason if reason else u""
        uri = self._uri_prefix.format(u"resolve-alert")
        data = {u"tenantId": tenant_id, u"alertIds": alert_ids, u"reason": reason}
        return self._default_session.post(uri, data=json.dumps(data))

    def reopen_alert(self, alert_ids, tenant_id=None, reason=None):
        if type(alert_ids) is not list:
            alert_ids = [alert_ids]
        tenant_id = tenant_id if tenant_id else self._user_context.get_current_tenant_id()
        uri = self._uri_prefix.format(u"reopen-alert")
        data = {u"tenantId": tenant_id, u"alertIds": alert_ids, u"reason": reason}
        return self._default_session.post(uri, data=json.dumps(data))
