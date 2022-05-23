from py42.sdk.queries.query_filter import (
    QueryFilterStringField as _QueryFilterStringField,
)


class EmailPolicyName(_QueryFilterStringField):
    """V1 filter class that filters events based on the email DLP policy that detected this file (applies to
    emails sent via Microsoft Office 365 only).
    """

    _term = "emailDlpPolicyNames"


class EmailSubject(_QueryFilterStringField):
    """V1 filter class that filters events based on the email's subject (applies to email events only)."""

    _term = "emailSubject"


class EmailRecipients(_QueryFilterStringField):
    """V1 filter class that filters events based on the email's recipient list (applies to email events only)."""

    _term = "emailRecipients"


class EmailSender(_QueryFilterStringField):
    """V1 filter class that filters events based on the email's sender (applies to email events only)."""

    _term = "emailSender"


class EmailFrom(_QueryFilterStringField):
    """V1 filter class that filters events based on the display name of the email's sender, as it appears in
    the \"From:\" field in the email (applies to email events only).
    """

    _term = "emailFrom"
