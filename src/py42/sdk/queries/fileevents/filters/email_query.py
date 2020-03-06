from py42._internal.filters.file_event_filter import _FileEventFilterStringField


class EmailRecipients(_FileEventFilterStringField):
    _term = u"emailRecipients"


class EmailSender(_FileEventFilterStringField):
    _term = u"emailSender"
