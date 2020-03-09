from py42._internal.compat import str
from py42.sdk.queries import BaseQuery
from py42.sdk.queries.alerts.filters.alert_filter import AlertQueryFilterStringField
from py42.sdk.queries.query_filter import QueryFilterStringField, QueryFilterTimestampField


class DateObserved(QueryFilterTimestampField):
    _term = u"CreatedAt"


class Actor(AlertQueryFilterStringField):
    _term = u"actor"


class RuleName(AlertQueryFilterStringField):
    _term = u"name"


class Description(AlertQueryFilterStringField):
    _term = u"description"


class Severity(QueryFilterStringField):
    _term = u"severity"

    HIGH = u"HIGH"
    MEDIUM = u"MEDIUM"
    LOW = u"LOW"


class AlertState(QueryFilterStringField):
    _term = u"state"

    OPEN = u"OPEN"
    DISMISSED = u"RESOLVED"


class AlertQuery(BaseQuery):
    def __init__(self, tenant_id, *args, **kwargs):
        super(AlertQuery, self).__init__(*args, **kwargs)
        self._tenant_id = tenant_id
        self.sort_key = u"CreatedAt"
        self.page_number = 0
        self.sort_direction = u"desc"

    def __str__(self):
        groups_string = u",".join(str(group_item) for group_item in self._filter_group_list)
        json = u'{{"tenantId":"{0}", "groupClause":"{1}", "groups":[{2}], "pgNum":{3}, "pgSize":{4}, "srtDirection":"{5}", "srtKey":"{6}"}}'.format(
            self._tenant_id,
            self._group_clause,
            groups_string,
            self.page_number,
            self.page_size,
            self.sort_direction,
            self.sort_key,
        )
        return json
