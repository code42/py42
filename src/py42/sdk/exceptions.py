from py42._internal.compat import str


class Py42Error(Exception):
    """A generic, Py42-specific exception."""


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


class Py42SessionInitializationError(Py42Error):
    def __init__(self, exception):
        error_message = (
            u"An error occurred while requesting "
            u"server environment information, caused by {0}".format(str(exception))
        )
        super(Py42SessionInitializationError, self).__init__(error_message)


class Py42SecurityPlanConnectionError(Py42Error):
    def __init__(self, error_message):
        super(Py42SecurityPlanConnectionError, self).__init__(error_message)


class Py42StorageSessionInitializationError(Py42Error):
    def __init__(self, error_message):
        super(Py42StorageSessionInitializationError, self).__init__(error_message)


class Py42HTTPError(Py42Error):
    def __init__(self, http_response):
        message = u"Failure in HTTP call {0}".format(str(http_response))
        super(Py42HTTPError, self).__init__(message)
        self._response = http_response

    @property
    def response(self):
        return self._response


class Py42BadRequestError(Py42HTTPError):
    def __init__(self, exception):
        super(Py42BadRequestError, self).__init__(str(exception))


class Py42UnauthorizedError(Py42HTTPError):
    def __init__(self, exception):
        super(Py42UnauthorizedError, self).__init__(str(exception))


class Py42ForbiddenError(Py42HTTPError):
    def __init__(self, exception):
        super(Py42ForbiddenError, self).__init__(str(exception))


class Py42NotFoundError(Py42HTTPError):
    def __init__(self, exception):
        super(Py42NotFoundError, self).__init__(str(exception))


class Py42InternalServerError(Py42HTTPError):
    def __init__(self, exception):
        super(Py42InternalServerError, self).__init__(str(exception))


def raise_py42_error(raised_error):
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
        raise Py42HTTPError(raised_error.response)
