from requests.auth import HTTPBasicAuth

from py42.clients import Clients
from py42.clients.alerts import AlertsModule
from py42.clients.authority import AuthorityClient
from py42.clients.detectionlists import DetectionListsModule
from py42.clients.securitydata import SecurityModule
from py42.services import Services
from py42.services._auth import V3Auth
from py42.services._connection import KeyValueStoreConnection
from py42.services._connection import KnownUrlConnection
from py42.services._connection import MicroserviceConnection
from py42.services._key_value_store import KeyValueStoreClient
from py42.services.administration import AdministrationClient
from py42.services.alertrules import AlertRulesClient
from py42.services.alerts import AlertClient
from py42.services.archive import ArchiveClient
from py42.services.detectionlists._profile import DetectionListUserClient
from py42.services.detectionlists.departing_employee import DepartingEmployeeClient
from py42.services.detectionlists.high_risk_employee import HighRiskEmployeeClient
from py42.services.devices import DeviceClient
from py42.services.file_event import FileEventClient
from py42.services.legalhold import LegalHoldClient
from py42.services.orgs import OrgClient
from py42.services.pds import PreservationDataServiceClient
from py42.services.savedsearch import SavedSearchClient
from py42.services.securitydata import SecurityClient
from py42.services.users import UserClient
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
        services, user_ctx = _init_services(basic_auth_connection, host_address)
        clients = _init_clients(services)

        return cls(clients, user_ctx)

    @property
    def serveradmin(self):
        """A collection of methods for getting server information for on-premise environments
        and tenant information for cloud environments.

        Returns:
            :class:`py42.services.administration.AdministrationClient`
        """
        return self._clients.authority.administration

    @property
    def archive(self):
        """A collection of methods for accessing Code42 storage archives. Useful for doing
        web-restores or finding a file on an archive.

        Returns:
            :class:`py42.clients.archive.ArchiveModule`
        """
        pass
        # return self._clients.archive

    @property
    def users(self):
        """A collection of methods for retrieving or updating data about users in the Code42
        environment.

        Returns:
            :class:`py42.services.users.UserClient`
        """
        return self._clients.authority.users

    @property
    def devices(self):
        """A collection of methods for retrieving or updating data about devices in the Code42
        environment.

        Returns:
            :class:`py42.services.devices.DeviceClient`
        """
        return self._clients.authority.devices

    @property
    def orgs(self):
        """A collection of methods for retrieving or updating data about organizations in the
        Code42 environment.

        Returns:
            :class:`py42.services.orgs.OrgClient`
        """
        return self._clients.authority.orgs

    @property
    def legalhold(self):
        """A collection of methods for retrieving and updating legal-hold matters, policies, and
        custodians.

        Returns:
            :class:`py42.services.legalhold.LegalHoldClient`
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
            :class:`py42.clients.securitydata.SecurityModule`
        """
        pass
        # return self._clients.securitydata

    @property
    def detectionlists(self):
        """A collection of properties each containing methods for managing specific detection
        lists, such as departing employees.

        Returns:
            :class:`py42.clients.detectionlists.DetectionListsModule`
        """
        return self._clients.detectionlists

    @property
    def alerts(self):
        """A collection of methods related to retrieving and updating alerts rules.

        Returns:
            :class:`py42.clients.alertrules.AlertRulesModule`
        """
        return self._clients.alerts


def _init_services(root_connection, host_address):
    ALERT_RULES_KEY = u"FedObserver-API_URL"
    ALERTS_KEY = u"AlertService-API_URL"
    FILE_EVENTS_KEY = u"FORENSIC_SEARCH-API_URL"
    PRESERVATION_DATA_KEY = u"PRESERVATION-DATA-SERVICE_API-URL"
    EMPLOYEE_CASE_MGMT_KEY = u"employeecasemanagement-API_URL"

    main_auth = V3Auth(root_connection)
    kv_connection = KeyValueStoreClient(KeyValueStoreConnection())

    def create_microservice_connection(key):
        return MicroserviceConnection(kv_connection, key, auth=main_auth)

    authority_connection = KnownUrlConnection(host_address, auth=main_auth)
    alert_rules_connection = create_microservice_connection(ALERT_RULES_KEY)
    alerts_connection = create_microservice_connection(ALERTS_KEY)
    file_events_connection = create_microservice_connection(FILE_EVENTS_KEY)
    pds_connection = create_microservice_connection(PRESERVATION_DATA_KEY)
    ecm_connection = create_microservice_connection(EMPLOYEE_CASE_MGMT_KEY)
    user_svc = UserClient(authority_connection)
    administration_svc = AdministrationClient(authority_connection)
    file_events_service = FileEventClient(file_events_connection)
    user_ctx = UserContext(administration_svc)
    user_profile_svc = DetectionListUserClient(ecm_connection, user_ctx, user_svc)

    services = Services(
        administration=administration_svc,
        archive=ArchiveClient(authority_connection),
        devices=DeviceClient(authority_connection),
        legalhold=LegalHoldClient(authority_connection),
        orgs=OrgClient(authority_connection),
        securitydata=SecurityClient(authority_connection),
        users=UserClient(authority_connection),
        alertrules=AlertRulesClient(alert_rules_connection, user_ctx, user_profile_svc),
        alerts=AlertClient(alerts_connection, user_ctx),
        filevents=file_events_service,
        savedsearch=SavedSearchClient(file_events_connection, file_events_service),
        preservationdata=PreservationDataServiceClient(pds_connection),
        departingemployee=DepartingEmployeeClient(ecm_connection, user_ctx, user_profile_svc),
        highriskemployee=HighRiskEmployeeClient(ecm_connection, user_ctx, user_profile_svc),
        userprofile=user_profile_svc,
    )

    return services, user_ctx


def _init_clients(services):
    authority = AuthorityClient(administration=services.administration,
                                archive=services.archive,
                                devices=services.devices,
                                legalhold=services.legalhold,
                                orgs=services.orgs,
                                securitydata=services.securitydata,
                                users=services.users
                                )
    # securitydata = SecurityModule()
    detectionlists = DetectionListsModule(services.userprofile,
                                          services.departingemployee,
                                          services.highriskemployee)

    securitydata = SecurityModule(services.securitydata, None)
    alerts = AlertsModule(services.alerts, services.alertrules)
    clients = Clients(authority=authority, detectionlists=detectionlists, alerts=alerts, securitydata=None, archive=None)
    return clients
