class Py42Error(Exception):
    """A generic, Py42-specific exception."""


class Py42InitializationError(Py42Error):
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


class Py42AuthenticationError(Py42Error):
    def __init__(self, error_message):
        super(Py42AuthenticationError, self).__init__(error_message)


class Py42ArchiveFileNotFoundError(Py42Error):
    def __init__(self, device_guid, file_path):
        message = u"File not found in archive " u"for device {0} at path {1}".format(
            device_guid, file_path
        )
        super(Py42ArchiveFileNotFoundError, self).__init__(message)


class Py42FeatureUnavailableError(Py42Error):
    def __init__(self):
        super(Py42FeatureUnavailableError, self).__init__(
            u"You may be trying to use a feature that is unavailable in your environment."
        )


class Py42SecurityPlanConnectionError(Py42Error):
    def __init__(self, error_message):
        super(Py42SecurityPlanConnectionError, self).__init__(error_message)


class Py42StorageSessionInitializationError(Py42Error):
    def __init__(self, error_message):
        super(Py42StorageSessionInitializationError, self).__init__(error_message)


class Py42DestinationNotFoundError(Py42Error):
    def __init__(self, error_message):
        super(Py42DestinationNotFoundError, self).__init__(error_message)
