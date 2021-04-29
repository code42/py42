import json

from py42 import settings
from py42._compat import str
from py42.sdk.queries.query_filter import create_eq_filter_group
from py42.services import BaseService
from py42.services.util import get_all_pages


class AlertService(BaseService):
    _uri_prefix = u"/svc/api/v1/{0}"

    _CREATED_AT = u"CreatedAt"
    _RULE_METADATA = u"ruleMetadata"
    _SEARCH_KEY = u"alerts"

    def __init__(self, connection, user_context):
        super(AlertService, self).__init__(connection)
        self._user_context = user_context

    def search(self, query, page_num=1, page_size=None):
        query.page_number = page_num - 1
        if page_size:
            query.page_size = page_size
        query = self._add_tenant_id_if_missing(query)
        uri = self._uri_prefix.format(u"query-alerts")
        return self._connection.post(uri, data=query)

    def get_search_page(self, query, page_num, page_size):
        query.page_number = page_num - 1
        query.page_size = page_size
        uri = self._uri_prefix.format(u"query-alerts")
        query = self._add_tenant_id_if_missing(query)
        return self._connection.post(uri, data=query)

    def search_all_pages(self, query):
        return get_all_pages(
            self.get_search_page,
            self._SEARCH_KEY,
            query=query,
            page_size=query.page_size,
        )

    def get_details(self, alert_ids):
        if not isinstance(alert_ids, (list, tuple)):
            alert_ids = [alert_ids]
        tenant_id = self._user_context.get_current_tenant_id()
        uri = self._uri_prefix.format(u"query-details")
        data = {u"tenantId": tenant_id, u"alertIds": alert_ids}
        results = self._connection.post(uri, json=data)
        return _convert_observation_json_strings_to_objects(results)

    def update_state(self, state, alert_ids, note=None):
        if not isinstance(alert_ids, (list, tuple)):
            alert_ids = [alert_ids]
        tenant_id = self._user_context.get_current_tenant_id()
        uri = self._uri_prefix.format(u"update-state")
        data = {
            u"tenantId": tenant_id,
            u"alertIds": alert_ids,
            u"note": note,
            u"state": state,
        }
        return self._connection.post(uri, json=data)

    def _add_tenant_id_if_missing(self, query):
        query_dict = json.loads(str(query))
        tenant_id = query_dict.get(u"tenantId", None)
        if tenant_id is None:
            query_dict[u"tenantId"] = self._user_context.get_current_tenant_id()
            return json.dumps(query_dict)
        else:
            return str(query)

    def get_rules_page(
        self, page_num, groups=None, sort_key=None, sort_direction=None, page_size=None
    ):
        # This API expects the first page to start with zero.
        page_num = page_num - 1
        page_size = page_size or settings.items_per_page
        data = {
            u"tenantId": self._user_context.get_current_tenant_id(),
            u"groups": groups or [],
            u"groupClause": u"AND",
            u"pgNum": page_num,
            u"pgSize": page_size,
            u"srtKey": sort_key,
            u"srtDirection": sort_direction,
        }
        uri = self._uri_prefix.format(u"rules/query-rule-metadata")
        return self._connection.post(uri, json=data)

    def get_all_rules(self, sort_key=_CREATED_AT, sort_direction=u"DESC"):
        return get_all_pages(
            self.get_rules_page,
            self._RULE_METADATA,
            groups=None,
            sort_key=sort_key,
            sort_direction=sort_direction,
        )

    def get_all_rules_by_name(
        self, rule_name, sort_key=_CREATED_AT, sort_direction=u"DESC"
    ):
        return get_all_pages(
            self.get_rules_page,
            self._RULE_METADATA,
            groups=[json.loads(str(create_eq_filter_group(u"Name", rule_name)))],
            sort_key=sort_key,
            sort_direction=sort_direction,
        )

    def get_rule_by_observer_id(
        self, observer_id, sort_key=_CREATED_AT, sort_direction=u"DESC"
    ):
        results = get_all_pages(
            self.get_rules_page,
            self._RULE_METADATA,
            groups=[
                json.loads(str(create_eq_filter_group(u"ObserverRuleId", observer_id)))
            ],
            sort_key=sort_key,
            sort_direction=sort_direction,
        )
        return next(results)

    def update_note(self, alert_id, note):
        tenant_id = self._user_context.get_current_tenant_id()
        uri = self._uri_prefix.format(u"add-note")
        data = {
            u"tenantId": tenant_id,
            u"alertId": alert_id,
            u"note": note,
        }
        return self._connection.post(uri, json=data)

    def get_aggregate_data(self, alert_id):
        uri = self._uri_prefix.format(u"query-details-aggregate")
        data = {
            u"alertId": alert_id,
        }
        return self._connection.post(uri, json=data)


def _convert_observation_json_strings_to_objects(results):
    for alert in results[u"alerts"]:
        if u"observations" in alert:
            for observation in alert[u"observations"]:
                try:
                    observation[u"data"] = json.loads(observation[u"data"])
                except Exception:
                    continue
    return results
