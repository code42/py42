from py42._internal.compat import str
from py42.sdk.queries import BaseQuery


class AlertQuery(BaseQuery):
    """Helper class for building Code42 Alert queries.

    An AlertQuery instance's ``all()`` and ``any()`` take one or more :class:`FilterGroup`
    objects to construct a query that can be passed to the :meth:`AlertClient.search()` method.
    ``all()`` returns results that match all of the provided filter criteria, ``any()`` will return
    results that match any of the filters.

    For convenience, the :class:`AlertQuery` constructor does the same as ``all()``.

    A tenant ID is required in either the constructor or ``all()`` or ``any()``. You can get the
    tenant ID from the method :meth:`SDKClient.usercontext.get_current_tenant_id()`.

    Usage example:::
        state_filter = AlertState.eq(AlertState.OPEN)
        rule_name_filter = RuleName.contains("EmailRule")
        tenant_id = sdk.usercontext.get_current_tenant_id()
        query = AlertQuery(tenant_id).all(state_filter, rule_name_filter)
    """

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
