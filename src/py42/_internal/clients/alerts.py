import json

from py42._internal.compat import str
from py42.clients import BaseClient
from py42.clients.util import get_all_pages


class AlertClient(BaseClient):
    _uri_prefix = u"/svc/api/v1/{0}"

    def __init__(self, session, user_context):
        super(AlertClient, self).__init__(session)
        self._user_context = user_context

    def search(self, query):
        query = self._add_tenant_id_if_missing(query)
        uri = self._uri_prefix.format(u"query-alerts")
        return self._session.post(uri, data=query)

    def get_details(self, alert_ids, tenant_id=None):
        if type(alert_ids) is not list:
            alert_ids = [alert_ids]
        tenant_id = tenant_id if tenant_id else self._user_context.get_current_tenant_id()
        uri = self._uri_prefix.format(u"query-details")
        data = {u"tenantId": tenant_id, u"alertIds": alert_ids}
        return self._session.post(uri, data=json.dumps(data))

    def resolve(self, alert_ids, tenant_id=None, reason=None):
        if type(alert_ids) is not list:
            alert_ids = [alert_ids]
        tenant_id = tenant_id if tenant_id else self._user_context.get_current_tenant_id()
        reason = reason if reason else u""
        uri = self._uri_prefix.format(u"resolve-alert")
        data = {u"tenantId": tenant_id, u"alertIds": alert_ids, u"reason": reason}
        return self._session.post(uri, data=json.dumps(data))

    def reopen(self, alert_ids, tenant_id=None, reason=None):
        if type(alert_ids) is not list:
            alert_ids = [alert_ids]
        tenant_id = tenant_id if tenant_id else self._user_context.get_current_tenant_id()
        uri = self._uri_prefix.format(u"reopen-alert")
        data = {u"tenantId": tenant_id, u"alertIds": alert_ids, u"reason": reason}
        return self._session.post(uri, data=json.dumps(data))

    def _add_tenant_id_if_missing(self, query):
        query_dict = json.loads(str(query))
        tenant_id = query_dict.get(u"tenantId", None)
        if tenant_id is None:
            query_dict[u"tenantId"] = self._user_context.get_current_tenant_id()
            return json.dumps(query_dict)
        else:
            return str(query)

    def _get_alert_rules(
        self, tenant_id, sort_key=None, sort_direction=None, page_num=None, page_size=None
    ):
        data = {
            u"tenantId": tenant_id,
            u"groups": [],
            u"groupClause": u"AND",
            u"pgNum": page_num - 1,  # Minus 1, as this API expects first page to start with zero.
            u"pgSize": page_size,
            u"srtKey": sort_key,
            u"srtDirection": sort_direction,
        }
        uri = self._uri_prefix.format(u"rules/query-rule-metadata")
        return self._session.post(uri, data=json.dumps(data))

    def get_all_rules(self, sort_key=u"CreatedAt", sort_direction=u"DESC"):
        tenant_id = self._user_context.get_current_tenant_id()
        return get_all_pages(
            self._get_alert_rules,
            u"ruleMetadata",
            tenant_id=tenant_id,
            sort_key=sort_key,
            sort_direction=sort_direction,
        )

    def get_rules_by_name(self, rule_name):
        rule_pages = self.get_all_rules()
        matched_rules = []
        for rule_page in rule_pages:
            rules = rule_page[u"ruleMetadata"]
            for rule in rules:
                if rule_name.lower() == rule[u"name"].lower():
                    matched_rules.append(rule)
        return matched_rules
