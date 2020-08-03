# import json
#
# from requests import HTTPError
#
# from py42.exceptions import Py42FeatureUnavailableError
# from py42.exceptions import Py42SessionInitializationError
# from py42.services import _key_value_store
# from py42.services import administration
# from py42.services import alerts
# from py42.services import archive
# from py42.services import devices
# from py42.services import legalhold
# from py42.services import orgs
# from py42.services import securitydata
# from py42.services import users
# from py42.services.alertrules import AlertRulesClient
# from py42.services.detectionlists._profile import DetectionListUserClient
# from py42.services.detectionlists.departing_employee import DepartingEmployeeClient
# from py42.services.detectionlists.high_risk_employee import HighRiskEmployeeClient
# from py42.services.file_event import FileEventClient
# from py42.services.pds import PreservationDataServiceClient
# from py42.services.savedsearch import SavedSearchClient
# from py42.services.storage.storagenode import StoragePreservationDataClient
#
#
# class AuthorityClient(object):
#     def __init__(self, connection):
#         self._connection = connection
#
#     def create_administration_client(self):
#         return administration.AdministrationClient(self._connection)
#
#     def create_user_client(self):
#         return users.UserClient(self._connection)
#
#     def create_device_client(self):
#         return devices.DeviceClient(self._connection)
#
#     def create_org_client(self):
#         return orgs.OrgClient(self._connection)
#
#     def create_legal_hold_client(self):
#         return legalhold.LegalHoldClient(self._connection)
#
#     def create_archive_client(self):
#         return archive.ArchiveClient(self._connection)
#
#     def create_security_client(self):
#         return securitydata.SecurityClient(self._connection)
#
#
# class MicroserviceClientFactory(object):
#     def __init__(
#         self,
#         root_session,
#         key_value_store_connection,
#         user_context,
#         user_client,
#     ):
#         self._root_session = root_session
#         self._user_context = user_context
#         self._user_client = user_client
#         self._key_value_store_connection = key_value_store_connection
#
#         self._alerts_client = None
#         self._departing_employee_client = None
#         self._file_event_client = None
#         self._high_risk_employee_client = None
#         self._detection_list_user_client = None
#         self._ecm_session = None
#         self._alert_rules_client = None
#         self._saved_search_client = None
#         self._file_event_session = None
#         self._pds_client = None
#
#     def get_alerts_client(self):
#         if not self._alerts_client:
#             connection = self._get_jwt_session(u"AlertService-API_URL")
#             self._alerts_client = alerts.AlertClient(connection, self._user_context)
#         return self._alerts_client
#
#     def get_departing_employee_client(self):
#         if not self._departing_employee_client:
#             self._departing_employee_client = DepartingEmployeeClient(
#                 self._get_ecm_session(),
#                 self._user_context,
#                 self.get_detection_list_user_client(),
#             )
#         return self._departing_employee_client
#
#     def get_file_event_client(self):
#         if not self._file_event_client:
#             self._file_event_client = FileEventClient(self._get_file_event_session())
#         return self._file_event_client
#
#     def get_high_risk_employee_client(self):
#         if not self._high_risk_employee_client:
#             self._high_risk_employee_client = HighRiskEmployeeClient(
#                 self._get_ecm_session(),
#                 self._user_context,
#                 self.get_detection_list_user_client(),
#             )
#         return self._high_risk_employee_client
#
#     def get_detection_list_user_client(self):
#         if not self._detection_list_user_client:
#             user_client = self._user_client
#             self._detection_list_user_client = DetectionListUserClient(
#                 self._get_ecm_session(), self._user_context, user_client
#             )
#         return self._detection_list_user_client
#
#     def get_alert_rules_client(self):
#         if not self._alert_rules_client:
#             connection = self._get_jwt_session(u"FedObserver-API_URL")
#             self._alert_rules_client = AlertRulesClient(
#                 connection, self._user_context, self.get_detection_list_user_client()
#             )
#         return self._alert_rules_client
#
#     def get_saved_search_client(self):
#         if not self._saved_search_client:
#             self._saved_search_client = SavedSearchClient(
#                 self._get_file_event_session(), self.get_file_event_client()
#             )
#         return self._saved_search_client
#
#     def get_preservation_data_service_client(self):
#         if not self._pds_client:
#             connection = self._get_jwt_session(u"PRESERVATION-DATA-SERVICE_API-URL")
#             self._pds_client = PreservationDataServiceClient(connection)
#         return self._pds_client
#
#     def create_storage_preservation_client(self, host_address):
#         main_session = self._session_factory.create_jwt_session(
#             host_address, self._root_session
#         )
#         streaming_session = self._session_factory.create_anonymous_session(host_address)
#         return StoragePreservationDataClient(main_session, streaming_session)
#
#     def _get_jwt_session(self, key):
#         url = self._get_stored_value(key)
#         return self._session_factory.create_jwt_session(url, self._root_session)
#
#     def _get_ecm_session(self):
#         if not self._ecm_session:
#             self._ecm_session = self._get_jwt_session(u"employeecasemanagement-API_URL")
#         return self._ecm_session
#
#     def _get_file_event_session(self):
#         if not self._file_event_session:
#             self._file_event_session = self._get_jwt_session(u"FORENSIC_SEARCH-API_URL")
#         return self._file_event_session
#
#     def _get_stored_value(self, key):
#         if not self._key_value_store_client:
#             url = _hacky_get_microservice_url(
#                 self._root_session, u"simple-key-value-store"
#             )
#             connection = self._session_factory.create_anonymous_session(url)
#             self._key_value_store_client = _key_value_store.KeyValueStoreClient(
#                 connection
#             )
#         return self._key_value_store_client.get_stored_value(key).text
