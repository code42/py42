from py42.sdk.queries.fileevents.file_event_query import FileEventFilterStringField


class EmailRecipients(FileEventFilterStringField):
    """Class that filters events based on the email's recipient list (applies to email events only)."""

    _term = u"emailRecipients"


class EmailSender(FileEventFilterStringField):
    """Class that filters events based on the email's sender (applies to email events only)."""

    _term = u"emailSender"
