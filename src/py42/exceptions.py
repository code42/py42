from py42._internal.compat import str


class Py42Exception(Exception):
    """A generic, Py42-specific exception."""


class Py42InitializationError(Py42Exception):
    def __init__(self, host_address):
        self.host_address = host_address
        super(Py42InitializationError, self).__init__(self._message)

    @property
    def _message(self):
        return (
            u"Invalid credentials or host address ({0}). Check that the username and password are correct, that the "
            u"host is available and reachable, and that you have supplied the full scheme, domain, and port "
            u"(e.g. https://myhost.code42.com:4285). If you are using a self-signed ssl certificate, try setting "
            u"py42.settings.verify_ssl_certs to false (or using a cert from a legitimate certificate "
            u"authority).".format(self.host_address)
        )


class UnauthorizedError(Py42Exception):
    def __init__(self, request_uri):
        self.request_uri = request_uri
        message = "You are not authorized to make this request to {0}.".format(request_uri)
        super(UnauthorizedError, self).__init__(message)


class Py42RequestException(Py42Exception):
    def __init__(self, message, base_exception):
        self.base_exception = base_exception
        super(Py42RequestException, self).__init__(
            u"{0}, caused by {1}".format(message, str(base_exception))
        )


class ArchiveFileNotFoundException(Py42Exception):
    def __init__(self, device_guid, file_path):
        self.device_guide = device_guid
        self.file_path = file_path
        super(ArchiveFileNotFoundException, self).__init__()
