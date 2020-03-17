class Py42Error(Exception):
    """A generic, Py42-specific exception."""


class Py42InitializationError(Py42Error):
    def __init__(self, host_address, error):
        self.host_address = host_address
        self.error = str(error)
        super(Py42InitializationError, self).__init__(self._message)

    @property
    def _message(self):
        return (
            u"Invalid credentials or host address ({0}). Check that the username and password are correct, that the "
            u"host is available and reachable, and that you have supplied the full scheme, domain, and port "
            u"(e.g. https://myhost.code42.com:4285). If you are using a self-signed ssl certificate, try setting "
            u"py42.settings.verify_ssl_certs to false (or using a cert from a legitimate certificate "
            u"authority). \n Failed with error {1} ".format(self.host_address, self.error)
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


class Py42SessionInitializationError(Py42Error):
    def __init__(self, exception):
        error_message = (
            u"An error occurred while requesting "
            u"server environment information, caused by {0}".format(str(exception))
        )
        super(Py42SessionInitializationError, self).__init__(error_message)


class Py42BadRequestError(Py42Error):
    def __init__(self, exception):
        super(Py42BadRequestError, self).__init__(str(exception))


class Py42UnauthorizedError(Py42Error):
    def __init__(self, exception):
        super(Py42UnauthorizedError, self).__init__(str(exception))


class Py42ForbiddenError(Py42Error):
    def __init__(self, exception):
        super(Py42ForbiddenError, self).__init__(str(exception))


class Py42NotFoundError(Py42Error):
    def __init__(self, exception):
        super(Py42NotFoundError, self).__init__(str(exception))


class Py42InternalServerError(Py42Error):
    def __init__(self, exception):
        super(Py42InternalServerError, self).__init__(str(exception))


def exception_checker(raised_error):

    if raised_error.response.status_code == 400:
        raise Py42BadRequestError(raised_error)
    elif raised_error.response.status_code == 401:
        raise Py42UnauthorizedError(raised_error)
    elif raised_error.response.status_code == 403:
        raise Py42ForbiddenError(raised_error)
    elif raised_error.response.status_code == 404:
        raise Py42NotFoundError(raised_error)
    elif 500 <= raised_error.response.status_code < 600:
        raise Py42InternalServerError(raised_error)
    else:
        raise raised_error
