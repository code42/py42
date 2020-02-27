from py42._internal.compat import str
from py42._internal.base_classes import BaseQuery
from py42._internal.filters.query_filter import (
    _QueryFilterTimestampField,
    _QueryFilterStringField,
    FilterGroup,
)
from py42._internal.filters.alert_filter import _AlertQueryFilterStringField


class DateObserved(_QueryFilterTimestampField):
    _term = u"CreatedAt"


class Actor(_AlertQueryFilterStringField):
    _term = u"actor"


class RuleName(_AlertQueryFilterStringField):
    _term = u"name"


class Description(_AlertQueryFilterStringField):
    _term = u"description"


class Severity(_QueryFilterStringField):
    _term = u"severity"

    class SeverityTypeEnum(object):
        def __init__(self, value):
            self._value = value

        def __repr__(self):
            return self._value

    HIGH = SeverityTypeEnum(u"HIGH")
    MEDIUM = SeverityTypeEnum(u"MEDIUM")
    LOW = SeverityTypeEnum(u"LOW")

    @classmethod
    def eq(cls, value):
        # type: (SeverityTypeEnum) -> FilterGroup
        return super(Severity, cls).eq(str(value))

    @classmethod
    def not_eq(cls, value):
        # type: (SeverityTypeEnum) -> FilterGroup
        return super(Severity, cls).not_eq(str(value))

    @classmethod
    def is_in(cls, value_list):
        # type: (iter[SeverityTypeEnum]) -> FilterGroup
        return super(Severity, cls).is_in([str(value) for value in value_list])

    @classmethod
    def not_in(cls, value_list):
        # type: (iter[SeverityTypeEnum]) -> FilterGroup
        return super(Severity, cls).not_in([str(value) for value in value_list])


class AlertState(_QueryFilterStringField):
    _term = u"state"

    class AlertStateTypeEnum(object):
        def __init__(self, value):
            self._value = value

        def __repr__(self):
            return self._value

    OPEN = AlertStateTypeEnum(u"OPEN")
    DISMISSED = AlertStateTypeEnum(u"RESOLVED")

    @classmethod
    def eq(cls, value):
        # type: (AlertStateTypeEnum) -> FilterGroup
        return super(AlertState, cls).eq(str(value))

    @classmethod
    def not_eq(cls, value):
        # type: (AlertStateTypeEnum) -> FilterGroup
        return super(AlertState, cls).not_eq(str(value))

    @classmethod
    def is_in(cls, value_list):
        # type: (iter[AlertStateTypeEnum]) -> FilterGroup
        return super(AlertState, cls).is_in([str(value) for value in value_list])

    @classmethod
    def not_in(cls, value_list):
        # type: (iter[AlertStateTypeEnum]) -> FilterGroup
        return super(AlertState, cls).not_in([str(value) for value in value_list])


class AlertQuery(BaseQuery):
    def __init__(self, tenant_id, *args, **kwargs):
        super(AlertQuery, self).__init__(*args, **kwargs)
        self._tenant_id = tenant_id
        self.sort_key = u"CreatedAt"
        self.page_number = 0
        self.sort_direction = u"desc"

    def __str__(self):
        groups_string = u",".join(str(group_item) for group_item in self._filter_group_list)
        json = u'{{"tenantId":"{0}", "groupClause":"{1}", "groups":[{2}], "pgNum":{3}, "pgSize":{4}, "srtDirection":"{5}", "srtKey":"{6}"}}'.format(
            self._tenant_id,
            self._group_clause,
            groups_string,
            self.page_number,
            self.page_size,
            self.sort_direction,
            self.sort_key,
        )
        return json
