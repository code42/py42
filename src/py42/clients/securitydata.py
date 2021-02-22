from threading import Lock

from py42.exceptions import Py42ChecksumNotFoundError
from py42.exceptions import Py42Error
from py42.exceptions import Py42HTTPError
from py42.exceptions import Py42NotFoundError
from py42.exceptions import Py42SecurityPlanConnectionError
from py42.sdk.queries.fileevents.file_event_query import FileEventQuery
from py42.sdk.queries.fileevents.filters.file_filter import MD5
from py42.sdk.queries.fileevents.filters.file_filter import SHA256


class SecurityDataClient(object):
    def __init__(
        self,
        security_service,
        file_event_service,
        preservation_data_service,
        saved_search_service,
        storage_service_factory,
    ):
        self._security_service = security_service
        self._file_event_service = file_event_service
        self._preservation_data_service = preservation_data_service
        self._saved_search_service = saved_search_service
        self._storage_service_factory = storage_service_factory
        self._client_cache = {}
        self._client_cache_lock = Lock()

    @property
    def savedsearches(self):
        """A collection of methods related to retrieving forensic search data.

        Returns:
            :class: `py42._internal.services.securitydata.SavedSearchService`
        """
        return self._saved_search_service

    def get_security_plan_storage_info_list(self, user_uid):
        """Gets IDs (plan UID, node GUID, and destination GUID) for the storage nodes containing
        the file activity event data for the user with the given UID.
        `REST Documentation <https://console.us.code42.com/swagger/#/Feature/getStorageNode>`__

        Args:
            user_uid (str): The UID of the user to get plan storage information for.

        Returns:
            list[:class:`py42.clients.securitydata.PlanStorageInfo`]
        """
        response = None
        locations = None
        try:
            response = self._security_service.get_security_event_locations(user_uid)
            locations = response[u"securityPlanLocationsByDestination"]
        except Py42NotFoundError:
            pass

        if response and locations:
            plan_destination_map = _get_plan_destination_map(locations)
            selected_plan_infos = self._get_plan_storage_infos(plan_destination_map)
            if not selected_plan_infos:
                raise Py42SecurityPlanConnectionError(
                    response,
                    u"Could not establish a connection to retrieve "
                    u"security events for user {}".format(user_uid),
                )

            return selected_plan_infos

    def get_all_plan_security_events(
        self,
        plan_storage_info,
        cursor=None,
        include_files=True,
        event_types=None,
        min_timestamp=None,
        max_timestamp=None,
    ):
        """Gets events for legacy Endpoint Monitoring file activity on removable media, in cloud
        sync folders, and browser uploads.
        `Support Article <https://support.code42.com/Administrator/6/Configuring/Endpoint_monitoring>`__

        Args:
            plan_storage_info (:class:`py42.clients.securitydata.PlanStorageInfo`):
                Information about storage nodes for a plan to get file event activity for.
            cursor (str, optional): A cursor position for only getting file events you did not
                previously get. Defaults to None.
            include_files (bool, optional): Whether to include the files related to the file events.
            Defaults to None.
            event_types: (str, optional): A comma-separated list of event types to filter by.

                    Available options are:
                        - ``DEVICE_APPEARED``
                        - ``DEVICE_DISAPPEARED``
                        - ``DEVICE_FILE_ACTIVITY``
                        - ``PERSONAL_CLOUD_FILE_ACTIVITY``
                        - ``RESTORE_JOB``
                        - ``RESTORE_FILE``
                        - ``FILE_OPENED``
                        - ``RULE_MATCH``
                        - ``DEVICE_SCAN_RESULT``
                        - ``PERSONAL_CLOUD_SCAN_RESULT``

                    Defaults to None.
            min_timestamp (int or float or str or datetime, optional): Timestamp in milliseconds or
                str format "yyyy-MM-DD HH:MM:SS" or a datetime instance. Defaults to None.
            max_timestamp (int or float or str or datetime, optional): Timestamp in milliseconds or
                str format "yyyy-MM-DD HH:MM:SS" or a datetime instance. Defaults to None.

        Returns:
            generator: An object that iterates over tuples whose first element is a :class:`py42.response.Py42Response` object
            containing a page of events, and whose second element is a string cursor.
        """
        return self._get_security_detection_events(
            plan_storage_info,
            cursor,
            include_files,
            event_types,
            min_timestamp,
            max_timestamp,
        )

    def get_all_user_security_events(
        self,
        user_uid,
        cursor=None,
        include_files=True,
        event_types=None,
        min_timestamp=None,
        max_timestamp=None,
    ):
        """Gets legacy Endpoint Monitoring file activity events for the user with the given UID.

        Args:
            user_uid (str): The UID of the user to get security events for.
            cursor (str, optional): A cursor position for only getting events you did not
                previously get. Defaults to None.
            include_files (bool, optional): Whether to include the files related to the file
                activity events. Defaults to None.
            event_types: (str, optional): A comma-separated list of event types to filter by.

                    Available options are:
                        - ``DEVICE_APPEARED``
                        - ``DEVICE_DISAPPEARED``
                        - ``DEVICE_FILE_ACTIVITY``
                        - ``PERSONAL_CLOUD_FILE_ACTIVITY``
                        - ``RESTORE_JOB``
                        - ``RESTORE_FILE``
                        - ``FILE_OPENED``
                        - ``RULE_MATCH``
                        - ``DEVICE_SCAN_RESULT``
                        - ``PERSONAL_CLOUD_SCAN_RESULT``

                    Defaults to None.
            min_timestamp (int or float or str or datetime, optional): Timestamp in milliseconds or
                str format "yyyy-MM-DD HH:MM:SS" or a datetime instance. Defaults to None.
            max_timestamp (int or float or str or datetime, optional): Timestamp in milliseconds or
                str format "yyyy-MM-DD HH:MM:SS" or a datetime instance. Defaults to None.

        Returns:
            generator: An object that iterates over tuples whose first element is a :class:`py42.response.Py42Response` object
            containing a page of events, and whose second element is a string cursor.
        """
        security_plan_storage_infos = self.get_security_plan_storage_info_list(user_uid)
        return self._get_security_detection_events(
            security_plan_storage_infos,
            cursor,
            include_files,
            event_types,
            min_timestamp,
            max_timestamp,
        )

    def search_file_events(self, query):
        """Searches for file events, returns up to the first 10,000 events.
        `REST Documentation <https://developer.code42.com/api/#operation/searchEventsUsingPOST>`__

        Args:
            query (str or :class:`py42.sdk.queries.fileevents.file_event_query.FileEventQuery`):
                The file event query to filter search results.

        Returns:
            :class:`py42.response.Py42Response`: A response containing the first 10,000
            events.
        """
        return self._file_event_service.search(query)

    def search_all_file_events(self, query, page_token=""):
        """Searches for all file events, returning a page of events with a token in the response to retrieve next page.
        `REST Documentation <https://developer.code42.com/api/#operation/searchEventsUsingPOST>`__

        Args:
            query (str or :class:`py42.sdk.queries.fileevents.file_event_query.FileEventQuery`):
                The file event query to filter search results.
            page_token (str, optional): A token used to indicate the starting point for
                additional page results. For the first page, do not pass ``page_token``. For
                all consecutive pages, pass the token from the previous response from
                field ``nextPgToken``. When using ``page_token``, any sorting parameters from
                the `FileEventQuery` will be ignored. Defaults to empty string.

        Returns:
            :class:`py42.response.Py42Response`: A response containing page of events.
        """

        query.page_token = page_token
        response = self._file_event_service.search(query)
        return response

    def stream_file_by_sha256(self, checksum):
        """Stream file based on SHA256 checksum.

        Args:
            checksum (str): SHA256 hash of the file.

        Returns:
            Returns a stream of the requested file.
        """
        response = self._search_by_hash(checksum, SHA256)
        events = response[u"fileEvents"]
        info = _get_version_lookup_info(events)
        if not len(events) or not info:
            raise Py42ChecksumNotFoundError(response, u"SHA256", checksum)
        return self._stream_file(checksum, info)

    def stream_file_by_md5(self, checksum):
        """Stream file based on MD5 checksum.

        Args:
            checksum (str): MD5 hash of the file.

        Returns:
            Returns a stream of the requested file.
        """
        response = self._search_by_hash(checksum, MD5)
        events = response[u"fileEvents"]
        info = _get_version_lookup_info(events)
        if not len(events) or not info:
            raise Py42ChecksumNotFoundError(response, u"MD5", checksum)
        return self._stream_file(checksum, info)

    def _search_by_hash(self, checksum, checksum_type):
        query = FileEventQuery.all(checksum_type.eq(checksum))
        query.sort_key = u"eventTimestamp"
        query.sort_direction = u"desc"
        response = self.search_file_events(query)
        return response

    def _stream_file(self, checksum, version_info):
        (device_guid, md5_hash, sha256_hash, path) = version_info
        version = self._get_file_version_for_stream(
            device_guid, md5_hash, sha256_hash, path
        )
        if version:
            pds = self._storage_service_factory.create_preservation_data_service(
                version[u"storageNodeURL"]
            )
            token = pds.get_download_token(
                version[u"archiveGuid"],
                version[u"fileId"],
                version[u"versionTimestamp"],
            )
            return pds.get_file(str(token))

        raise Py42Error(
            u"No file with hash {} available for download on any storage node.".format(
                checksum
            )
        )

    def _get_file_version_for_stream(self, device_guid, md5_hash, sha256_hash, path):
        version = self._get_device_file_version(
            device_guid, md5_hash, sha256_hash, path
        )
        if not version:
            version = self._get_other_file_location_version(md5_hash, sha256_hash)
        return version

    def _get_device_file_version(self, device_guid, md5_hash, sha256_hash, path):
        response = self._preservation_data_service.get_file_version_list(
            device_guid, md5_hash, sha256_hash, path
        )
        versions = response[u"versions"]
        if versions:
            exact_match = next(
                (
                    x
                    for x in versions
                    if x[u"fileMD5"] == md5_hash and x[u"fileSHA256"] == sha256_hash
                ),
                None,
            )
            if exact_match:
                return exact_match

            most_recent = sorted(
                versions, key=lambda i: i[u"versionTimestamp"], reverse=True
            )
            return most_recent[0]

    def _get_other_file_location_version(self, md5_hash, sha256_hash):
        response = self._file_event_service.get_file_location_detail_by_sha256(
            sha256_hash
        )
        locations = response[u"locations"]
        if locations:
            paths = _parse_file_location_response(locations)
            version = self._preservation_data_service.find_file_version(
                md5_hash, sha256_hash, paths
            )
            if version.status_code != 204:
                return version

    def _get_plan_storage_infos(self, plan_destination_map):
        plan_infos = []
        for plan_uid in plan_destination_map:
            destinations = plan_destination_map[plan_uid]
            storage_info = self._get_storage_info_for_plan(plan_uid, destinations)
            if storage_info:
                plan_infos.append(storage_info)

        return plan_infos

    def _get_storage_info_for_plan(self, plan_uid, destinations):
        for destination in destinations:
            # try to connect to every storage node for this plan until one works
            plan_storage_info = self._get_storage_info_for_plan_destination(
                plan_uid, destination
            )
            if plan_storage_info:
                return plan_storage_info

    def _get_storage_info_for_plan_destination(self, plan_uid, destination):
        try:
            destination_guid = destination[u"destinationGuid"]
            node_guid = destination[u"nodeGuid"]
            plan_storage_info = PlanStorageInfo(plan_uid, destination_guid, node_guid)
            self._try_get_security_detection_event_client(plan_storage_info)
            return plan_storage_info
        except Py42HTTPError:
            #  This function is called in a loop until we get a result that is not None.
            #  If all return None, then the calling function raises Py42SecurityPlanConnectionError.
            pass

    def _try_get_security_detection_event_client(self, plan_storage_info):
        # check if we have already created and stored this client
        client = self._client_cache.get(plan_storage_info.node_guid)

        # otherwise, create it
        if client is None:
            client = self._storage_service_factory.create_security_data_service(
                plan_storage_info.plan_uid, plan_storage_info.destination_guid
            )

            # store this client via its guid so that we don't have to call StorageAuthToken
            # just to determine what storage client to use
            with self._client_cache_lock:
                self._client_cache.update({plan_storage_info.node_guid: client})

        return client

    def _get_security_detection_events(
        self,
        plan_storage_infos,
        cursor,
        include_files,
        event_types,
        min_timestamp,
        max_timestamp,
    ):
        if not isinstance(plan_storage_infos, (list, tuple)):
            plan_storage_infos = [plan_storage_infos]

        # get the storage node client for each plan
        for plan_storage_info in plan_storage_infos:
            client = self._try_get_security_detection_event_client(plan_storage_info)
            started = False

            # get all pages of events for this plan
            while cursor or not started:
                started = True
                response = client.get_plan_security_events(
                    plan_storage_info.plan_uid,
                    cursor=cursor,
                    include_files=include_files,
                    event_types=event_types,
                    min_timestamp=min_timestamp,
                    max_timestamp=max_timestamp,
                )

                if response.text:
                    cursor = response.data.get(u"cursor")
                    # if there are no results, we don't get a cursor and have reached the end
                    if cursor:
                        yield response, cursor


def _get_plan_destination_map(locations_list):
    plan_destination_map = {}
    for plans in _get_destinations_in_locations_list(locations_list):
        for plan_uid in plans:
            plan_destination_map[plan_uid] = plans[plan_uid]
    return plan_destination_map


def _get_destinations_in_locations_list(locations_list):
    for destination in locations_list:
        for node in destination[u"securityPlanLocationsByNode"]:
            yield _get_plans_in_node(destination, node)


def _get_plans_in_node(destination, node):
    return {
        plan_uid: [
            {
                u"destinationGuid": destination[u"destinationGuid"],
                u"nodeGuid": node[u"nodeGuid"],
            }
        ]
        for plan_uid in node[u"securityPlanUids"]
    }


def _parse_file_location_response(locations):
    devices = {}
    for location in locations:
        file_name = location[u"fileName"]
        file_path = u"{}{}".format(location[u"filePath"], file_name)
        device_id = location[u"deviceUid"]
        device_entry = devices.get(device_id)
        if device_entry:
            devices[device_id]["paths"].append(file_path)
        else:
            devices[device_id] = {"deviceGuid": device_id, "paths": [file_path]}

    return [devices[key] for key in devices]


def _get_version_lookup_info(events):
    for event in events:
        device_guid = event[u"deviceUid"]
        md5 = event[u"md5Checksum"]
        sha256 = event[u"sha256Checksum"]
        fileName = event[u"fileName"]
        filePath = event[u"filePath"]

        if device_guid and md5 and sha256 and fileName and filePath:
            path = "{}{}".format(filePath, fileName)
            return device_guid, md5, sha256, path


class PlanStorageInfo(object):
    def __init__(self, plan_uid, destination_guid, node_guid):
        self._plan_uid = plan_uid
        self._destination_uid = destination_guid
        self._node_guid = node_guid

    @property
    def plan_uid(self):
        """The UID of the storage plan."""
        return self._plan_uid

    @property
    def destination_guid(self):
        """The GUID of the destination containing the storage archive."""
        return self._destination_uid

    @property
    def node_guid(self):
        """The GUID of the storage node containing the archive."""
        return self._node_guid
