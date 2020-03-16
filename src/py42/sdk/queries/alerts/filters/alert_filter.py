from py42.sdk.queries.query_filter import (
    QueryFilterStringField,
    create_filter_group,
    create_query_filter,
)


def create_contains_filter_group(term, value):
    filter_list = [create_query_filter(term, u"CONTAINS", value)]
    return create_filter_group(filter_list, u"AND")


def create_not_contains_filter_group(term, value):
    filter_list = [create_query_filter(term, u"DOES_NOT_CONTAIN", value)]
    return create_filter_group(filter_list, u"AND")


class AlertQueryFilterStringField(QueryFilterStringField):
    @classmethod
    def contains(cls, value):
        return create_contains_filter_group(cls._term, value)

    @classmethod
    def not_contains(cls, value):
        return create_not_contains_filter_group(cls._term, value)
