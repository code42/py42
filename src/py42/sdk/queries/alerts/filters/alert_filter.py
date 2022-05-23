from py42.choices import Choices as _Choices
from py42.sdk.queries.alerts.util import (
    AlertQueryFilterStringField as _AlertQueryFilterStringField,
)
from py42.sdk.queries.alerts.util import (
    AlertQueryFilterTimestampField as _AlertQueryFilterTimestampField,
)
from py42.sdk.queries.query_filter import (
    QueryFilterStringField as _QueryFilterStringField,
)


class DateObserved(_AlertQueryFilterTimestampField):
    """Class that filters alerts based on the timestamp the alert was triggered."""

    _term = "createdAt"


class Actor(_AlertQueryFilterStringField):
    """Class that filters alerts based on the username that originated the event(s) that
    triggered the alert."""

    _term = "actor"


class RuleName(_AlertQueryFilterStringField):
    """Class that filters alerts based on rule name."""

    _term = "name"


class RuleId(_QueryFilterStringField):
    """Class that filters alerts based on rule identifier."""

    _term = "ruleId"


class RuleSource(_QueryFilterStringField, _Choices):
    """Class that filters alerts based on rule source.

    Available options are:
        - :attr:`RuleSource.ALERTING`
        - :attr:`RuleSource.DEPARTING_EMPLOYEE`
        - :attr:`RuleSource.HIGH_RISK_EMPLOYEE`
    """

    _term = "ruleSource"

    ALERTING = "Alerting"
    DEPARTING_EMPLOYEE = "Departing Employee"
    HIGH_RISK_EMPLOYEE = "High Risk Employee"


class RuleType(_QueryFilterStringField, _Choices):
    """Class that filters alerts based on rule type.

    Available options are:
        - :attr:`RuleType.ENDPOINT_EXFILTRATION`
        - :attr:`RuleType.CLOUD_SHARE_PERMISSIONS`
        - :attr:`RuleType.FILE_TYPE_MISMATCH`
    """

    _term = "type"

    ENDPOINT_EXFILTRATION = "FedEndpointExfiltration"
    CLOUD_SHARE_PERMISSIONS = "FedCloudSharePermissions"
    FILE_TYPE_MISMATCH = "FedFileTypeMismatch"


class Description(_AlertQueryFilterStringField):
    """Class that filters alerts based on rule description text."""

    _term = "description"


class Severity(_QueryFilterStringField, _Choices):
    """Class that filters alerts based on severity.

    Available options are:
        - :attr:`Severity.CRITICAL`
        - :attr:`Severity.HIGH`
        - :attr:`Severity.MODERATE`
        - :attr:`Severity.LOW`
    """

    _term = "riskSeverity"

    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MODERATE"
    MODERATE = "MODERATE"
    LOW = "LOW"


class AlertState(_QueryFilterStringField, _Choices):
    """Class that filters alerts based on alert state.

    Available options are:
        - :attr:`AlertState.OPEN`
        - :attr:`AlertState.DISMISSED`
        - :attr:`AlertState.PENDING`
        - :attr:`AlertState.IN_PROGRESS`
    """

    _term = "state"

    OPEN = "OPEN"
    DISMISSED = "RESOLVED"
    PENDING = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"
