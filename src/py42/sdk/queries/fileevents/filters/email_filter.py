from py42.sdk.queries.fileevents.file_event_query import FileEventFilterStringField


class EmailRecipients(FileEventFilterStringField):
    """Class that filters events based on the email recipients involved in the email exposure."""

    _term = u"emailRecipients"


class EmailSender(FileEventFilterStringField):
    """Class that filters events based on the email sender involved in the email exposure."""

    _term = u"emailSender"
