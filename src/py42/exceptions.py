from py42._internal.compat import str


class Py42InitializationException(Exception):
    def __init__(self, host_address):
        super(Py42InitializationException, self).__init__(self._message)
        self._host_address = host_address

    @property
    def _message(self):
        return (
            u"Invalid credentials or host address ({0}). Check that the username and password are correct, that the "
            u"host is available and reachable, and that you have supplied the full scheme, domain, and port "
            u"(e.g. https://myhost.code42.com:4285). If you are using a self-signed ssl certificate, try setting "
            u"py42.settings.verify_ssl_certs to false (or using a cert from a legitimate certificate "
            u"authority).".format(self._host_address)
        )


class ReauthorizationException(Exception):
    def __init__(self, base_exception):
        message = (
            u"An error occurred while trying to handle an unauthorized request, caused by: {0}"
        ).format(str(base_exception))
        super(ReauthorizationException, self).__init__(message)


class Py42RequestException(Exception):
    pass


class ArchiveFileNotFoundException(Exception):
    def __init__(self, device_guid, file_path):
        message = u"File not found in archive for device {0} at path {1}".format(
            device_guid, file_path
        )
        super(ArchiveFileNotFoundException, self).__init__(message)


class StorageLoginRetrievalException(Exception):
    def __init__(self, base_exception):
        message = (
            u"An error occurred while trying to retrieve storage logon info, caused by {0}"
        ).format(str(base_exception))
        super(StorageLoginRetrievalException, self).__init__(message)


class TokenRetrievalException(Exception):
    def __init__(self, token_type, base_exception):
        self.token_type = token_type
        message = u"An error occurred while trying to retrieve a {0}, caused by {0}"
        message = message.format(token_type, str(base_exception))
        super(TokenRetrievalException, self).__init__(message)
