import re

from py42._compat import str


class Py42Error(Exception):
    """A generic, Py42 custom base exception."""


class Py42ResponseError(Py42Error):
    """A base custom class to manage all errors raised because of an HTTP response."""

    def __init__(self, response, message):
        super(Py42ResponseError, self).__init__(message)
        self._response = response

    @property
    def response(self):
        """The response prior to the error."""
        return self._response


class Py42ArchiveFileNotFoundError(Py42ResponseError):
    """An exception raised when a resource file is not found or the path is invalid."""

    def __init__(self, response, device_guid, file_path):
        message = u"File not found in archive for device {} at path {}".format(
            device_guid, file_path
        )
        super(Py42ArchiveFileNotFoundError, self).__init__(response, message)


class Py42ChecksumNotFoundError(Py42ResponseError):
    """An exception raised when a user-supplied hash could not successfully locate its corresponding resource."""

    def __init__(self, response, checksum_name, checksum_value):
        message = u"No files found with {} checksum {}".format(
            checksum_name, checksum_value
        )
        super(Py42ChecksumNotFoundError, self).__init__(response, message)


class Py42FeatureUnavailableError(Py42ResponseError):
    """An exception raised when a requested feature is not supported in your Code42 environment."""

    def __init__(self, response):
        super(Py42FeatureUnavailableError, self).__init__(
            response,
            u"You may be trying to use a feature that is unavailable in your environment.",
        )


class Py42HTTPError(Py42ResponseError):
    """A base custom class to manage all HTTP errors raised by an API endpoint."""

    def __init__(self, exception, message=None):
        message = message or u"Failure in HTTP call {}".format(str(exception))
        super(Py42HTTPError, self).__init__(exception.response, message)


class Py42SecurityPlanConnectionError(Py42HTTPError):
    """An exception raised when the user is not authorized to access the requested resource."""

    def __init__(self, exception, error_message):
        super(Py42SecurityPlanConnectionError, self).__init__(exception, error_message)


class Py42DeviceNotConnectedError(Py42ResponseError):
    """An exception raised when trying to push a restore to a device that is not
    connected to an Authority server."""

    def __init__(self, response, device_guid):
        message = (
            u"Device with GUID '{}' is not currently connected to the Authority "
            u"server.".format(device_guid)
        )
        super(Py42DeviceNotConnectedError, self).__init__(response, message)


class Py42InvalidArchivePassword(Py42HTTPError):
    """An exception raised when the password for unlocking an archive is invalid."""

    def __init__(self, exception):
        message = "Invalid archive password."
        super(Py42InvalidArchivePassword, self).__init__(exception, message)


class Py42InvalidArchiveEncryptionKey(Py42HTTPError):
    """An exception raised the encryption key for an archive is invalid."""

    def __init__(self, exception):
        message = "Invalid archive encryption key."
        super(Py42InvalidArchiveEncryptionKey, self).__init__(exception, message)


class Py42StorageSessionInitializationError(Py42HTTPError):
    """An exception raised when the user is not authorized to initialize a storage session. This
    may occur when trying to restore a file or trying to get events for file activity on removable
    media, in cloud sync folders, and browser uploads."""

    def __init__(self, exception, error_message):
        super(Py42StorageSessionInitializationError, self).__init__(
            exception, error_message
        )


class Py42SessionInitializationError(Py42Error):
    """An exception raised when a user connection is invalid. A connection might be invalid due to
    connection timeout, invalid token, etc.
    """

    def __init__(self, exception):
        error_message = (
            u"An error occurred while requesting "
            u"server environment information, caused by {}".format(str(exception))
        )
        super(Py42SessionInitializationError, self).__init__(exception, error_message)


class Py42BadRequestError(Py42HTTPError):
    """A wrapper to represent an HTTP 400 error."""


class Py42UnauthorizedError(Py42HTTPError):
    """A wrapper to represent an HTTP 401 error."""


class Py42ForbiddenError(Py42HTTPError):
    """A wrapper to represent an HTTP 403 error."""


class Py42NotFoundError(Py42HTTPError):
    """A wrapper to represent an HTTP 404 error."""


class Py42InternalServerError(Py42HTTPError):
    """A wrapper to represent an HTTP 500 error."""


class Py42TooManyRequestsError(Py42HTTPError):
    """A wrapper to represent an HTTP 429 error."""


class Py42ActiveLegalHoldError(Py42BadRequestError):
    """An exception raised when attempting to deactivate a user or device that is in an
    active legal hold."""

    def __init__(self, exception, resource, resource_id):
        msg = u"Cannot deactivate the {0} with ID {1} as the {0} is involved in a legal hold matter.".format(
            resource, resource_id,
        )
        super(Py42ActiveLegalHoldError, self).__init__(exception, msg)


class Py42UserAlreadyAddedError(Py42BadRequestError):
    """An exception raised when the user is already added to group or list, such as the
    Departing Employee list."""

    def __init__(self, exception, user_id, list_name):
        msg = u"User with ID {} is already on the {}.".format(user_id, list_name)
        super(Py42UserAlreadyAddedError, self).__init__(exception, msg)


class Py42LegalHoldNotFoundOrPermissionDeniedError(Py42ForbiddenError):
    """An exception raised when a legal hold matter is inaccessible from your account or
    the matter ID is not valid."""

    def __init__(self, exception, matter_id):
        super(Py42LegalHoldNotFoundOrPermissionDeniedError, self).__init__(
            exception,
            u"Matter with ID={} can not be found. Your account may not have permission to view the matter.".format(
                matter_id
            ),
        )


class Py42InvalidRuleOperationError(Py42HTTPError):
    """An exception raised when trying to add or remove users to a system rule."""

    def __init__(self, exception, rule_id, source):
        msg = u"Only alert rules with a source of 'Alerting' can be targeted by this command. "
        msg += u"Rule {0} has a source of '{1}'."
        super(Py42InvalidRuleOperationError, self).__init__(
            exception, msg.format(rule_id, source)
        )


class Py42MFARequiredError(Py42UnauthorizedError):
    """An exception raised when a request requires multi-factor authentication"""

    def __init__(self, exception, message=None):
        message = message or u"User requires multi-factor authentication."
        super(Py42MFARequiredError, self).__init__(exception, message)


class Py42UserAlreadyExistsError(Py42InternalServerError):
    """An exception raised when a user already exists"""

    def __init__(self, exception, message=None):
        message = message or u"User already exists."
        super(Py42UserAlreadyExistsError, self).__init__(exception, message)


class Py42CloudAliasLimitExceededError(Py42BadRequestError):
    """An Exception raised when trying to add a cloud alias to a user when that user
    already has the max amount of supported cloud aliases."""

    def __init__(self, exception, message=None):
        message = message or u"Cloud alias limit exceeded."
        super(Py42BadRequestError, self).__init__(exception, message)


class Py42BadRestoreRequestError(Py42BadRequestError):
    """An error raised when the given restore arguments are not compatible and cause
    a bad request."""

    def __init__(self, exception):
        message = u"Unable to create restore session."
        super(Py42BadRestoreRequestError, self).__init__(exception, message)


class Py42InvalidPageTokenError(Py42BadRequestError):
    """An error raised when the page token given is invalid."""

    def __init__(self, exception, page_token):
        message = u"Invalid page token: {}".format(page_token)
        super(Py42InvalidPageTokenError, self).__init__(exception, message)


class Py42UserNotOnListError(Py42NotFoundError):
    """An exception raised when the user is not on a detection list."""

    def __init__(self, exception, user_id, list_name):
        message = u"User with ID '{}' is not currently on the {} list.".format(
            user_id, list_name
        )
        super(Py42NotFoundError, self).__init__(exception, message)


def raise_py42_error(raised_error):
    """Raises the appropriate :class:`py42.exceptions.Py42HttpError` based on the given
    HTTPError's response status code.
    """
    if raised_error.response.status_code == 400:
        raise Py42BadRequestError(raised_error)
    elif raised_error.response.status_code == 401:
        if raised_error.response.text and re.search(
            "(TOTP_AUTH_CONFIGURATION_REQUIRED_FOR_USER|TIME_BASED_ONE_TIME_PASSWORD_REQUIRED)",
            raised_error.response.text,
        ):
            raise Py42MFARequiredError(raised_error)
        raise Py42UnauthorizedError(raised_error)
    elif raised_error.response.status_code == 403:
        raise Py42ForbiddenError(raised_error)
    elif raised_error.response.status_code == 404:
        raise Py42NotFoundError(raised_error)
    elif raised_error.response.status_code == 429:
        raise Py42TooManyRequestsError(raised_error)
    elif 500 <= raised_error.response.status_code < 600:
        raise Py42InternalServerError(raised_error)
    else:
        raise Py42HTTPError(raised_error)
