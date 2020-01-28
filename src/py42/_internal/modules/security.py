from py42._internal.client_factories import FileEventClientFactory, StorageClientFactory
from py42._internal.clients.security import SecurityClient, get_normalized_security_event_plan_info


class SecurityModule(object):
    def __init__(self, security_client, storage_client_factory, file_event_client_factory):
        # type: (SecurityClient, StorageClientFactory, FileEventClientFactory) -> None
        self._security_client = security_client
        self._storage_client_factory = storage_client_factory
        self._file_event_client_factory = file_event_client_factory

    def get_security_event_locations(self, user_uid):
        # unlike most api calls this does not return the response from /c42api/v3/SecurityEventsLocation in raw form.
        # This is because the format has changed between versions of the c42 authority and the response has to be
        # normalized.

        return get_normalized_security_event_plan_info(self._security_client, user_uid)

    def get_security_detection_event_client(self, plan_uid, destination_guid):
        return self._storage_client_factory.get_storage_client_from_plan_uid(
            plan_uid, destination_guid
        ).security

    def search_file_events(self, query, then=None, **kwargs):
        """Searches for file events

        Args:
            query: raw JSON query or FileEventQuery object. See https://support.code42.com/Administrator/Cloud/Monitoring_and_managing/Forensic_File_Search_API
            then: function to call with the result

        Returns:
            list of file events as JSON
        """
        file_event_client = self._file_event_client_factory.get_file_event_client()
        return file_event_client.search_file_events(query, then=then, **kwargs)
