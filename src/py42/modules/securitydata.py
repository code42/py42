import json
from threading import Lock

from requests.exceptions import HTTPError

from py42.exceptions import Py42ArchiveFileNotFoundError
from py42.exceptions import Py42Error
from py42.exceptions import Py42HTTPError
from py42.exceptions import Py42SecurityPlanConnectionError
from py42.exceptions import raise_py42_error
from py42.sdk.queries.fileevents.file_event_query import FileEventQuery
from py42.sdk.queries.fileevents.filters.file_filter import MD5
from py42.sdk.queries.fileevents.filters.file_filter import SHA256
from py42.settings import debug


class SecurityModule(object):
    def __init__(
        self, security_client, storage_client_factory, microservices_client_factory
    ):
        self._security_client = security_client
        self._storage_client_factory = storage_client_factory
        self._microservices_client_factory = microservices_client_factory
        self._client_cache = {}
        self._client_cache_lock = Lock()

    @property
    def savedsearches(self):
        """A collection of methods related to retrieving forensic search data.

        Returns:
            :class: `py42._internal.clients.securitydata.SavedSearchClient`
        """
        return self._microservices_client_factory.get_saved_search_client()

    def get_security_plan_storage_info_list(self, user_uid):
        """Gets IDs (plan UID, node GUID, and destination GUID) for the storage nodes containing
        the file activity event data for the user with the given UID.
        `REST Documentation <https://console.us.code42.com/swagger/#/Feature/getStorageNode>`__

        Args:
            user_uid (str): The UID of the user to get plan storage information for.

        Returns:
            list[:class:`py42.modules.securitydata.PlanStorageInfo`]
        """
        locations = None
        try:
            response = self._security_client.get_security_event_locations(user_uid)
            locations = response[u"securityPlanLocationsByDestination"]
        except HTTPError as err:
            if err.response.status_code == 404:
                pass
            else:
                raise_py42_error(err)

        if locations:
            plan_destination_map = _get_plan_destination_map(locations)
            selected_plan_infos = self._get_plan_storage_infos(plan_destination_map)
            if not selected_plan_infos:
                raise Py42SecurityPlanConnectionError(
                    u"Could not establish a connection to retrieve "
                    u"security events for user {}".format(user_uid)
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
            plan_storage_info (:class:`py42.sdk.modules.securitydata.PlanStorageInfo`):
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
            min_timestamp (float, optional): A POSIX timestamp representing the beginning of the
                date range of events to get. Defaults to None.
            max_timestamp (float, optional): A POSIX timestamp representing the end of the date
                range of events to get. Defaults to None.

        Returns:
            generator: An object that iterates over :class:`py42.response.Py42Response` objects
            that each contain a page of events.
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
            min_timestamp (float, optional): A POSIX timestamp representing the beginning of the
                date range of events to get. Defaults to None.
            max_timestamp (float, optional): A POSIX timestamp representing the end of the date
                range of events to get. Defaults to None.

        Returns:
            generator: An object that iterates over :class:`py42.response.Py42Response` objects
            that each contain a page of events.
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
        """Searches for file events.
        `REST Documentation <https://support.code42.com/Administrator/Cloud/Monitoring_and_managing/Forensic_File_Search_API>`__

        Args:
            query (:class:`py42.sdk.queries.fileevents.file_event_query.FileEventQuery`): Also
                accepts a raw JSON str.

        Returns:
            :class:`py42.response.Py42Response`: A response containing the first 10,000
            events.
        """
        file_event_client = self._microservices_client_factory.get_file_event_client()
        return file_event_client.search(query)

    def _search_by_hash(self, hash, type):
        query = FileEventQuery.all(type.eq(hash))
        response = self.search_file_events(query)
        return response[u"fileEvents"]

    def _find_file_versions(self, md5_hash, sha256_hash):
        file_event_client = self._microservices_client_factory.get_file_event_client()
        pds_client = (
            self._microservices_client_factory.get_preservation_data_service_client()
        )
        response = file_event_client.get_file_location_detail_by_sha256(sha256_hash)

        if u"locations" not in response and not len(response[u"locations"]):
            raise Py42Error(
                u"PDS service can't find requested file "
                u"with md5 hash {} and sha256 hash {}.".format(md5_hash, sha256_hash)
            )

        for device_id, paths in _parse_file_location_response(response):
            try:
                yield pds_client.find_file_versions(
                    md5_hash, sha256_hash, device_id, paths
                )
            except Py42HTTPError as err:
                # API searches multiple paths to find the file to be streamed, as returned by
                # 'get_file_location_detail_by_sha256', hence we keep looking until we find a stream
                # to return
                debug.logger.warning(
                    u"Failed to find any file version for md5 hash {} / sha256 hash {}. "
                    u"Error: ".format(md5_hash, sha256_hash),
                    err,
                )

    def _stream_file(self, file_generator, checksum):
        for response in file_generator:
            if response.status_code == 204:
                continue
            try:
                storage_node_client = self._microservices_client_factory.create_storage_preservation_client(
                    response[u"storageNodeURL"]
                )
                token = storage_node_client.get_download_token(
                    response[u"archiveGuid"],
                    response[u"fileId"],
                    response[u"versionTimestamp"],
                )
                return storage_node_client.get_file(str(token))
            except Py42HTTPError:
                # API searches multiple paths to find the file to be streamed, as returned by
                # 'get_file_location_detail_by_sha256', hence we keep looking until we find a stream
                # to return
                debug.logger.warning(
                    u"Failed to stream file with hash {}, info: {}.".format(
                        checksum, response.text
                    )
                )
        raise Py42Error(
            u"No file with hash {} available for download on any storage node.".format(
                checksum
            )
        )

    def stream_file_by_sha256(self, checksum):
        """Stream file based on SHA256 checksum.

        Args:
            checksum (str): SHA256 hash of the file.

        Returns:
            Returns a stream of the requested file.
        """
        events = self._search_by_hash(checksum, SHA256)
        if not len(events):
            message = u"File not found in archive with sha256 checksum {}".format(
                checksum
            )
            raise Py42Error(message)
        md5_hash = events[0][u"md5Checksum"]

        return self._stream_file(self._find_file_versions(md5_hash, checksum), checksum)

    def stream_file_by_md5(self, checksum):
        """Stream file based on MD5 checksum.

        Args:
            checksum (str): MD5 hash of the file.

        Returns:
            Returns a stream of the requested file.
        """
        events = self._search_by_hash(checksum, MD5)
        if not len(events):
            raise Py42ArchiveFileNotFoundError(checksum, "")
        sha256_hash = events[0][u"sha256Checksum"]
        return self._stream_file(
            self._find_file_versions(checksum, sha256_hash), checksum
        )

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
        except HTTPError:
            #  This function is called in a loop until we get a result that is not None.
            #  If all return None, then the calling function raises Py42SecurityPlanConnectionError.
            pass

    def _try_get_security_detection_event_client(self, plan_storage_info):
        # check if we have already created and stored this client
        client = self._client_cache.get(plan_storage_info.node_guid)

        # otherwise, create it
        if client is None:
            client = self._storage_client_factory.from_plan_info(
                plan_storage_info.plan_uid, plan_storage_info.destination_guid
            ).securitydata

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
                    # we use json.loads here because the cursor prop doesn't appear
                    # on responses that have no results
                    cursor = json.loads(response.text).get(u"cursor")
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


def _parse_file_location_response(response):

    for location in response[u"locations"]:
        paths = []
        file_name = location[u"fileName"]
        device_id = location[u"deviceUid"]
        paths.append(u"{}{}".format(location[u"filePath"], file_name))
        yield device_id, paths


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
