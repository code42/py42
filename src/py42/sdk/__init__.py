from requests.auth import HTTPBasicAuth

from py42.clients import Clients
from py42.clients._archive_access import ArchiveAccessorManager
from py42.clients._storage import StorageClientFactory
from py42.clients.alertrules import AlertRulesClient
from py42.clients.alerts import AlertsClient
from py42.clients.archive import ArchiveClient
from py42.clients.authority import AuthorityClient
from py42.clients.detectionlists import DetectionListsClient
from py42.clients.securitydata import SecurityDataClient
from py42.services import Services
from py42.services._auth import V3Auth
from py42.services._connection import KeyValueStoreConnection
from py42.services._connection import KnownUrlConnection
from py42.services._connection import MicroserviceConnection
from py42.services._keyvaluestore import KeyValueStoreClient
from py42.services.administration import AdministrationService
from py42.services.alertrules import AlertRulesService
from py42.services.alerts import AlertService
from py42.services.archive import ArchiveService
from py42.services.detectionlists._profile import DetectionListUserService
from py42.services.detectionlists.departing_employee import DepartingEmployeeService
from py42.services.detectionlists.high_risk_employee import HighRiskEmployeeService
from py42.services.devices import DeviceService
from py42.services.fileevent import FileEventService
from py42.services.legalhold import LegalHoldService
from py42.services.orgs import OrgService
from py42.services.pds import PreservationDataService
from py42.services.savedsearch import SavedSearchService
from py42.services.securitydata import SecurityDataService
from py42.services.storage._connection_manager import ConnectionManager
from py42.services.users import UserService
from py42.usercontext import UserContext


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
    def __init__(self, clients, user_ctx):
        self._clients = clients
        self._user_ctx = user_ctx

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
        basic_auth = HTTPBasicAuth(username, password)
        basic_auth_connection = KnownUrlConnection(host_address, auth=basic_auth)
        auth = V3Auth(basic_auth_connection)
        authority_connection = KnownUrlConnection(host_address, auth=auth)
        services, user_ctx = _init_services(authority_connection, auth)
        clients = _init_clients(services, auth)

        # test credentials
        clients.authority.users.get_current()

        return cls(clients, user_ctx)

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
            * Alerts
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


def _init_services(authority_connection, main_auth):
    alert_rules_key = u"FedObserver-API_URL"
    alerts_key = u"AlertService-API_URL"
    file_events_key = u"FORENSIC_SEARCH-API_URL"
    preservation_data_key = u"PRESERVATION-DATA-SERVICE_API-URL"
    employee_case_mgmt_key = u"employeecasemanagement-API_URL"

    kv_connection = KeyValueStoreClient(KeyValueStoreConnection())

    def create_microservice_connection(key):
        return MicroserviceConnection(kv_connection, key, auth=main_auth)

    alert_rules_connection = create_microservice_connection(alert_rules_key)
    alerts_connection = create_microservice_connection(alerts_key)
    file_events_connection = create_microservice_connection(file_events_key)
    pds_connection = create_microservice_connection(preservation_data_key)
    ecm_connection = create_microservice_connection(employee_case_mgmt_key)
    user_svc = UserService(authority_connection)
    administration_svc = AdministrationService(authority_connection)
    file_events_service = FileEventService(file_events_connection)
    user_ctx = UserContext(administration_svc)
    user_profile_svc = DetectionListUserService(ecm_connection, user_ctx, user_svc)

    services = Services(
        administration=administration_svc,
        archive=ArchiveService(authority_connection),
        devices=DeviceService(authority_connection),
        legalhold=LegalHoldService(authority_connection),
        orgs=OrgService(authority_connection),
        securitydata=SecurityDataService(authority_connection),
        users=UserService(authority_connection),
        alertrules=AlertRulesService(
            alert_rules_connection, user_ctx, user_profile_svc
        ),
        alerts=AlertService(alerts_connection, user_ctx),
        filevents=file_events_service,
        savedsearch=SavedSearchService(file_events_connection, file_events_service),
        preservationdata=PreservationDataService(pds_connection),
        departingemployee=DepartingEmployeeService(
            ecm_connection, user_ctx, user_profile_svc
        ),
        highriskemployee=HighRiskEmployeeService(
            ecm_connection, user_ctx, user_profile_svc
        ),
        userprofile=user_profile_svc,
    )

    return services, user_ctx


def _init_clients(services, connection):
    authority = AuthorityClient(
        administration=services.administration,
        archive=services.archive,
        devices=services.devices,
        legalhold=services.legalhold,
        orgs=services.orgs,
        securitydata=services.securitydata,
        users=services.users,
    )
    detectionlists = DetectionListsClient(
        services.userprofile, services.departingemployee, services.highriskemployee
    )

    storage_client_factory = StorageClientFactory(
        connection, services.devices, ConnectionManager()
    )
    alertrules = AlertRulesClient(services.alerts, services.alertrules)
    securitydata = SecurityDataClient(
        services.securitydata, services.savedsearch, storage_client_factory
    )
    alerts = AlertsClient(services.alerts, alertrules)
    archive_accessor_mgr = ArchiveAccessorManager(
        services.archive, storage_client_factory
    )
    archive = ArchiveClient(archive_accessor_mgr, services.archive)
    clients = Clients(
        authority=authority,
        detectionlists=detectionlists,
        alerts=alerts,
        securitydata=securitydata,
        archive=archive,
    )
    return clients
