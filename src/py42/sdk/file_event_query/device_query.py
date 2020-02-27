from py42._internal.filters.file_event_filter import _FileEventFilterStringField


class DeviceUsername(_FileEventFilterStringField):
    _term = u"deviceUserName"


class OSHostname(_FileEventFilterStringField):
    _term = u"osHostName"


class PrivateIPAddress(_FileEventFilterStringField):
    _term = u"privateIpAddresses"


class PublicIPAddress(_FileEventFilterStringField):
    _term = u"publicIpAddress"
