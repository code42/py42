from pycpg.settings import debug


class PycpgError(Exception):
    """A generic, Pycpg custom base exception."""


class PycpgResponseError(PycpgError):
    """A base custom class to manage all errors raised because of an HTTP response."""

    def __init__(self, response, message, *args):
        super().__init__(message, *args)
        self._response = response

    @property
    def response(self):
        """The response prior to the error."""
        return self._response


class PycpgArchiveFileNotFoundError(PycpgResponseError):
    """An exception raised when a resource file is not found or the path is invalid."""

    def __init__(self, response, device_guid, file_path):
        message = (
            f"File not found in archive for device {device_guid} at path {file_path}"
        )
        super().__init__(response, message, device_guid, file_path)
        self._device_guid = device_guid
        self._file_path = file_path

    @property
    def device_guid(self):
        """The device GUID provided."""
        return self._device_guid

    @property
    def file_path(self):
        """The file path provided."""
        return self._file_path


class PycpgChecksumNotFoundError(PycpgResponseError):
    """An exception raised when a user-supplied hash could not successfully locate its corresponding resource."""

    def __init__(self, response, checksum_name, checksum_value):
        message = f"No files found with {checksum_name} checksum {checksum_value}."
        super().__init__(response, message, checksum_name, checksum_value)
        self._checksum_name = checksum_name
        self._checksum_value = checksum_value

    @property
    def checksum_name(self):
        """The checksum name."""
        return self._checksum_name

    @property
    def checksum_value(self):
        """The checksum value."""
        return self.checksum_value


class PycpgFeatureUnavailableError(PycpgResponseError):
    """An exception raised when a requested feature is not supported in your CrashPlan environment."""

    def __init__(self, response):
        super().__init__(
            response,
            "You may be trying to use a feature that is unavailable in your environment.",
        )


class PycpgHTTPError(PycpgResponseError):
    """A base custom class to manage all HTTP errors raised by an API endpoint."""

    def __init__(self, exception, message=None, *args):
        if not message:
            response_content = f"Response content: {exception.response.text}"
            message = f"Failure in HTTP call {exception}. {response_content}"
            debug.logger.debug(message)

        super().__init__(exception.response, message, *args)


class PycpgDeviceNotConnectedError(PycpgResponseError):
    """An exception raised when trying to push a restore to a device that is not
    connected to an Authority server."""

    def __init__(self, response, device_guid):
        message = (
            f"Device with GUID '{device_guid}' is not currently connected to the Authority "
            "server."
        )
        super().__init__(response, message, device_guid)
        self._device_guid = device_guid

    @property
    def device_guid(self):
        """The device GUID."""
        return self._device_guid


class PycpgInvalidArchivePassword(PycpgHTTPError):
    """An exception raised when the password for unlocking an archive is invalid."""

    def __init__(self, exception):
        message = "Invalid archive password."
        super().__init__(exception, message)


class PycpgInvalidArchiveEncryptionKey(PycpgHTTPError):
    """An exception raised the encryption key for an archive is invalid."""

    def __init__(self, exception):
        message = "Invalid archive encryption key."
        super().__init__(exception, message)


class PycpgStorageSessionInitializationError(PycpgHTTPError):
    """An exception raised when the user is not authorized to initialize a storage session. This
    may occur when trying to restore a file or trying to get events for file activity on removable
    media, in cloud sync folders, and browser uploads."""

    def __init__(self, exception, message):
        super().__init__(exception, message)


class PycpgSessionInitializationError(PycpgError):
    """An exception raised when a user connection is invalid. A connection might be invalid due to
    connection timeout, invalid token, etc.
    """

    def __init__(self, exception):
        message = (
            "An error occurred while requesting "
            f"server environment information, caused by {exception}"
        )
        super().__init__(exception, message)


class PycpgBadRequestError(PycpgHTTPError):
    """A wrapper to represent an HTTP 400 error."""


class PycpgUnauthorizedError(PycpgHTTPError):
    """A wrapper to represent an HTTP 401 error."""


class PycpgForbiddenError(PycpgHTTPError):
    """A wrapper to represent an HTTP 403 error."""


class PycpgNotFoundError(PycpgHTTPError):
    """A wrapper to represent an HTTP 404 error."""


class PycpgConflictError(PycpgHTTPError):
    """A wrapper to represent an HTTP 409 error."""


class PycpgInternalServerError(PycpgHTTPError):
    """A wrapper to represent an HTTP 500 error."""


class PycpgTooManyRequestsError(PycpgHTTPError):
    """A wrapper to represent an HTTP 429 error."""


class PycpgOrgNotFoundError(PycpgBadRequestError):
    """An exception raised when a 400 HTTP error message indicates that an
    organization was not found."""

    def __init__(self, exception, org_uid):
        msg = f"The organization with UID '{org_uid}' was not found."
        super().__init__(exception, msg, org_uid)
        self._org_uid = org_uid

    @property
    def org_uid(self):
        """ " The org UID."""
        return self._org_uid


class PycpgActiveLegalHoldError(PycpgBadRequestError):
    """An exception raised when attempting to deactivate a user or device that is in an
    active legal hold."""

    def __init__(self, exception, resource, resource_id):
        msg = f"Cannot deactivate the {resource} with ID {resource_id} as the {resource} is involved in a legal hold matter."
        super().__init__(exception, msg, resource, resource_id)
        self._resource = resource
        self._resource_id = resource_id

    @property
    def resource(self):
        """The user or device resource."""
        return self._resource

    @property
    def resource_id(self):
        """The resource ID."""
        return self._resource_id


class PycpgUserAlreadyAddedError(PycpgBadRequestError):
    """An exception raised when the user is already added to group or list, such as the
    Departing Employee list."""

    def __init__(self, exception, user_id, list_name):
        msg = f"User with ID {user_id} is already on the {list_name}."
        super().__init__(exception, msg, user_id, list_name)
        self._user_id = user_id

    @property
    def user_id(self):
        """The user ID."""
        return self._user_id


class PycpgLegalHoldNotFoundOrPermissionDeniedError(PycpgForbiddenError):
    """An exception raised when a legal hold matter is inaccessible from your account or
    the matter UID is not valid."""

    def __init__(self, exception, resource_uid, legal_hold_resource="matter"):
        message = f"{legal_hold_resource.capitalize()} with UID '{resource_uid}' can not be found. Your account may not have permission to view the {legal_hold_resource.lower()}."
        super().__init__(exception, message, resource_uid)
        self._resource_uid = resource_uid

    @property
    def uid(self):
        """The UID of the legal hold resource."""
        return self._resource_uid


class PycpgLegalHoldCriteriaMissingError(PycpgBadRequestError):
    """An exception raised when a bad request was made to a Legal Hold endpoint."""

    def __init__(self, exception):
        super().__init__(
            exception,
            "At least one criteria must be specified: legal_hold_membership_uid, "
            "legal_hold_matter_uid, user_uid, or user.",
        )


class PycpgLegalHoldAlreadyDeactivatedError(PycpgBadRequestError):
    """An exception raised when trying to deactivate a Legal Hold Matter that is already inactive."""

    def __init__(self, exception, legal_hold_matter_uid):
        message = f"Legal Hold Matter with UID '{legal_hold_matter_uid}' has already been deactivated."
        super().__init__(exception, message, legal_hold_matter_uid)
        self._legal_hold_matter_uid = legal_hold_matter_uid

    @property
    def legal_hold_matter_uid(self):
        """The legal hold matter UID."""
        return self._legal_hold_matter_uid


class PycpgLegalHoldAlreadyActiveError(PycpgBadRequestError):
    """An exception raised when trying to activate a Legal Hold Matter that is already active."""

    def __init__(self, exception, legal_hold_matter_uid):
        message = (
            f"Legal Hold Matter with UID '{legal_hold_matter_uid}' is already active."
        )
        super().__init__(exception, message, legal_hold_matter_uid)
        self._legal_hold_matter_uid = legal_hold_matter_uid

    @property
    def legal_hold_matter_uid(self):
        """The legal hold matter UID."""
        return self._legal_hold_matter_uid



class PycpgMFARequiredError(PycpgUnauthorizedError):
    """Deprecated: An exception raised when a request requires multi-factor authentication"""

    def __init__(self, exception, message=None):
        message = message or "User requires multi-factor authentication."
        super().__init__(exception, message)


class PycpgUserAlreadyExistsError(PycpgInternalServerError):
    """An exception raised when a user already exists"""

    def __init__(self, exception, message=None):
        message = message or "User already exists."
        super().__init__(exception, message)


class PycpgUsernameMustBeEmailError(PycpgInternalServerError):
    """An exception raised when trying to set a non-email as a user's username
    in a cloud environment."""

    def __init__(self, exception):
        message = "Username must be an email address."
        super().__init__(exception, message)


class PycpgInvalidEmailError(PycpgInternalServerError):
    """An exception raised when trying to set an invalid email as a user's email."""

    def __init__(self, email, exception):
        message = f"'{email}' is not a valid email."
        super().__init__(exception, message, email)
        self._email = email

    @property
    def email(self):
        """The email being assigned to a user."""
        return self._email


class PycpgInvalidPasswordError(PycpgInternalServerError):
    """An exception raised when trying to set an invalid password as a user's password."""

    def __init__(self, exception):
        message = "Invalid password."
        super().__init__(exception, message)


class PycpgInvalidUsernameError(PycpgInternalServerError):
    """An exception raised when trying to set an invalid username as a user's username."""

    def __init__(self, exception):
        message = "Invalid username."
        super().__init__(exception, message)



class PycpgBadRestoreRequestError(PycpgBadRequestError):
    """An error raised when the given restore arguments are not compatible and cause
    a bad request."""

    def __init__(self, exception):
        message = "Unable to create restore session."
        super().__init__(exception, message)


class PycpgInvalidPageTokenError(PycpgBadRequestError):
    """An error raised when the page token given is invalid."""

    def __init__(self, exception, page_token):
        message = (
            f'Invalid page token: "{page_token}".\n'
            "Page tokens match the last event ID received in a previous query.  "
            "Your page token may be invalid if the original query has changed "
            "such that the corresponding event is being filtered out of the results, "
            "or if the event has expired according to your data retention policy."
        )
        super().__init__(exception, message, page_token)
        self._page_token = page_token

    @property
    def page_token(self):
        """The page token."""
        return self._page_token



def raise_pycpg_error(raised_error):
    """Raises the appropriate :class:`pycpg.exceptions.PycpgHttpError` based on the given
    HTTPError's response status code.
    """
    if raised_error.response.status_code == 400:
        raise PycpgBadRequestError(raised_error)
    elif raised_error.response.status_code == 401:
        raise PycpgUnauthorizedError(raised_error)
    elif raised_error.response.status_code == 403:
        raise PycpgForbiddenError(raised_error)
    elif raised_error.response.status_code == 404:
        raise PycpgNotFoundError(raised_error)
    elif raised_error.response.status_code == 409:
        raise PycpgConflictError(raised_error)
    elif raised_error.response.status_code == 429:
        raise PycpgTooManyRequestsError(raised_error)
    elif 500 <= raised_error.response.status_code < 600:
        raise PycpgInternalServerError(raised_error)
    else:
        raise PycpgHTTPError(raised_error)
