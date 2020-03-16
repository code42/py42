from py42.sdk.queries.fileevents.file_event_query import FileEventFilterStringField


class DeviceUsername(FileEventFilterStringField):
    _term = u"deviceUserName"


class OSHostname(FileEventFilterStringField):
    _term = u"osHostName"


class PrivateIPAddress(FileEventFilterStringField):
    _term = u"privateIpAddresses"


class PublicIPAddress(FileEventFilterStringField):
    _term = u"publicIpAddress"
