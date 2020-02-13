from py42._internal.base_classes import BaseQuery
from py42._internal.query_filter import (
    _QueryFilterStringField,
    _QueryFilterTimestampField,
)


class DateObserved(_QueryFilterTimestampField):
    _term = u"CreatedAt"


class Actor(_QueryFilterStringField):
    _term = u"actor"


class Severity(_QueryFilterStringField):
    _term = u"severity"


class RuleName(_QueryFilterStringField):
    _term = u"name"


class Description(_QueryFilterStringField):
    _term = u"description"


class AlertState(_QueryFilterStringField):
    _term = u"State"


class AlertQuery(BaseQuery):
    pass
