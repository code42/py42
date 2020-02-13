from py42._internal.base_classes import BaseQuery
from py42._internal.clients.administration import AdministrationClient
from py42._internal.query_filter import (
    _QueryFilterStringField,
    _QueryFilterTimestampField,
)
from py42.util import get_obj_from_response


class DateObserved(_QueryFilterTimestampField):
    _term = u"CreatedAt"


class Actor(_QueryFilterStringField):
    _term = u"actor"


class Severity(_QueryFilterStringField):
    _term = u"severity"


class RuleName(_QueryFilterStringField):
    _term = u"name"


class Description(_QueryFilterStringField):
    _term = u"description"


class AlertState(_QueryFilterStringField):
    _term = u"State"


class AlertQuery(BaseQuery):
    def __init__(self, tenant_id, *args, **kwargs):
        super(AlertQuery, self).__init__(*args, **kwargs)
        self._tenant_id = tenant_id
        self.sort_key = u"CreatedAt"

    def __str__(self):
        groups_string = u",".join(str(group_item) for group_item in self._filter_group_list)
        json = u'{{"tenantId":"{0}", "groupClause":"{1}", "groups":[{2}], "pgNum":{3}, "pgSize":{4}, "srtDir":"{5}", "srtKey":"{6}"}}'.format(
            self._tenant_id,
            self._group_clause,
            groups_string,
            self.page_number,
            self.page_size,
            self.sort_direction,
            self.sort_key,
        )
        return json


class AlertQueryFactory(object):
    _tenant_id = None

    def __init__(self, administration_client):
        # type: (AlertQueryFactory, AdministrationClient) -> None
        self._administration = administration_client

    def create_alert_for_current_tenant(self, *args, **kwargs):
        tenant_id = self._get_current_tenant_id()
        return AlertQuery(tenant_id, *args, **kwargs)

    def _get_current_tenant_id(self):
        if self._tenant_id is None:
            response = self._administration.get_current_tenant()
            tenant = get_obj_from_response(response, u"data")
            self._tenant_id = tenant.get(u"tenantUid")
        return self._tenant_id
