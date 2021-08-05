from py42.sdk.queries.query_filter import QueryFilterStringField


class EmailPolicyName(QueryFilterStringField):
    """Class that filters events based on the email DLP policy that detected this file (applies to
    emails sent via Microsoft Office 365 only).
    """

    _term = "emailDlpPolicyNames"


class EmailSubject(QueryFilterStringField):
    """Class that filters events based on the email's subject (applies to email events only)."""

    _term = "emailSubject"


class EmailRecipients(QueryFilterStringField):
    """Class that filters events based on the email's recipient list (applies to email events only)."""

    _term = "emailRecipients"


class EmailSender(QueryFilterStringField):
    """Class that filters events based on the email's sender (applies to email events only)."""

    _term = "emailSender"


class EmailFrom(QueryFilterStringField):
    """Class that filters events based on the display name of the email's sender, as it appears in
    the \"From:\" field in the email (applies to email events only).
    """

    _term = "emailFrom"
