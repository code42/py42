from py42.sdk.queries.fileevents.util import FileEventFilterStringField


class DeviceUsername(FileEventFilterStringField):
    """V1 filter class that filters events by the Code42 username of the device that observed the event."""

    _term = "deviceUserName"


class OSHostname(FileEventFilterStringField):
    """V1 filter class that filters events by hostname of the device that observed the event."""

    _term = "osHostName"


class PrivateIPAddress(FileEventFilterStringField):
    """V1 filter class that filters events by private (LAN) IP address of the device that observed the event."""

    _term = "privateIpAddresses"


class PublicIPAddress(FileEventFilterStringField):
    """V1 filter class that filters events by public (WAN) IP address of the device that observed the event."""

    _term = "publicIpAddress"


class DeviceSignedInUserName(FileEventFilterStringField):
    """V1 filter class that filters events by signed in user of the device that observed the event."""

    _term = "operatingSystemUser"
