from py42._internal.filters.query_filter import create_query_filter, create_filter_group, _QueryFilterStringField



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
