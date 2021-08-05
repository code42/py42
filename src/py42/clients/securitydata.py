import re
from threading import Lock

from py42.exceptions import Py42ChecksumNotFoundError
from py42.exceptions import Py42Error
from py42.sdk.queries.fileevents.file_event_query import FileEventQuery
from py42.sdk.queries.fileevents.filters.file_filter import MD5
from py42.sdk.queries.fileevents.filters.file_filter import SHA256


class SecurityDataClient(object):
    def __init__(
        self,
        file_event_service,
        preservation_data_service,
        saved_search_service,
        storage_service_factory,
    ):
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
            :class: `py42._internal.services.SavedSearchService`
        """
        return self._saved_search_service

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
                field ``nextPgToken``. Defaults to empty string.

        Returns:
            :class:`py42.response.Py42Response`: A response containing page of events.
        """

        query.page_token = _escape_quote_chars_in_token(page_token)
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


def _escape_quote_chars_in_token(token):
    """
    The `nextPgToken` returned in Forensic Search requests with > 10k results is the eventId
    of the last event returned in the response. Some eventIds have double-quote chars in
    them, which need to be escaped when passing the token in the next search request.
    """
    unescaped_quote_pattern = r'[^\\]"'

    return re.sub(
        pattern=unescaped_quote_pattern,
        repl=lambda match: match.group().replace(u'"', r"\""),
        string=token,
    )
