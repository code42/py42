from py42._internal.compat import str


class Py42Error(Exception):
    """A generic, Py42 custom base exception."""


class Py42ArchiveFileNotFoundError(Py42Error):
    """An exception raised when a resource file is not found or the path is invalid."""

    def __init__(self, device_guid, file_path):
        message = u"File not found in archive for device {} at path {}".format(
            device_guid, file_path
        )
        super(Py42ArchiveFileNotFoundError, self).__init__(message)


class Py42ChecksumNotFoundError(Py42Error):
    """An exception raised when a user-supplied hash could not successfully locate its corresponding resource."""

    def __init__(self, checksum_name, checksum_value):
        message = u"No files found with {} checksum {}".format(
            checksum_name, checksum_value
        )
        super(Py42ChecksumNotFoundError, self).__init__(message)


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
            u"server environment information, caused by {}".format(str(exception))
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


class Py42UserAlreadyAddedError(Py42Error):
    def __init__(self, user_id, list_name):
        msg = u"User with ID {} is already on the {}.".format(user_id, list_name)
        super().__init__(msg)


class Py42UserNotInLegalHoldError(Py42Error):
    def __init__(self, username, matter_id):
        super().__init__(
            u"{} is not an active member of legal hold matter '{}'".format(
                username, matter_id
            )
        )


class Py42LegalHoldNotFoundOrPermissionDeniedError(Py42Error):
    def __init__(self, matter_id):
        super().__init__(
            u"Matter with id={} either does not exist or your profile does not have permission to "
            u"view it.".format(matter_id)
        )


class Py42UserDoesNotExistError(Py42Error):
    """An error to represent a username that is not in our system. The CLI shows this error when
    the user tries to add or remove a user that does not exist. This error is not shown during
    bulk add or remove."""

    def __init__(self, username):
        super().__init__(u"User '{}' does not exist.".format(username))


class Py42InvalidRuleTypeError(Py42Error):
    def __init__(self, rule_id, source):
        msg = u"Only alert rules with a source of 'Alerting' can be targeted by this command. "
        msg += u"Rule {0} has a source of '{1}'."
        super().__init__(msg.format(rule_id, source))


class Py42HTTPError(Py42Error):
    """A base custom class to manage all HTTP errors raised by an API endpoint."""

    def __init__(self, exception):
        message = u"Failure in HTTP call {}".format(str(exception))
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
