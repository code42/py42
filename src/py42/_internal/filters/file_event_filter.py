from py42._internal.filters.query_filter import (
    create_query_filter,
    create_filter_group,
    _QueryFilterStringField,
)


def create_exists_filter_group(term):
    filter_list = [create_query_filter(term, u"EXISTS")]
    return create_filter_group(filter_list, u"AND")


def create_not_exists_filter_group(term):
    filter_list = [create_query_filter(term, u"DOES_NOT_EXIST")]
    return create_filter_group(filter_list, u"AND")


class _FileEventFilterStringField(_QueryFilterStringField):
    @classmethod
    def exists(cls):
        return create_exists_filter_group(cls._term)

    @classmethod
    def not_exists(cls):
        return create_not_exists_filter_group(cls._term)
