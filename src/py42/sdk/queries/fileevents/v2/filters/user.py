from py42.sdk.queries.fileevents.util import (
    FileEventFilterStringField as _FileEventFilterStringField,
)


class Email(_FileEventFilterStringField):
    """V2 filter class that filters events by the Code42 user email of the actor."""

    _term = "user.email"


class Id(_FileEventFilterStringField):
    """V2 filter class that filters events by the Code42 user ID of the actor."""

    _term = "user.id"


class DeviceUid(_FileEventFilterStringField):
    """V2 filter class that filters events by the device UID of the actor."""

    _term = "user.deviceUid"
