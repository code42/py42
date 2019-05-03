import py42.util as util
from py42._internal.clients.security import SecurityClient
from py42._internal.client_factories import StorageClientFactory, FileEventClientFactory


class SecurityModule(object):
    def __init__(self, security_client, storage_client_factory, file_event_client_factory):
        # type: (SecurityClient, StorageClientFactory, FileEventClientFactory) -> None
        self._security_client = security_client
        self._storage_client_factory = storage_client_factory
        self._file_event_client_factory = file_event_client_factory

    def get_security_event_locations(self, user_uid, catch=None, **kwargs):
        storage_clients = self._storage_client_factory.create_security_plan_clients(user_uid=user_uid, catch=catch)
        client_calls = [client.security.get_security_detection_events for client in storage_clients]
        return self._return_first_successful_result(client_calls, user_uid=user_uid, catch=catch, **kwargs)

    def get_security_detection_events_for_user(self, user_uid, cursor=None, include_files=None, event_types=None,
                                               min_timestamp=None, max_timestamp=None, **kwargs):

        return self.get_security_event_locations(user_uid=user_uid, cursor=cursor,
                                                 include_files=include_files,
                                                 event_types=event_types,
                                                 min_timestamp=min_timestamp,
                                                 max_timestamp=max_timestamp, **kwargs)

    def get_security_detection_event_summary(self, user_uid, cursor=None, include_files=None, event_types=None,
                                             min_timestamp=None, max_timestamp=None, **kwargs):

        return self.get_security_event_locations(user_uid=user_uid, cursor=cursor,
                                                 include_files=include_files, event_types=event_types,
                                                 min_timestamp=min_timestamp, max_timestamp=max_timestamp,
                                                 summarize=True, **kwargs)

    def search_file_events(self, query, then=None, catch=None, **kwargs):
        """Search for file events
        :param query: raw JSON query. See https://support.code42.com/Administrator/Cloud/Monitoring_and_managing/Forensic_File_Search_API
        :param then: function to call with the result
        :param catch: function to call with an exception of one occurrs
        :return: list of file events as JSON
        """
        file_event_client = self._file_event_client_factory.create_file_event_client()
        return file_event_client.search_file_events(query, then=then, catch=catch, **kwargs)

    def _return_first_successful_result(self, func_list, catch=None, *args, **kwargs):
        if len(func_list):
            func = func_list[0]

            def catch_and_try_next(ex):
                func_list.remove(func)
                if len(func_list):
                    self._return_first_successful_result(func_list, *args, **kwargs)

            catch = util.wrap_func(catch_and_try_next, catch)
            result = func(catch=catch, *args, **kwargs)
            return result
