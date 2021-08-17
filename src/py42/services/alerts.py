import json

from py42 import settings
from py42.sdk.queries.query_filter import create_eq_filter_group
from py42.services import BaseService
from py42.services.util import get_all_pages


class AlertService(BaseService):
    _uri_prefix = "/svc/api"

    _CREATED_AT = "CreatedAt"
    _RULE_METADATA = "ruleMetadata"
    _SEARCH_KEY = "alerts"

    def __init__(self, connection, user_context):
        super().__init__(connection)
        self._user_context = user_context

    def search(self, query, page_num=1, page_size=None):
        query.page_number = page_num - 1
        if page_size:
            query.page_size = page_size
        query = self._add_tenant_id_if_missing(query)
        uri = f"{self._uri_prefix}/v1/query-alerts"
        return self._connection.post(uri, json=query)

    def get_search_page(self, query, page_num, page_size):
        query.page_number = page_num - 1
        query.page_size = page_size
        uri = f"{self._uri_prefix}/v1/query-alerts"
        query = self._add_tenant_id_if_missing(query)
        return self._connection.post(uri, json=query)

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
        uri = f"{self._uri_prefix}/v1/query-details"
        data = {"tenantId": tenant_id, "alertIds": alert_ids}
        results = self._connection.post(uri, json=data)
        return _convert_observation_json_strings_to_objects(results)

    def update_state(self, state, alert_ids, note=None):
        if not isinstance(alert_ids, (list, tuple)):
            alert_ids = [alert_ids]
        tenant_id = self._user_context.get_current_tenant_id()
        uri = f"{self._uri_prefix}/v1/update-state"
        data = {
            "tenantId": tenant_id,
            "alertIds": alert_ids,
            "note": note,
            "state": state,
        }
        return self._connection.post(uri, json=data)

    def _add_tenant_id_if_missing(self, query):
        query_dict = dict(query)
        tenant_id = query_dict.get("tenantId", None)
        if tenant_id is None:
            query_dict["tenantId"] = self._user_context.get_current_tenant_id()
            return query_dict
        else:
            return query_dict

    def get_rules_page(
        self, page_num, groups=None, sort_key=None, sort_direction=None, page_size=None
    ):
        # This API expects the first page to start with zero.
        page_num = page_num - 1
        page_size = page_size or settings.items_per_page
        data = {
            "tenantId": self._user_context.get_current_tenant_id(),
            "groups": groups or [],
            "groupClause": "AND",
            "pgNum": page_num,
            "pgSize": page_size,
            "srtKey": sort_key,
            "srtDirection": sort_direction,
        }
        uri = f"{self._uri_prefix}/v1/rules/query-rule-metadata"
        return self._connection.post(uri, json=data)

    def get_all_rules(self, sort_key=_CREATED_AT, sort_direction="DESC"):
        return get_all_pages(
            self.get_rules_page,
            self._RULE_METADATA,
            groups=None,
            sort_key=sort_key,
            sort_direction=sort_direction,
        )

    def get_all_rules_by_name(
        self, rule_name, sort_key=_CREATED_AT, sort_direction="DESC"
    ):
        return get_all_pages(
            self.get_rules_page,
            self._RULE_METADATA,
            groups=[json.loads(str(create_eq_filter_group("Name", rule_name)))],
            sort_key=sort_key,
            sort_direction=sort_direction,
        )

    def get_rule_by_observer_id(
        self, observer_id, sort_key=_CREATED_AT, sort_direction="DESC"
    ):
        results = get_all_pages(
            self.get_rules_page,
            self._RULE_METADATA,
            groups=[
                json.loads(str(create_eq_filter_group("ObserverRuleId", observer_id)))
            ],
            sort_key=sort_key,
            sort_direction=sort_direction,
        )
        return next(results)

    def update_note(self, alert_id, note):
        tenant_id = self._user_context.get_current_tenant_id()
        uri = f"{self._uri_prefix}/v1/add-note"
        data = {
            "tenantId": tenant_id,
            "alertId": alert_id,
            "note": note,
        }
        return self._connection.post(uri, json=data)

    def get_aggregate_data(self, alert_id):
        uri = f"{self._uri_prefix}/v2/query-details-aggregate"
        data = {"alertId": alert_id}
        response = self._connection.post(uri, json=data)
        response.data["alert"]["ffsUrl"] = response.data["alert"].get("ffsUrlEndpoint")
        return response


def _convert_observation_json_strings_to_objects(results):
    for alert in results["alerts"]:
        if "observations" in alert:
            for observation in alert["observations"]:
                try:
                    observation["data"] = json.loads(observation["data"])
                except Exception:
                    continue
    return results
