from py42._internal.compat import str
from py42.sdk.queries import BaseQuery
from py42.sdk.queries.query_filter import (
    QueryFilterStringField,
    create_filter_group,
    create_query_filter,
)


class FileEventQuery(BaseQuery):
    def __init__(self, *args, **kwargs):
        super(FileEventQuery, self).__init__(*args, **kwargs)
        self.sort_key = u"eventId"
        self.page_number = 1

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


def create_exists_filter_group(term):
    filter_list = [create_query_filter(term, u"EXISTS")]
    return create_filter_group(filter_list, u"AND")


def create_not_exists_filter_group(term):
    filter_list = [create_query_filter(term, u"DOES_NOT_EXIST")]
    return create_filter_group(filter_list, u"AND")


class FileEventFilterStringField(QueryFilterStringField):
    @classmethod
    def exists(cls):
        return create_exists_filter_group(cls._term)

    @classmethod
    def not_exists(cls):
        return create_not_exists_filter_group(cls._term)
