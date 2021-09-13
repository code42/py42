from requests.auth import HTTPBasicAuth

from py42.clients import Clients
from py42.clients._archiveaccess.accessorfactory import ArchiveAccessorFactory
from py42.clients.alertrules import AlertRulesClient
from py42.clients.alerts import AlertsClient
from py42.clients.archive import ArchiveClient
from py42.clients.auditlogs import AuditLogsClient
from py42.clients.authority import AuthorityClient
from py42.clients.cases import CasesClient
from py42.clients.detectionlists import DetectionListsClient
from py42.clients.loginconfig import LoginConfigurationClient
from py42.clients.securitydata import SecurityDataClient
from py42.clients.trustedactivities import TrustedActivitiesClient
from py42.exceptions import Py42Error
from py42.exceptions import Py42UnauthorizedError
from py42.services import Services
from py42.services._auth import BearerAuth
from py42.services._auth import CustomJWTAuth
from py42.services._connection import Connection
from py42.services._keyvaluestore import KeyValueStoreService
from py42.services.administration import AdministrationService
from py42.services.alertrules import AlertRulesService
from py42.services.alerts import AlertService
from py42.services.archive import ArchiveService
from py42.services.auditlogs import AuditLogsService
from py42.services.cases import CasesService
from py42.services.casesfileevents import CasesFileEventsService
from py42.services.detectionlists.departing_employee import DepartingEmployeeService
from py42.services.detectionlists.high_risk_employee import HighRiskEmployeeService
from py42.services.detectionlists.user_profile import DetectionListUserService
from py42.services.devices import DeviceService
from py42.services.fileevent import FileEventService
from py42.services.legalhold import LegalHoldService
from py42.services.orgs import OrgService
from py42.services.preservationdata import PreservationDataService
from py42.services.savedsearch import SavedSearchService
from py42.services.storage._service_factory import ConnectionManager
from py42.services.storage._service_factory import StorageServiceFactory
from py42.services.trustedactivities import TrustedActivitiesService
from py42.services.users import UserService
from py42.usercontext import UserContext


def from_local_account(host_address, username, password, totp=None):
    """Creates a :class:`~py42.sdk.SDKClient` object for accessing the Code42 REST APIs using the
    supplied credentials. This method supports only accounts created within the Code42 console or using the
    APIs (including py42). Username/passwords that are based on Active Directory,
    Okta, or other Identity providers cannot be used with this method.

    Args:
        host_address (str): The domain name of the Code42 instance being authenticated to, e.g.
            console.us.code42.com
        username (str): The username of the authenticating account.
        password (str): The password of the authenticating account.
        totp (callable or str, optional): The time-based one-time password of the authenticating account. Include only
            if the account uses Code42's two-factor authentication. Defaults to None.

    Returns:
        :class:`py42.sdk.SDKClient`
    """
    client = SDKClient.from_local_account(host_address, username, password, totp)

    # test credentials
    try:
        client.users.get_current()
    except Py42UnauthorizedError as err:
        login_type = client.loginconfig.get_for_user(username)["loginType"]
        if login_type == "CLOUD_SSO":
            raise Py42Error("SSO users are not supported in `from_local_account()`.")
        msg = f"SDK initialization failed, double-check username/password, and provide two-factor TOTP token if Multi-Factor Auth configured for your user. User LoginConfig: {login_type}"
        err.args = (msg,)
        raise
    return client


def from_jwt_provider(host_address, jwt_provider):
    """Creates a :class:`~py42.sdk.SDKClient` object for accessing the Code42 REST APIs using a custom
    auth mechanism. User can use any authentication mechanism like that returns a JSON Web token on authentication
    which would then be used for all subsequent requests.

    Args:
        host_address (str): The domain name of the Code42 instance being authenticated to, e.g.
            console.us.code42.com
        jwt_provider (function): A function that accepts no parameters and on execution returns a JSON web token string.

    Returns:
        :class:`py42.sdk.SDKClient`
    """

    client = SDKClient.from_jwt_provider(host_address, jwt_provider)
    client.users.get_current()
    return client


class SDKClient:
    def __init__(self, main_connection, auth):
        services, user_ctx = _init_services(main_connection, auth)
        self._clients = _init_clients(services, main_connection)
        self._user_ctx = user_ctx

    @classmethod
    def from_local_account(cls, host_address, username, password, totp=None):
        """Creates a :class:`~py42.sdk.SDKClient` object for accessing the Code42 REST APIs using
        the supplied credentials. This method supports only accounts created within the Code42 console or
        using the APIs (including py42). Username/passwords that are based on Active
        Directory, Okta, or other Identity providers should use the `from_jwt_provider` method.

        Args:
            host_address (str): The domain name of the Code42 instance being authenticated to, e.g.
                console.us.code42.com
            username (str): The username of the authenticating account.
            password (str): The password of the authenticating account.
            totp (callable or str, optional): The time-based one-time password of the authenticating account. Include only
                if the account uses Code42's two-factor authentication. Defaults to None.
        Returns:
            :class:`py42.sdk.SDKClient`
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
        """Creates a :class:`~py42.sdk.SDKClient` object for accessing the Code42 REST APIs using a custom
            auth mechanism. User can use any authentication mechanism like that returns a JSON Web token
            on authentication which would then be used for all subsequent requests.

        Args:
            host_address (str): The domain name of the Code42 instance being authenticated to, e.g.
                console.us.code42.com
            jwt_provider (function): A function that accepts no parameters and on execution returns a
            JSON web token string.

        Returns:
            :class:`py42.sdk.SDKClient`
        """
        custom_auth = CustomJWTAuth(jwt_provider)
        main_connection = Connection.from_host_address(host_address, auth=custom_auth)

        return cls(main_connection, custom_auth)

    @property
    def loginconfig(self):
        """A collection of methods related to getting information about the login configuration
        of user accounts.

        Returns:
            :class:`py42.clients.loginconfig.LoginConfigurationClient.`
        """
        return self._clients.loginconfig

    @property
    def serveradmin(self):
        """A collection of methods for getting server information for on-premise environments
        and tenant information for cloud environments.

        Returns:
            :class:`py42.services.administration.AdministrationService`
        """
        return self._clients.authority.administration

    @property
    def archive(self):
        """A collection of methods for accessing Code42 storage archives. Useful for doing
        web-restores or finding a file on an archive.

        Returns:
            :class:`py42.clients.archive.ArchiveClient`
        """
        return self._clients.archive

    @property
    def users(self):
        """A collection of methods for retrieving or updating data about users in the Code42
        environment.

        Returns:
            :class:`py42.services.users.UserService`
        """
        return self._clients.authority.users

    @property
    def devices(self):
        """A collection of methods for retrieving or updating data about devices in the Code42
        environment.

        Returns:
            :class:`py42.services.devices.DeviceService`
        """
        return self._clients.authority.devices

    @property
    def orgs(self):
        """A collection of methods for retrieving or updating data about organizations in the
        Code42 environment.

        Returns:
            :class:`py42.services.orgs.OrgService`
        """
        return self._clients.authority.orgs

    @property
    def legalhold(self):
        """A collection of methods for retrieving and updating legal-hold matters, policies, and
        custodians.

        Returns:
            :class:`py42.services.legalhold.LegalHoldService`
        """
        return self._clients.authority.legalhold

    @property
    def usercontext(self):
        """A collection of methods related to getting information about the currently logged in
        user, such as the tenant ID.

        Returns:
            :class:`py42.usercontext.UserContext`
        """
        return self._user_ctx

    @property
    def securitydata(self):
        """A collection of methods and properties for getting security data such as:
            * File events
            * Security plan information

        Returns:
            :class:`py42.clients.securitydata.SecurityDataClient`
        """
        return self._clients.securitydata

    @property
    def detectionlists(self):
        """A collection of properties each containing methods for managing specific detection
        lists, such as departing employees.

        Returns:
            :class:`py42.clients.detectionlists.DetectionListsClient`
        """
        return self._clients.detectionlists

    @property
    def alerts(self):
        """A collection of methods related to retrieving and updating alerts rules.

        Returns:
            :class:`py42.clients.alertrules.AlertRulesClient`
        """
        return self._clients.alerts

    @property
    def auditlogs(self):
        """A collection of methods for retrieving audit logs.

        Returns:
            :class:`py42.clients.auditlogs.AuditLogsClient`
        """
        return self._clients.auditlogs

    @property
    def cases(self):
        """A collection of methods and properties for managing cases and file events
        associated with the case.

        Returns:
            :class:`py42.clients.cases.CaseClient`
        """
        return self._clients.cases

    @property
    def trustedactivities(self):
        """A collection of methods and properties for managing trusted domains.

        Returns:
            :class:`py42.clients.trustedactivities.TrustedActivitiesClient`
        """
        return self._clients.trustedactivities


def _init_services(main_connection, main_auth):
    alert_rules_key = "FedObserver-API_URL"
    alerts_key = "AlertService-API_URL"
    file_events_key = "FORENSIC_SEARCH-API_URL"
    preservation_data_key = "PRESERVATION-DATA-SERVICE_API-URL"
    employee_case_mgmt_key = "employeecasemanagementV2-API_URL"
    kv_prefix = "simple-key-value-store"
    audit_logs_key = "AUDIT-LOG_API-URL"
    cases_key = "CASES_API-URL"
    trusted_activities_key = "TRUSTED-DOMAINS_API-URL"

    kv_connection = Connection.from_microservice_prefix(main_connection, kv_prefix)
    kv_service = KeyValueStoreService(kv_connection)

    alert_rules_conn = Connection.from_microservice_key(
        kv_service, alert_rules_key, auth=main_auth
    )
    alerts_conn = Connection.from_microservice_key(
        kv_service, alerts_key, auth=main_auth
    )
    file_events_conn = Connection.from_microservice_key(
        kv_service, file_events_key, auth=main_auth
    )
    pds_conn = Connection.from_microservice_key(
        kv_service, preservation_data_key, auth=main_auth
    )
    ecm_conn = Connection.from_microservice_key(
        kv_service, employee_case_mgmt_key, auth=main_auth
    )
    audit_logs_conn = Connection.from_microservice_key(
        kv_service, audit_logs_key, auth=main_auth
    )
    user_svc = UserService(main_connection)
    administration_svc = AdministrationService(main_connection)
    file_event_svc = FileEventService(file_events_conn)
    user_ctx = UserContext(administration_svc)
    user_profile_svc = DetectionListUserService(ecm_conn, user_ctx, user_svc)
    cases_conn = Connection.from_microservice_key(kv_service, cases_key, auth=main_auth)
    trusted_activities_conn = Connection.from_microservice_key(
        kv_service, trusted_activities_key, auth=main_auth
    )

    services = Services(
        administration=administration_svc,
        archive=ArchiveService(main_connection),
        devices=DeviceService(main_connection),
        legalhold=LegalHoldService(main_connection),
        orgs=OrgService(main_connection),
        users=UserService(main_connection),
        alertrules=AlertRulesService(alert_rules_conn, user_ctx, user_profile_svc),
        alerts=AlertService(alerts_conn, user_ctx),
        fileevents=file_event_svc,
        savedsearch=SavedSearchService(file_events_conn, file_event_svc),
        preservationdata=PreservationDataService(pds_conn),
        departingemployee=DepartingEmployeeService(
            ecm_conn, user_ctx, user_profile_svc
        ),
        highriskemployee=HighRiskEmployeeService(ecm_conn, user_ctx, user_profile_svc),
        userprofile=user_profile_svc,
        auditlogs=AuditLogsService(audit_logs_conn),
        cases=CasesService(cases_conn),
        casesfileevents=CasesFileEventsService(cases_conn),
        trustedactivities=TrustedActivitiesService(trusted_activities_conn),
    )

    return services, user_ctx


def _init_clients(services, connection):
    authority = AuthorityClient(
        administration=services.administration,
        archive=services.archive,
        devices=services.devices,
        legalhold=services.legalhold,
        orgs=services.orgs,
        users=services.users,
    )
    detectionlists = DetectionListsClient(
        services.userprofile, services.departingemployee, services.highriskemployee
    )
    storage_service_factory = StorageServiceFactory(
        connection, services.devices, ConnectionManager()
    )
    alertrules = AlertRulesClient(services.alerts, services.alertrules)
    securitydata = SecurityDataClient(
        services.fileevents,
        services.preservationdata,
        services.savedsearch,
        storage_service_factory,
    )
    alerts = AlertsClient(services.alerts, alertrules)
    archive_accessor_factory = ArchiveAccessorFactory(
        services.archive, storage_service_factory
    )
    archive = ArchiveClient(archive_accessor_factory, services.archive)
    auditlogs = AuditLogsClient(services.auditlogs)
    loginconfig = LoginConfigurationClient(connection)
    trustedactivities = TrustedActivitiesClient(services.trustedactivities)
    clients = Clients(
        authority=authority,
        detectionlists=detectionlists,
        alerts=alerts,
        securitydata=securitydata,
        archive=archive,
        auditlogs=auditlogs,
        cases=CasesClient(services.cases, services.casesfileevents),
        loginconfig=loginconfig,
        trustedactivities=trustedactivities,
    )
    return clients
