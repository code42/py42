from py42.sdk.queries.fileevents.file_event_query import FileEventFilterStringField


class UserEmail(FileEventFilterStringField):
    """Class that filters events by the Code42 user email of the actor."""

    _term = "user.email"


class UserId(FileEventFilterStringField):
    """Class that filters events by the Code42 user ID of the actor."""

    _term = "user.id"
