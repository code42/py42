import json

from py42 import settings
from py42._internal.compat import str
from py42.clients import BaseClient
from py42.clients.util import get_all_pages
from py42.sdk.queries.query_filter import create_eq_filter_group


class AlertClient(BaseClient):
    _uri_prefix = u"/svc/api/v1/{0}"

    def __init__(self, session, user_context):
        super(AlertClient, self).__init__(session)
        self._user_context = user_context

    def search(self, query):
        query = self._add_tenant_id_if_missing(query)
        uri = self._uri_prefix.format(u"query-alerts")
        return self._session.post(uri, data=query)

    def get_details(self, alert_ids):
        if not isinstance(alert_ids, (list, tuple)):
            alert_ids = [alert_ids]
        tenant_id = self._user_context.get_current_tenant_id()
        uri = self._uri_prefix.format(u"query-details")
        data = {u"tenantId": tenant_id, u"alertIds": alert_ids}
        results = self._session.post(uri, data=json.dumps(data))
        return _convert_observation_json_strings_to_objects(results)

    def resolve(self, alert_ids, reason=None):
        if not isinstance(alert_ids, (list, tuple)):
            alert_ids = [alert_ids]
        tenant_id = self._user_context.get_current_tenant_id()
        reason = reason or u""
        uri = self._uri_prefix.format(u"resolve-alert")
        data = {u"tenantId": tenant_id, u"alertIds": alert_ids, u"reason": reason}
        return self._session.post(uri, data=json.dumps(data))

    def reopen(self, alert_ids, reason=None):
        if not isinstance(alert_ids, (list, tuple)):
            alert_ids = [alert_ids]
        tenant_id = self._user_context.get_current_tenant_id()
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

    def get_page(
        self,
        tenant_id=None,
        groups=None,
        sort_key=None,
        sort_direction=None,
        page_num=1,
        page_size=None,
    ):
        page_size = page_size or settings.items_per_page
        tenant_id = tenant_id or self._user_context.get_current_tenant_id()
        return self._get_page(
            tenant_id=tenant_id,
            groups=groups,
            sort_key=sort_key,
            sort_direction=sort_direction,
            page_num=page_num,
            page_size=page_size,
        )

    def _get_page(
        self,
        tenant_id,
        groups=None,
        sort_key=None,
        sort_direction=None,
        page_num=None,
        page_size=None,
    ):
        # This method exists separately from `get_page()` because
        # of the tenant ID parameter - trying to avoid it and avoid duplicate calls
        # to retrieve it.

        # This API expects the first page to start with zero.
        page_num = page_num - 1
        data = {
            u"tenantId": tenant_id,
            u"groups": groups or [],
            u"groupClause": u"AND",
            u"pgNum": page_num,
            u"pgSize": page_size,
            u"srtKey": sort_key,
            u"srtDirection": sort_direction,
        }
        uri = self._uri_prefix.format(u"rules/query-rule-metadata")
        return self._session.post(uri, data=json.dumps(data))

    def get_all_rules(self, sort_key=u"CreatedAt", sort_direction=u"DESC"):
        tenant_id = self._user_context.get_current_tenant_id()
        return get_all_pages(
            self._get_page,
            u"ruleMetadata",
            tenant_id=tenant_id,
            groups=None,
            sort_key=sort_key,
            sort_direction=sort_direction,
        )

    def get_all_rules_by_name(
        self, rule_name, sort_key=u"CreatedAt", sort_direction=u"DESC"
    ):
        tenant_id = self._user_context.get_current_tenant_id()
        return get_all_pages(
            self._get_page,
            u"ruleMetadata",
            tenant_id=tenant_id,
            groups=[json.loads(str(create_eq_filter_group(u"Name", rule_name)))],
            sort_key=sort_key,
            sort_direction=sort_direction,
        )

    def get_rule_by_observer_id(
        self, observer_id, sort_key=u"CreatedAt", sort_direction=u"DESC"
    ):
        tenant_id = self._user_context.get_current_tenant_id()
        results = get_all_pages(
            self._get_page,
            u"ruleMetadata",
            tenant_id=tenant_id,
            groups=[
                json.loads(str(create_eq_filter_group(u"ObserverRuleId", observer_id)))
            ],
            sort_key=sort_key,
            sort_direction=sort_direction,
        )
        return next(results)


def _convert_observation_json_strings_to_objects(results):
    for alert in results[u"alerts"]:
        if u"observations" in alert:
            for observation in alert[u"observations"]:
                try:
                    observation[u"data"] = json.loads(observation[u"data"])
                except Exception:
                    continue
    return results
