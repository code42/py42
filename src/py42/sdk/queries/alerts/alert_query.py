from py42.sdk.queries import BaseQuery


class AlertQuery(BaseQuery):
    """Helper class for building Code42 Alert queries.

    An AlertQuery instance's ``all()`` and ``any()`` take one or more
    :class:`~py42.sdk.queries.query_filter.FilterGroup` objects to construct a query that
    can be passed to the :meth:`AlertService.search()` method. ``all()`` returns results
    that match all of the provided filter criteria, ``any()`` will return results that
    match any of the filters.

    For convenience, the :class:`AlertQuery` constructor does the same as ``all()``.

    Usage example::

        state_filter = AlertState.eq(AlertState.OPEN)
        rule_name_filter = RuleName.contains("EmailRule")
        query = AlertQuery.all(state_filter, rule_name_filter)
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.sort_key = "CreatedAt"
        self.page_number = 0
        self.page_size = 500
        self.sort_direction = "desc"

    def __str__(self):
        groups_string = ",".join(
            str(group_item) for group_item in self._filter_group_list
        )
        json = (
            f'{{"tenantId": null, "groupClause":"{self._group_clause}", "groups":[{groups_string}], "pgNum":{self.page_number}, '
            f'"pgSize":{self.page_size}, "srtDirection":"{self.sort_direction}", "srtKey":"{self.sort_key}"}}'
        )
        return json

    def __iter__(self):
        filter_group_list = [dict(item) for item in self._filter_group_list]
        output_dict = {
            "tenantId": None,
            "groupClause": self._group_clause,
            "groups": filter_group_list,
            "pgNum": self.page_number,
            "pgSize": self.page_size,
            "srtDirection": self.sort_direction,
            "srtKey": self.sort_key,
        }
        for key in output_dict:
            yield key, output_dict[key]
