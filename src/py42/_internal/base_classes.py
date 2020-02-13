from py42._internal.compat import str
from py42._internal.query_filter import FilterGroup


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
        self.page_number = 1
        self.page_size = 100
        self.sort_direction = u"asc"
        self.sort_key = u"eventId"

    def __str__(self):
        groups_string = u",".join(str(group_item) for group_item in self._filter_group_list)
        json = u'{{"groupClause":"{0}", "groups":[{1}], "pgNum":{2}, "pgSize":{3}, "srtDir":"{4}", "srtKey":"{5}"}}'.format(
            self._group_clause,
            groups_string,
            self.page_number,
            self.page_size,
            self.sort_direction,
            self.sort_key,
        )
        return json

    @classmethod
    def any(cls, *args):
        # type: (iter[FilterGroup]) -> BaseQuery
        return cls(*args, group_clause=u"OR")

    @classmethod
    def all(cls, *args):
        # type: (iter[FilterGroup]) -> BaseQuery
        return cls(*args)
