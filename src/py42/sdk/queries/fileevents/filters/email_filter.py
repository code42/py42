from py42.sdk.queries.fileevents.file_event_query import FileEventFilterStringField


class EmailRecipients(FileEventFilterStringField):
    _term = u"emailRecipients"


class EmailSender(FileEventFilterStringField):
    _term = u"emailSender"
