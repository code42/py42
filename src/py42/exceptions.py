from py42.settings import debug


class Py42Error(Exception):
    """A generic, Py42 custom base exception."""


class Py42ResponseError(Py42Error):
    """A base custom class to manage all errors raised because of an HTTP response."""

    def __init__(self, response, message, *args):
        super().__init__(message, *args)
        self._response = response

    @property
    def response(self):
        """The response prior to the error."""
        return self._response


class Py42ArchiveFileNotFoundError(Py42ResponseError):
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


class Py42ChecksumNotFoundError(Py42ResponseError):
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


class Py42FeatureUnavailableError(Py42ResponseError):
    """An exception raised when a requested feature is not supported in your Code42 environment."""

    def __init__(self, response):
        super().__init__(
            response,
            "You may be trying to use a feature that is unavailable in your environment.",
        )


class Py42HTTPError(Py42ResponseError):
    """A base custom class to manage all HTTP errors raised by an API endpoint."""

    def __init__(self, exception, message=None, *args):
        if not message:
            response_content = f"Response content: {exception.response.text}"
            message = f"Failure in HTTP call {exception}. {response_content}"
            debug.logger.debug(message)

        super().__init__(exception.response, message, *args)


class Py42DeviceNotConnectedError(Py42ResponseError):
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


class Py42InvalidArchivePassword(Py42HTTPError):
    """An exception raised when the password for unlocking an archive is invalid."""

    def __init__(self, exception):
        message = "Invalid archive password."
        super().__init__(exception, message)


class Py42InvalidArchiveEncryptionKey(Py42HTTPError):
    """An exception raised the encryption key for an archive is invalid."""

    def __init__(self, exception):
        message = "Invalid archive encryption key."
        super().__init__(exception, message)


class Py42StorageSessionInitializationError(Py42HTTPError):
    """An exception raised when the user is not authorized to initialize a storage session. This
    may occur when trying to restore a file or trying to get events for file activity on removable
    media, in cloud sync folders, and browser uploads."""

    def __init__(self, exception, message):
        super().__init__(exception, message)


class Py42SessionInitializationError(Py42Error):
    """An exception raised when a user connection is invalid. A connection might be invalid due to
    connection timeout, invalid token, etc.
    """

    def __init__(self, exception):
        message = (
            "An error occurred while requesting "
            f"server environment information, caused by {exception}"
        )
        super().__init__(exception, message)


class Py42BadRequestError(Py42HTTPError):
    """A wrapper to represent an HTTP 400 error."""


class Py42UnauthorizedError(Py42HTTPError):
    """A wrapper to represent an HTTP 401 error."""


class Py42ForbiddenError(Py42HTTPError):
    """A wrapper to represent an HTTP 403 error."""


class Py42NotFoundError(Py42HTTPError):
    """A wrapper to represent an HTTP 404 error."""


class Py42ConflictError(Py42HTTPError):
    """A wrapper to represent an HTTP 409 error."""


class Py42InternalServerError(Py42HTTPError):
    """A wrapper to represent an HTTP 500 error."""


class Py42TooManyRequestsError(Py42HTTPError):
    """A wrapper to represent an HTTP 429 error."""


class Py42OrgNotFoundError(Py42BadRequestError):
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


class Py42ActiveLegalHoldError(Py42BadRequestError):
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


class Py42UserAlreadyAddedError(Py42BadRequestError):
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


class Py42LegalHoldNotFoundOrPermissionDeniedError(Py42ForbiddenError):
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


class Py42LegalHoldCriteriaMissingError(Py42BadRequestError):
    """An exception raised when a bad request was made to a Legal Hold endpoint."""

    def __init__(self, exception):
        super().__init__(
            exception,
            "At least one criteria must be specified: legal_hold_membership_uid, "
            "legal_hold_matter_uid, user_uid, or user.",
        )


class Py42LegalHoldAlreadyDeactivatedError(Py42BadRequestError):
    """An exception raised when trying to deactivate a Legal Hold Matter that is already inactive."""

    def __init__(self, exception, legal_hold_matter_uid):
        message = f"Legal Hold Matter with UID '{legal_hold_matter_uid}' has already been deactivated."
        super().__init__(exception, message, legal_hold_matter_uid)
        self._legal_hold_matter_uid = legal_hold_matter_uid

    @property
    def legal_hold_matter_uid(self):
        """The legal hold matter UID."""
        return self._legal_hold_matter_uid


class Py42LegalHoldAlreadyActiveError(Py42BadRequestError):
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


class Py42InvalidRuleOperationError(Py42HTTPError):
    """An exception raised when trying to add or remove users to a system rule."""

    def __init__(self, exception, rule_id, source):
        msg = "Only alert rules with a source of 'Alerting' can be targeted by this command. "
        msg += f"Rule {rule_id} has a source of '{source}'."
        super().__init__(exception, msg, rule_id, source)
        self._rule_id = rule_id
        self._source = source

    @property
    def rule_id(self):
        """The rule ID."""
        return self._rule_id

    @property
    def source(self):
        """The rule source."""
        return self._source


class Py42MFARequiredError(Py42UnauthorizedError):
    """Deprecated: An exception raised when a request requires multi-factor authentication"""

    def __init__(self, exception, message=None):
        message = message or "User requires multi-factor authentication."
        super().__init__(exception, message)


class Py42UserAlreadyExistsError(Py42InternalServerError):
    """An exception raised when a user already exists"""

    def __init__(self, exception, message=None):
        message = message or "User already exists."
        super().__init__(exception, message)


class Py42UsernameMustBeEmailError(Py42InternalServerError):
    """An exception raised when trying to set a non-email as a user's username
    in a cloud environment."""

    def __init__(self, exception):
        message = "Username must be an email address."
        super().__init__(exception, message)


class Py42InvalidEmailError(Py42InternalServerError):
    """An exception raised when trying to set an invalid email as a user's email."""

    def __init__(self, email, exception):
        message = f"'{email}' is not a valid email."
        super().__init__(exception, message, email)
        self._email = email

    @property
    def email(self):
        """The email being assigned to a user."""
        return self._email


class Py42InvalidPasswordError(Py42InternalServerError):
    """An exception raised when trying to set an invalid password as a user's password."""

    def __init__(self, exception):
        message = "Invalid password."
        super().__init__(exception, message)


class Py42InvalidUsernameError(Py42InternalServerError):
    """An exception raised when trying to set an invalid username as a user's username."""

    def __init__(self, exception):
        message = "Invalid username."
        super().__init__(exception, message)


class Py42CloudAliasLimitExceededError(Py42BadRequestError):
    """An Exception raised when trying to add a cloud alias to a user when that user
    already has the max amount of supported cloud aliases."""

    def __init__(self, exception, message=None):
        message = (
            message
            or "Cloud alias limit exceeded. A max of 2 cloud aliases are allowed."
        )
        super(Py42BadRequestError, self).__init__(exception, message)


class Py42CloudAliasCharacterLimitExceededError(Py42Error):
    """An exception raised when trying to add a cloud alias to a user that exceeds the max character limit."""

    def __init__(self):
        message = "Cloud alias character limit exceeded. Max 50 characters."
        super().__init__(message)


class Py42BadRestoreRequestError(Py42BadRequestError):
    """An error raised when the given restore arguments are not compatible and cause
    a bad request."""

    def __init__(self, exception):
        message = "Unable to create restore session."
        super().__init__(exception, message)


class Py42InvalidPageTokenError(Py42BadRequestError):
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


class Py42UserNotOnListError(Py42NotFoundError):
    """An exception raised when the user is not on a detection list."""

    def __init__(self, exception, user_id, list_name):
        message = f"User with ID '{user_id}' is not currently on the {list_name} list."
        super(Py42NotFoundError, self).__init__(exception, message, user_id, list_name)
        self._user_id = user_id
        self._list_name = list_name

    @property
    def user_id(self):
        """The user ID."""
        return self._user_id

    @property
    def list_name(self):
        """The list name."""
        return self._list_name


class Py42UnableToCreateProfileError(Py42BadRequestError):
    """An error raised when trying to call the method for creating a detection-list
    user when the user does not exist or is currently awaiting the profile to get
    created on the back-end. Note: you are no longer able to create detection-list
    profiles using the API; py42 only returns already existing profiles."""

    def __init__(self, exception, username):
        message = (
            "Detection-list profiles are now created automatically on the server. "
            f"Unable to find a detection-list profile for '{username}'. "
            "It is possibly still being created if you just recently created the "
            "Code42 user."
        )
        super().__init__(exception, message, username)
        self._username = username

    @property
    def username(self):
        """The username of the user."""
        return self._username


class Py42InvalidRuleError(Py42NotFoundError):
    """An exception raised when the observer rule ID does not exist."""

    def __init__(self, exception, rule_id):
        message = f"Invalid Observer Rule ID '{rule_id}'."
        super(Py42NotFoundError, self).__init__(exception, message, rule_id)
        self._rule_id = rule_id

    @property
    def rule_id(self):
        """The observer rule ID."""
        return self._rule_id


class Py42UpdateClosedCaseError(Py42BadRequestError):
    """An error raised when trying to update a closed case."""

    def __init__(self, exception):
        msg = "Cannot update a closed case."
        super().__init__(exception, msg)


class Py42CaseNameExistsError(Py42BadRequestError):
    """An error raised when trying to create a case with a name that already exists."""

    def __init__(self, exception, case_name):
        msg = f"Case name '{case_name}' already exists, please set another name."
        super().__init__(exception, msg, case_name)
        self._case_name = case_name

    @property
    def case_name(self):
        """The case name."""
        return self._case_name


class Py42DescriptionLimitExceededError(Py42BadRequestError):
    """An error raised when description of a case exceeds the allowed char length limit."""

    def __init__(self, exception):
        msg = "Description limit exceeded, max 250 characters allowed."
        super().__init__(exception, msg)


class Py42InvalidCaseUserError(Py42BadRequestError):
    """An error raised when a case subject or assignee is not a valid user."""

    def __init__(self, exception, user_uid):
        msg = f"The provided {user_uid} is not a valid user."
        super().__init__(exception, msg)
        self._user_uid = user_uid

    @property
    def user(self):
        """The user UID."""
        return self._user_uid


class Py42CaseAlreadyHasEventError(Py42BadRequestError):
    """An error raised when event is already associated to the case."""

    def __init__(self, exception):
        msg = "Event is already associated to the case."
        super().__init__(exception, msg)


class Py42TrustedActivityInvalidChangeError(Py42BadRequestError):
    """An error raised when an invalid change is being made to a trusted activity."""

    def __init__(self, exception):
        msg = "Invalid change to trusted activity. Trusted activity type cannot be changed."
        super().__init__(exception, msg)


class Py42TrustedActivityConflictError(Py42ConflictError):
    """An error raised when theres a conflict with a trusted activity domain URL."""

    def __init__(self, exception, value):
        msg = (
            f"Duplicate URL or workspace name, '{value}' already exists on your trusted list.  "
            "Please provide a unique value"
        )
        super().__init__(exception, msg, value)
        self._value = value

    @property
    def value(self):
        """The domain, URL or workspace name."""
        return self._value


class Py42TrustedActivityInvalidCharacterError(Py42BadRequestError):
    """An error raised when an invalid character is in a trusted activity value."""

    def __init__(self, exception):
        msg = "Invalid character in domain or Slack workspace name"
        super().__init__(exception, msg)


class Py42TrustedActivityIdNotFound(Py42NotFoundError):
    """An exception raised when the trusted activity ID does not exist."""

    def __init__(self, exception, resource_id):
        message = f"Resource ID '{resource_id}' not found."
        super().__init__(exception, message, resource_id)
        self._resource_id = resource_id

    @property
    def resource_id(self):
        """The resource ID."""
        return self._resource_id


class Py42WatchlistNotFound(Py42NotFoundError):
    """An exception raised when the watchlist with the given ID was not found."""

    def __init__(self, exception, resource_id):
        message = f"Watchlist ID '{resource_id}' not found."
        super().__init__(exception, message, resource_id)
        self._watchlist_id = resource_id

    @property
    def watchlist_id(self):
        """The watchlist ID."""
        return self._watchlist_id


class Py42WatchlistOrUserNotFound(Py42NotFoundError):
    """An exception raised when the watchlist ID or the User ID does not exist."""

    def __init__(self, exception, watchlist_id, user_id):
        message = f"Watchlist ID '{watchlist_id}' or User ID '{user_id}' not found."
        super().__init__(exception, message, watchlist_id, user_id)
        self._watchlist_id = watchlist_id
        self._user_id = user_id

    @property
    def watchlist_id(self):
        """The watchlist ID."""
        return self._watchlist_id

    @property
    def user_id(self):
        """The user ID."""
        return self._user_id


class Py42InvalidWatchlistType(Py42BadRequestError):
    """An exception raised when an invalid watchlist type is specified."""

    def __init__(self, exception, watchlist_type):
        message = f"'{watchlist_type}' cannot be converted to a valid watchlist type.  Please look at the WatchlistType class for valid types."
        super().__init__(exception, message, watchlist_type)
        self._watchlist_type = watchlist_type

    @property
    def watchlist_type(self):
        """The specified watchlist type."""
        return self._watchlist_type


class Py42UserRiskProfileNotFound(Py42NotFoundError):
    """An exception raised when the user with the given ID for a user risk profile was not found."""

    def __init__(self, exception, user_id, identifier="ID"):
        message = (
            f"User risk profile for user with the {identifier} '{user_id}' not found."
        )
        super().__init__(exception, message, user_id)
        self._user_id = user_id

    @property
    def user(self):
        """The user identifier."""
        return self._user_id


def raise_py42_error(raised_error):
    """Raises the appropriate :class:`py42.exceptions.Py42HttpError` based on the given
    HTTPError's response status code.
    """
    if raised_error.response.status_code == 400:
        raise Py42BadRequestError(raised_error)
    elif raised_error.response.status_code == 401:
        raise Py42UnauthorizedError(raised_error)
    elif raised_error.response.status_code == 403:
        raise Py42ForbiddenError(raised_error)
    elif raised_error.response.status_code == 404:
        raise Py42NotFoundError(raised_error)
    elif raised_error.response.status_code == 409:
        raise Py42ConflictError(raised_error)
    elif raised_error.response.status_code == 429:
        raise Py42TooManyRequestsError(raised_error)
    elif 500 <= raised_error.response.status_code < 600:
        raise Py42InternalServerError(raised_error)
    else:
        raise Py42HTTPError(raised_error)
