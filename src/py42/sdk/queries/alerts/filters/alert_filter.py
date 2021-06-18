from py42.sdk.queries.query_filter import create_filter_group
from py42.sdk.queries.query_filter import create_query_filter
from py42.sdk.queries.query_filter import QueryFilterStringField
from py42.sdk.queries.query_filter import QueryFilterTimestampField
from py42.util import get_attribute_keys_from_class
from py42.util import MICROSECOND_FORMAT
from py42.util import parse_timestamp_to_microseconds_precision


def create_contains_filter_group(term, value):
    """Creates a :class:`~py42.sdk.queries.query_filter.FilterGroup` for filtering results
    where the value with key ``term`` contains the given value. Useful for creating ``CONTAINS``
    filters that are not yet supported in py42 or programmatically crafting filter groups.

    Args:
        term: (str): The term of the filter, such as ``actor``.
        value (str): The value used to match on.

    Returns:
        :class:`~py42.sdk.queries.query_filter.FilterGroup`
    """

    filter_list = [create_query_filter(term, u"CONTAINS", value)]
    return create_filter_group(filter_list, u"AND")


def create_not_contains_filter_group(term, value):
    """Creates a :class:`~py42.sdk.queries.query_filter.FilterGroup` for filtering results
    where the value with key ``term`` does not contain the given value. Useful for creating
    ``DOES_NOT_CONTAIN`` filters that are not yet supported in py42 or programmatically
    crafting filter groups.

    Args:
        term: (str): The term of the filter, such as ``actor``.
        value (str): The value used to exclude on.

    Returns:
        :class:`~py42.sdk.queries.query_filter.FilterGroup`
    """

    filter_list = [create_query_filter(term, u"DOES_NOT_CONTAIN", value)]
    return create_filter_group(filter_list, u"AND")


class AlertQueryFilterStringField(QueryFilterStringField):
    @classmethod
    def contains(cls, value):
        """Creates a :class:`~py42.sdk.queries.query_filter.FilterGroup` for filtering
        results where the value with key ``self._term`` contains the given value. Useful
        for creating ``CONTAINS`` filters that are not yet supported in py42 or programmatically
        crafting filter groups.

        Args:
            value (str): The value used to match on.

        Returns:
            :class:`~py42.sdk.queries.query_filter.FilterGroup`
        """

        return create_contains_filter_group(cls._term, value)

    @classmethod
    def not_contains(cls, value):
        """Creates a :class:`~py42.sdk.queries.query_filter.FilterGroup` for filtering
        results where the value with key ``self._term`` does not contain the given value.
        Useful for creating ``DOES_NOT_CONTAIN`` filters that are not yet supported in py42
        or programmatically crafting filter groups.

        Args:
            value (str): The value used to exclude on.

        Returns:
            :class:`~py42.sdk.queries.query_filter.FilterGroup`
        """

        return create_not_contains_filter_group(cls._term, value)


class AlertQueryFilterTimestampField(QueryFilterTimestampField):
    """Helper class for creating alert filters where the search value is a timestamp."""

    @staticmethod
    def _parse_timestamp(value):
        return parse_timestamp_to_microseconds_precision(value)

    @staticmethod
    def _convert_datetime_to_timestamp(value):
        return value.strftime(MICROSECOND_FORMAT)


class DateObserved(AlertQueryFilterTimestampField):
    """Class that filters alerts based on the timestamp the alert was triggered."""

    _term = u"createdAt"


class Actor(AlertQueryFilterStringField):
    """Class that filters alerts based on the username that originated the event(s) that
    triggered the alert."""

    _term = u"actor"


class RuleName(AlertQueryFilterStringField):
    """Class that filters alerts based on rule name."""

    _term = u"name"


class RuleId(QueryFilterStringField):
    """Class that filters alerts based on rule identifier."""

    _term = u"ruleId"


class RuleSource(QueryFilterStringField):
    """Class that filters alerts based on rule source.

    Available options are:
        - :attr:`RuleSource.ALERTING`
        - :attr:`RuleSource.DEPARTING_EMPLOYEE`
        - :attr:`RuleSource.HIGH_RISK_EMPLOYEE`
    """

    _term = u"ruleSource"

    ALERTING = u"Alerting"
    DEPARTING_EMPLOYEE = u"Departing Employee"
    HIGH_RISK_EMPLOYEE = u"High Risk Employee"

    @staticmethod
    def choices():
        return get_attribute_keys_from_class(RuleSource)


class RuleType(QueryFilterStringField):
    """Class that filters alerts based on rule type.

    Available options are:
        - :attr:`RuleType.ENDPOINT_EXFILTRATION`
        - :attr:`RuleType.CLOUD_SHARE_PERMISSIONS`
        - :attr:`RuleType.FILE_TYPE_MISMATCH`
    """

    _term = u"type"

    ENDPOINT_EXFILTRATION = u"FedEndpointExfiltration"
    CLOUD_SHARE_PERMISSIONS = u"FedCloudSharePermissions"
    FILE_TYPE_MISMATCH = u"FedFileTypeMismatch"

    @staticmethod
    def choices():
        return get_attribute_keys_from_class(RuleType)


class Description(AlertQueryFilterStringField):
    """Class that filters alerts based on rule description text."""

    _term = u"description"


class Severity(QueryFilterStringField):
    """Class that filters alerts based on severity.

    Available options are:
        - :attr:`Severity.HIGH`
        - :attr:`Severity.MEDIUM`
        - :attr:`Severity.LOW`
    """

    _term = u"severity"

    HIGH = u"HIGH"
    MEDIUM = u"MEDIUM"
    LOW = u"LOW"

    @staticmethod
    def choices():
        return get_attribute_keys_from_class(Severity)


class AlertState(QueryFilterStringField):
    """Class that filters alerts based on alert state.

    Available options are:
        - :attr:`AlertState.OPEN`
        - :attr:`AlertState.DISMISSED`
        - :attr:`AlertState.PENDING`
        - :attr:`AlertState.IN_PROGRESS`
    """

    _term = u"state"

    OPEN = u"OPEN"
    DISMISSED = u"RESOLVED"
    PENDING = u"PENDING"
    IN_PROGRESS = u"IN_PROGRESS"

    @staticmethod
    def choices():
        return get_attribute_keys_from_class(AlertState)
