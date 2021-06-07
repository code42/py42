import re

from py42._compat import str
from py42.settings import debug


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
        if not message:
            response_content = "Response content: {}".format(exception.response.text)
            message = u"Failure in HTTP call {}. {}".format(
                str(exception), response_content
            )
            debug.logger.debug(message)

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


class Py42OrgNotFoundError(Py42BadRequestError):
    """An exception raised when a 400 HTTP error message indicates that an
    organization was not found."""

    def __init__(self, exception, org_uid):
        msg = u"The organization with UID '{}' was not found.".format(org_uid)
        super(Py42OrgNotFoundError, self).__init__(exception, msg)


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


class Py42LegalHoldCriteriaMissingError(Py42BadRequestError):
    """An exception raised when a bad request was made to a Legal Hold endpoint."""

    def __init__(self, exception):
        super(Py42LegalHoldCriteriaMissingError, self).__init__(
            exception,
            u"At least one criteria must be specified; legal_hold_membership_uid, "
            u"legal_hold_uid, user_uid, or user.",
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


class Py42UsernameMustBeEmailError(Py42InternalServerError):
    """An exception raised when trying to set a non-email as a user's username
    in a cloud environment."""

    def __init__(self, exception):
        message = u"Username must be an email address."
        super(Py42UsernameMustBeEmailError, self).__init__(exception, message)


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


class Py42UnableToCreateProfileError(Py42BadRequestError):
    """An error raised when trying to call the method for creating a detection-list
    user when the user does not exist or is currently awaiting the profile to get
    created on the back-end. Note: you are no longer able to create detection-list
    profiles using the API; py42 only returns already existing profiles."""

    def __init__(self, exception, username):
        message = (
            u"Detection-list profiles are now created automatically on the server. "
            u"Unable to find a detection-list profile for '{}'. "
            u"It is possibly still being created if you just recently created the "
            u"Code42 user.".format(username)
        )
        super(Py42UnableToCreateProfileError, self).__init__(exception, message)


class Py42InvalidRuleError(Py42NotFoundError):
    """An exception raised when the observer rule ID does not exist."""

    def __init__(self, exception, rule_id):
        message = u"Invalid Observer Rule ID '{}'.".format(rule_id)
        super(Py42NotFoundError, self).__init__(exception, message)


class Py42UpdateClosedCaseError(Py42BadRequestError):
    """An error raised when trying to update a closed case."""

    def __init__(self, exception):
        msg = u"Cannot update a closed case."
        super(Py42UpdateClosedCaseError, self).__init__(exception, msg)


class Py42CaseNameExistsError(Py42BadRequestError):
    """An error raised when trying to create a case with a name that already exists."""

    def __init__(self, exception, case_name):
        msg = u"Case name '{}' already exists, please set another name".format(
            case_name
        )
        super(Py42CaseNameExistsError, self).__init__(exception, msg)


class Py42DescriptionLimitExceededError(Py42BadRequestError):
    """An error raised when description of a case exceeds the allowed char length limit."""

    def __init__(self, exception):
        msg = u"Description limit exceeded, max 250 characters allowed."
        super(Py42DescriptionLimitExceededError, self).__init__(exception, msg)


class Py42InvalidCaseUserError(Py42BadRequestError):
    """An error raised when a case subject or assignee is not a valid user."""

    def __init__(self, exception, user_field):
        msg = u"The provided {} is not a valid user.".format(user_field)
        super(Py42InvalidCaseUserError, self).__init__(exception, msg)


class Py42CaseAlreadyHasEventError(Py42BadRequestError):
    """An error raised when event is already associated to the case."""

    def __init__(self, exception):
        msg = u"Event is already associated to the case."
        super(Py42CaseAlreadyHasEventError, self).__init__(exception, msg)


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
