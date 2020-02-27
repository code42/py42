from py42._internal.filters.query_filter import FilterGroup


class BaseClient(object):
    def __init__(self, default_session):
        self._default_session = default_session


class BaseAuthorityClient(BaseClient):
    def __init__(self, default_session, v3_required_session):
        super(BaseAuthorityClient, self).__init__(default_session)
        self._default_session = default_session
        self._v3_required_session = v3_required_session


class BaseQuery(object):
    def __init__(self, *args, **kwargs):
        # type: (iter[FilterGroup], any) -> None
        self._filter_group_list = list(args)
        self._group_clause = kwargs.get(u"group_clause", u"AND")
        self.page_size = 10000
        self.sort_direction = u"asc"

        # Override
        self.page_number = None
        self.sort_key = None

    @classmethod
    def any(cls, *args):
        # type: (iter[FilterGroup]) -> BaseQuery
        return cls(*args, group_clause=u"OR")

    @classmethod
    def all(cls, *args):
        # type: (iter[FilterGroup]) -> BaseQuery
        return cls(*args)
