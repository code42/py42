from py42._internal.compat import str


class Py42Error(Exception):
    """A generic, Py42 custom base exception."""


class Py42ArchiveFileNotFoundError(Py42Error):
    """An exception raised when a resource file is not found or the path is invalid."""

    def __init__(self, device_guid, file_path):
        message = u"File not found in archive " u"for device {0} at path {1}".format(
            device_guid, file_path
        )
        super(Py42ArchiveFileNotFoundError, self).__init__(message)


class Py42FeatureUnavailableError(Py42Error):
    """An exception raised when a requested feature is not supported in your Code42 environment."""

    def __init__(self):
        super(Py42FeatureUnavailableError, self).__init__(
            u"You may be trying to use a feature that is unavailable in your environment."
        )


class Py42SessionInitializationError(Py42Error):
    """An exception raised when a user session is invalid. A session might be invalid due to
    session timeout, invalid token, etc.
    """

    def __init__(self, exception):
        error_message = (
            u"An error occurred while requesting "
            u"server environment information, caused by {0}".format(str(exception))
        )
        super(Py42SessionInitializationError, self).__init__(error_message)


class Py42SecurityPlanConnectionError(Py42Error):
    """An exception raised when the user is not authorized to access the requested resource."""

    def __init__(self, error_message):
        super(Py42SecurityPlanConnectionError, self).__init__(error_message)


class Py42StorageSessionInitializationError(Py42Error):
    """An exception raised when the user is not authorized to initialize a storage session. This
    may occur when trying to restore a file or trying to get events for file activity on removable
    media, in cloud sync folders, and browser uploads."""

    def __init__(self, error_message):
        super(Py42StorageSessionInitializationError, self).__init__(error_message)


class Py42HTTPError(Py42Error):
    """A base custom class to manage all HTTP errors raised by an API endpoint."""

    def __init__(self, exception):
        message = u"Failure in HTTP call {0}".format(str(exception))
        super(Py42HTTPError, self).__init__(message)
        self._response = exception.response

    @property
    def response(self):
        """The response object containing the HTTP error details."""
        return self._response


class Py42BadRequestError(Py42HTTPError):
    """A wrapper to represent an HTTP 400 error."""

    def __init__(self, exception):
        super(Py42BadRequestError, self).__init__(exception)


class Py42UnauthorizedError(Py42HTTPError):
    """A wrapper to represent an HTTP 401 error."""

    def __init__(self, exception):
        super(Py42UnauthorizedError, self).__init__(exception)


class Py42ForbiddenError(Py42HTTPError):
    """A wrapper to represent an HTTP 403 error."""

    def __init__(self, exception):
        super(Py42ForbiddenError, self).__init__(exception)


class Py42NotFoundError(Py42HTTPError):
    """A wrapper to represent an HTTP 404 error."""

    def __init__(self, exception):
        super(Py42NotFoundError, self).__init__(exception)


class Py42InternalServerError(Py42HTTPError):
    """A wrapper to represent an HTTP 500 error."""

    def __init__(self, exception):
        super(Py42InternalServerError, self).__init__(exception)


def raise_py42_error(raised_error):
    """Raises the appropriate :class:`py42.exceptions.Py42HttpError` based on the given
    error's response status code.
    """
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
        raise Py42HTTPError(raised_error)
