from requests import Session

from py42._internal.initialization import SDKDependencies
from py42._internal.session_factory import (
    AuthHandlerFactory,
    SessionFactory,
    SessionModifierFactory,
)


def from_local_account(host_address, username, password):
    """Creates a :class:`~py42.sdk.SDKClient` object for accessing the Code42 REST APIs using the
    supplied credentials. Currently, only accounts created within the Code42 console or using the
    APIs (including py42) are supported. Username/passwords that are based on Active Directory,
    Okta, or other Identity providers cannot be used with this method.

    Args:
        host_address (str): The domain name of the Code42 instance being authenticated to, e.g.
            console.us.code42.com
        username (str): The username of the authenticating account.
        password (str): The password of the authenticating account.

    Returns:
        :class:`py42.sdk.SDKClient`
    """
    return SDKClient.from_local_account(host_address, username, password)


class SDKClient(object):
    def __init__(self, sdk_dependencies):
        self._sdk_dependencies = sdk_dependencies

    @classmethod
    def from_local_account(cls, host_address, username, password):
        """Creates a :class:`~py42.sdk.SDKClient` object for accessing the Code42 REST APIs using
        the supplied credentials. Currently, only accounts created within the Code42 console or
        using the APIs (including py42) are supported. Username/passwords that are based on Active
        Directory, Okta, or other Identity providers cannot be used with this method.

        Args:
            host_address (str): The domain name of the Code42 instance being authenticated to, e.g.
                console.us.code42.com
            username (str): The username of the authenticating account.
            password (str): The password of the authenticating account.

        Returns:
            :class:`py42.sdk.SDKClient`
        """
        session_impl = Session
        session_factory = SessionFactory(
            session_impl, SessionModifierFactory(), AuthHandlerFactory()
        )
        basic_auth_session = session_factory.create_basic_auth_session(
            host_address, username, password
        )
        sdk_dependencies = SDKDependencies(host_address, session_factory, basic_auth_session)
        return cls(sdk_dependencies)

    @property
    def serveradmin(self):
        """A collection of methods for getting server information for on-premise environments
        and tenant information for cloud environments.

        Returns:
            :class:`py42.clients.administration.AdministrationClient`
        """
        return self._sdk_dependencies.administration_client

    @property
    def archive(self):
        """A collection of methods for accessing Code42 storage archives. Useful for doing
        web-restores or finding a file on an archive.

        Returns:
            :class:`py42.modules.archive.ArchiveModule`
        """
        return self._sdk_dependencies.archive_module

    @property
    def users(self):
        """A collection of methods for retrieving or updating data about users in the Code42
        environment.

        Returns:
            :class:`py42.clients.users.UserClient`
        """
        return self._sdk_dependencies.user_client

    @property
    def devices(self):
        """A collection of methods for retrieving or updating data about devices in the Code42
        environment.

        Returns:
            :class:`py42.clients.devices.DeviceClient`
        """
        return self._sdk_dependencies.device_client

    @property
    def orgs(self):
        """A collection of methods for retrieving or updating data about organizations in the
        Code42 environment.

        Returns:
            :class:`py42.clients.orgs.OrgClient`
        """
        return self._sdk_dependencies.org_client

    @property
    def legalhold(self):
        """A collection of methods for retrieving and updating legal-hold matters, policies, and
        custodians.

        Returns:
            :class:`py42.clients.legalhold.LegalHoldClient`
        """
        return self._sdk_dependencies.legal_hold_client

    @property
    def usercontext(self):
        """A collection of methods related to getting information about the currently logged in
        user, such as the tenant ID.

        Returns:
            :class:`py42.usercontext.UserContext`
        """
        return self._sdk_dependencies.user_context

    @property
    def securitydata(self):
        """A collection of methods and properties for getting security data such as:
            * File events
            * Alerts
            * Security plan information

        Returns:
            :class:`py42.modules.securitydata.SecurityModule`
        """
        return self._sdk_dependencies.security_module

    @property
    def detectionlists(self):
        """A collection of properties each containing methods for managing specific detection
        lists, such as departing employees.

        Returns:
            :class:`py42.modules.detectionlists.DetectionListsModule`
        """
        return self._sdk_dependencies.detection_lists_module

    @property
    def alerts(self):
        """A collection of methods related to retrieving and updating alerts rules.

        Returns:
            :class:`py42.modules.alertrules.AlertRulesModule`
        """
        return self._sdk_dependencies.alerts_module
