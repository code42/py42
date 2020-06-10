from py42._internal.compat import str
from py42.sdk.queries import BaseQuery


class AlertQuery(BaseQuery):
    """Helper class for building Code42 Alert queries.

    An AlertQuery instance's ``all()`` and ``any()`` take one or more :class:`FilterGroup`
    objects to construct a query that can be passed to the :meth:`AlertClient.search()` method.
    ``all()`` returns results that match all of the provided filter criteria, ``any()`` will return
    results that match any of the filters.

    For convenience, the :class:`AlertQuery` constructor does the same as ``all()``.

    Usage example::

        state_filter = AlertState.eq(AlertState.OPEN)
        rule_name_filter = RuleName.contains("EmailRule")
        query = AlertQuery.all(state_filter, rule_name_filter)
    """

    def __init__(self, *args, **kwargs):
        super(AlertQuery, self).__init__(*args, **kwargs)
        self.sort_key = u"CreatedAt"
        self.page_number = 0
        self.page_size = 500
        self.sort_direction = u"desc"

    def __str__(self):
        groups_string = u",".join(str(group_item) for group_item in self._filter_group_list)
        json = u'{{"tenantId": null, "groupClause":"{0}", "groups":[{1}], "pgNum":{2}, "pgSize":{3}, "srtDirection":"{4}", "srtKey":"{5}"}}'.format(
            self._group_clause,
            groups_string,
            self.page_number,
            self.page_size,
            self.sort_direction,
            self.sort_key,
        )
        return json

    def __iter__(self):
        filter_group_list = [dict(item) for item in self._filter_group_list]
        output_dict = {
            u"tenantId": None,
            u"groupClause": self._group_clause,
            u"groups": filter_group_list,
            u"pgNum": self.page_number,
            u"pgSize": self.page_size,
            u"srtDirection": self.sort_direction,
            u"srtKey": self.sort_key,
        }
        for key in output_dict:
            yield (key, output_dict[key])
