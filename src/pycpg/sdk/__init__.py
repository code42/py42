import warnings

from requests.auth import HTTPBasicAuth

from pycpg.exceptions import PycpgError
from pycpg.exceptions import PycpgUnauthorizedError
from pycpg.services._auth import ApiClientAuth
from pycpg.services._auth import BearerAuth
from pycpg.services._auth import CustomJWTAuth
from pycpg.services._connection import Connection
from pycpg.usercontext import UserContext

warnings.simplefilter("always", DeprecationWarning)
warnings.simplefilter("always", UserWarning)


def from_api_client(host_address, client_id, secret):
    """Creates a :class:`~pycpg.sdk.SDKClient` object for accessing the CrashPlan REST APIs using
    an API client ID and secret.

    Args:
        host_address (str): The domain name of the CrashPlan instance being authenticated to, e.g.
            console.us1.crashPlan.com
        client_id (str): The client ID of the API client to authenticate with.
        secret (str): The secret of the API client to authenticate with.

    Returns:
        :class:`pycpg.sdk.SDKClient`
    """

    return SDKClient.from_api_client(host_address, client_id, secret)


def from_local_account(host_address, username, password, totp=None):
    """Creates a :class:`~pycpg.sdk.SDKClient` object for accessing the CrashPlan REST APIs using the
    supplied credentials. This method supports only accounts created within the CrashPlan console or using the
    APIs (including pycpg). Username/passwords that are based on Active Directory,
    Okta, or other Identity providers cannot be used with this method.

    Args:
        host_address (str): The domain name of the CrashPlan instance being authenticated to, e.g.
            console.us1.crashPlan.com
        username (str): The username of the authenticating account.
        password (str): The password of the authenticating account.
        totp (callable or str, optional): The time-based one-time password of the authenticating account. Include only
            if the account uses CrashPlan's two-factor authentication. Defaults to None.

    Returns:
        :class:`pycpg.sdk.SDKClient`
    """
    client = SDKClient.from_local_account(host_address, username, password, totp)

    # test credentials
    try:
        client.users.get_current()
    except PycpgUnauthorizedError as err:
        login_type = client.loginconfig.get_for_user(username)["loginType"]
        if login_type == "CLOUD_SSO":
            raise PycpgError("SSO users are not supported in `from_local_account()`.")
        msg = f"SDK initialization failed, double-check username/password, and provide two-factor TOTP token if Multi-Factor Auth configured for your user. User LoginConfig: {login_type}"
        err.args = (msg,)
        raise
    return client


def from_jwt_provider(host_address, jwt_provider):
    """Creates a :class:`~pycpg.sdk.SDKClient` object for accessing the CrashPlan REST APIs using a custom
    auth mechanism. User can use any authentication mechanism like that returns a JSON Web token on authentication
    which would then be used for all subsequent requests.

    Args:
        host_address (str): The domain name of the CrashPlan instance being authenticated to, e.g.
            console.us1.crashPlan.com
        jwt_provider (function): A function that accepts no parameters and on execution returns a JSON web token string.

    Returns:
        :class:`pycpg.sdk.SDKClient`
    """

    client = SDKClient.from_jwt_provider(host_address, jwt_provider)
    client.usercontext.get_current_tenant_id()
    return client


class SDKClient:
    def __init__(self, main_connection, auth, auth_flag=None):
        services, user_ctx = _init_services(main_connection, auth, auth_flag)
        self._clients = _init_clients(services, main_connection)
        self._user_ctx = user_ctx
        self._auth_flag = auth_flag

    @classmethod
    def from_api_client(cls, host_address, client_id, secret):
        """Creates a :class:`~pycpg.sdk.SDKClient` object for accessing the CrashPlan REST APIs using
        an API client ID and secret.

        Args:
            host_address (str): The domain name of the CrashPlan instance being authenticated to, e.g.
                console.us1.crashPlan.com
            client_id (str): The client ID of the API client to authenticate with.
            secret (str): The secret of the API client to authenticate with.

        Returns:
            :class:`pycpg.sdk.SDKClient`
        """

        basic_auth = HTTPBasicAuth(client_id, secret)
        auth_connection = Connection.from_host_address(host_address, auth=basic_auth)
        api_client_auth = ApiClientAuth(auth_connection)
        main_connection = Connection.from_host_address(
            host_address, auth=api_client_auth
        )
        api_client_auth.get_credentials()
        return cls(main_connection, api_client_auth, auth_flag=1)

    @classmethod
    def from_local_account(cls, host_address, username, password, totp=None):
        """Creates a :class:`~pycpg.sdk.SDKClient` object for accessing the CrashPlan REST APIs using
        the supplied credentials. This method supports only accounts created within the CrashPlan console or
        using the APIs (including pycpg). Username/passwords that are based on Active
        Directory, Okta, or other Identity providers should use the `from_jwt_provider` method.

        Args:
            host_address (str): The domain name of the CrashPlan instance being authenticated to, e.g.
                console.us1.crashPlan.com
            username (str): The username of the authenticating account.
            password (str): The password of the authenticating account.
            totp (callable or str, optional): The time-based one-time password of the authenticating account. Include only
                if the account uses CrashPlan's two-factor authentication. Defaults to None.
        Returns:
            :class:`pycpg.sdk.SDKClient`
        """
        basic_auth = None
        if username and password:
            basic_auth = HTTPBasicAuth(username, password)
        auth_connection = Connection.from_host_address(host_address, auth=basic_auth)
        bearer_auth = BearerAuth(auth_connection, totp)
        main_connection = Connection.from_host_address(host_address, auth=bearer_auth)

        return cls(main_connection, bearer_auth)

    @classmethod
    def from_jwt_provider(cls, host_address, jwt_provider):
        """Creates a :class:`~pycpg.sdk.SDKClient` object for accessing the CrashPlan REST APIs using a custom
            auth mechanism. User can use any authentication mechanism like that returns a JSON Web token
            on authentication which would then be used for all subsequent requests.

        Args:
            host_address (str): The domain name of the CrashPlan instance being authenticated to, e.g.
                console.us1.crashPlan.com
            jwt_provider (function): A function that accepts no parameters and on execution returns a
            JSON web token string.

        Returns:
            :class:`pycpg.sdk.SDKClient`
        """
        custom_auth = CustomJWTAuth(jwt_provider)
        main_connection = Connection.from_host_address(host_address, auth=custom_auth)
        custom_auth.get_credentials()
        return cls(main_connection, custom_auth)

    @property
    def loginconfig(self):
        """A collection of methods related to getting information about the login configuration
        of user accounts.

        Returns:
            :class:`pycpg.clients.loginconfig.LoginConfigurationClient.`
        """
        return self._clients.loginconfig

    @property
    def serveradmin(self):
        """A collection of methods for getting server information for on-premise environments
        and tenant information for cloud environments.

        Returns:
            :class:`pycpg.services.administration.AdministrationService`
        """
        return self._clients.authority.administration

    @property
    def archive(self):
        """A collection of methods for accessing CrashPlan storage archives. Useful for doing
        web-restores or finding a file on an archive.

        Returns:
            :class:`pycpg.clients.archive.ArchiveClient`
        """
        return self._clients.archive

    @property
    def users(self):
        """A collection of methods for retrieving or updating data about users in the CrashPlan
        environment.

        Returns:
            :class:`pycpg.services.users.UserService`
        """
        return self._clients.authority.users

    @property
    def devices(self):
        """A collection of methods for retrieving or updating data about devices in the CrashPlan
        environment.

        Returns:
            :class:`pycpg.services.devices.DeviceService`
        """
        return self._clients.authority.devices

    @property
    def orgs(self):
        """A collection of methods for retrieving or updating data about organizations in the
        CrashPlan environment.

        Returns:
            :class:`pycpg.services.orgs.OrgService`
        """
        return self._clients.authority.orgs

    @property
    def legalhold(self):
        """A collection of methods for retrieving and updating legal-hold matters, policies, and
        custodians.

        Returns:
            :class:`pycpg.services.legalhold.LegalHoldService`
        """
        return self._clients.authority.legalhold

    @property
    def usercontext(self):
        """A collection of methods related to getting information about the currently logged in
        user, such as the tenant ID.

        Returns:
            :class:`pycpg.usercontext.UserContext`
        """
        return self._user_ctx

    @property
    def auditlogs(self):
        """A collection of methods for retrieving audit logs.

        Returns:
            :class:`pycpg.clients.auditlogs.AuditLogsClient`
        """
        return self._clients.auditlogs


def _init_services(main_connection, main_auth, auth_flag=None):
    # services are imported within function to prevent circular imports when a service
    # imports anything from pycpg.sdk.queries
    from pycpg.services import Services
    from pycpg.services._keyvaluestore import KeyValueStoreService
    from pycpg.services.administration import AdministrationService
    from pycpg.services.archive import ArchiveService
    from pycpg.services.auditlogs import AuditLogsService
    from pycpg.services.devices import DeviceService
    from pycpg.services.fileevent import FileEventService
    from pycpg.services.legalhold import LegalHoldService
    from pycpg.services.legalholdapiclient import LegalHoldApiClientService
    from pycpg.services.orgs import OrgService
    from pycpg.services.users import UserService


    kv_prefix = "simple-key-value-store"
    audit_logs_key = "AUDIT-LOG_API-URL"

    kv_connection = Connection.from_microservice_prefix(main_connection, kv_prefix)
    kv_service = KeyValueStoreService(kv_connection)

    audit_logs_conn = Connection.from_microservice_key(
        kv_service, audit_logs_key, auth=main_auth
    )
    administration_svc = AdministrationService(main_connection)

    user_ctx = UserContext(administration_svc)



    services = Services(
        administration=administration_svc,
        archive=ArchiveService(main_connection),
        devices=DeviceService(main_connection),
        # Only use updated legal hold client if initialized with API Client authorization
        legalhold=LegalHoldApiClientService(main_connection)
        if auth_flag
        else LegalHoldService(main_connection),
        orgs=OrgService(main_connection),
        users=UserService(main_connection),
        auditlogs=AuditLogsService(audit_logs_conn),
    )

    return services, user_ctx

def _init_clients(services, connection):
    # clients are imported within function to prevent circular imports when a client
    # imports anything from pycpg.sdk.queries
    from pycpg.clients import Clients
    from pycpg.clients._archiveaccess.accessorfactory import ArchiveAccessorFactory
    from pycpg.clients.archive import ArchiveClient
    from pycpg.clients.auditlogs import AuditLogsClient
    from pycpg.clients.authority import AuthorityClient
    from pycpg.clients.loginconfig import LoginConfigurationClient
    from pycpg.clients.securitydata import SecurityDataClient
    from pycpg.services.storage._service_factory import StorageServiceFactory

    authority = AuthorityClient(
        administration=services.administration,
        archive=services.archive,
        devices=services.devices,
        legalhold=services.legalhold,
        orgs=services.orgs,
        users=services.users,
    )
    storage_service_factory = StorageServiceFactory(connection, services.devices)
    securitydata = SecurityDataClient(
        storage_service_factory,
    )
    archive_accessor_factory = ArchiveAccessorFactory(
        services.archive, storage_service_factory
    )
    archive = ArchiveClient(archive_accessor_factory, services.archive)
    auditlogs = AuditLogsClient(services.auditlogs)
    loginconfig = LoginConfigurationClient(connection)
    clients = Clients(
        authority=authority,
        securitydata=securitydata,
        archive=archive,
        auditlogs=auditlogs,
        loginconfig=loginconfig
    )
    return clients
