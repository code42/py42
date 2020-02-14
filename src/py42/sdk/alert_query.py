# -*- coding: utf-8 -*-

from py42._internal.compat import str
from py42._internal.base_classes import BaseQuery
from py42._internal.query_filter import (
    _QueryFilterStringField,
    _QueryFilterTimestampField,
    FilterGroup,
    create_query_filter,
    create_filter_group,
)


def create_contains_group(term, value):
    filter_list = [create_query_filter(term, u"CONTAINS", value)]
    return create_filter_group(filter_list, u"AND")


def create_not_contains_group(term, value):
    filter_list = [create_query_filter(term, u"DOES_NOT_CONTAIN", value)]
    return create_filter_group(filter_list, u"AND")


class _AlertQueryFilterStringField(_QueryFilterStringField):
    @classmethod
    def contains(cls, value):
        # type: (str) -> FilterGroup
        return create_contains_group(cls._term, value)


class DateObserved(_QueryFilterTimestampField):
    _term = u"CreatedAt"


class Actor(_AlertQueryFilterStringField):
    _term = u"actor"


class Severity(_AlertQueryFilterStringField):
    _term = u"severity"


class RuleName(_AlertQueryFilterStringField):
    _term = u"name"


class Description(_AlertQueryFilterStringField):
    _term = u"description"


class AlertState(_AlertQueryFilterStringField):
    _term = u"State"


class AlertQuery(BaseQuery):
    def __init__(self, tenant_id, *args, **kwargs):
        super(AlertQuery, self).__init__(*args, **kwargs)
        self._tenant_id = tenant_id
        self.sort_key = u"CreatedAt"

        # For alerts, page numbers begin at 0, counter to file event queries
        self.page_number = 0

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
    """Abstracts away having to get the tenant ID when creating queries"""

    _tenant_id = None

    def __init__(self, administration_client):
        self._administration = administration_client

    def create_query_for_current_tenant(self, *args, **kwargs):
        tenant_id = self._get_current_tenant_id()
        return AlertQuery(tenant_id, *args, **kwargs)

    def _get_current_tenant_id(self):
        if self._tenant_id is None:
            self._tenant_id = self._administration.get_current_tenant_id()
        return self._tenant_id
