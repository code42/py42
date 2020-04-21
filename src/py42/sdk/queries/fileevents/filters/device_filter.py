from py42.sdk.queries.fileevents.file_event_query import FileEventFilterStringField


class DeviceUsername(FileEventFilterStringField):
    """Class that filters events by the Code42 username of the device that observed the event."""

    _term = u"deviceUserName"


class OSHostname(FileEventFilterStringField):
    """Class that filters events by hostname of the device that observed the event."""

    _term = u"osHostName"


class PrivateIPAddress(FileEventFilterStringField):
    """Class that filters events by private (LAN) IP address of the device that observed the event."""

    _term = u"privateIpAddresses"


class PublicIPAddress(FileEventFilterStringField):
    """Class that filters events by public (WAN) IP address of the device that observed the event."""

    _term = u"publicIpAddress"
