from py42.sdk.queries.query_filter import FilterGroup


class BaseQuery(object):
    def __init__(self, *args, **kwargs):
        self._filter_group_list = list(args)
        self._group_clause = kwargs.get(u"group_clause", u"AND")
        self.page_number = kwargs.get(u"page_number", 1)
        self.page_size = kwargs.get(u"page_size", 10000)
        self.sort_direction = u"asc"

        # Override
        self.sort_key = None

    @classmethod
    def from_dict(cls, _dict, group_clause=u"AND", **kwargs):
        filter_groups = [FilterGroup.from_dict(item) for item in _dict[u"groups"]]
        return cls(*filter_groups, group_clause=group_clause, **kwargs)

    @classmethod
    def any(cls, *args):
        return cls(*args, group_clause=u"OR")

    @classmethod
    def all(cls, *args):
        return cls(*args)
