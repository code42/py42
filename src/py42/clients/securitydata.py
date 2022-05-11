from py42.exceptions import Py42ChecksumNotFoundError
from py42.exceptions import Py42Error
from py42.sdk.queries.fileevents.v2.file_event_query import FileEventQuery
from py42.sdk.queries.fileevents.v2.filters.file import MD5
from py42.sdk.queries.fileevents.v2.filters.file import SHA256
from py42.services.util import escape_quote_chars


class SecurityDataClient:
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

    @property
    def savedsearches(self):
        """A collection of methods related to retrieving forensic search data.

        Returns:
            :class: `py42.services.savedsearch.SavedSearchService`
        """
        return self._saved_search_service

    def search_file_events(self, query):
        """Searches for file events, returns up to the first 10,000 events.
        `REST Documentation <https://developer.code42.com/api/#operation/searchEventsUsingPOST>`__

        Args:
            query (str or :class:`py42.sdk.queries.fileevents.v2.file_event_query.FileEventQuery`):
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
            query (str or :class:`py42.sdk.queries.fileevents.v2.file_event_query.FileEventQuery`):
                The file event query to filter search results.
            page_token (str, optional): A token used to indicate the starting point for
                additional page results. For the first page, do not pass ``page_token``. For
                all consecutive pages, pass the token from the previous response from
                field ``nextPgToken``. Defaults to empty string.

        Returns:
            :class:`py42.response.Py42Response`: A response containing a page of events.
        """

        query.page_token = escape_quote_chars(page_token)
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
        events = response["fileEvents"]
        info = _get_version_lookup_info(events)
        if not len(events) or not info:
            raise Py42ChecksumNotFoundError(response, "SHA256", checksum)
        return self._stream_file(checksum, info)

    def stream_file_by_md5(self, checksum):
        """Stream file based on MD5 checksum.

        Args:
            checksum (str): MD5 hash of the file.

        Returns:
            Returns a stream of the requested file.
        """
        response = self._search_by_hash(checksum, MD5)
        events = response["fileEvents"]
        info = _get_version_lookup_info(events)
        if not len(events) or not info:
            raise Py42ChecksumNotFoundError(response, "MD5", checksum)
        return self._stream_file(checksum, info)

    def _search_by_hash(self, checksum, checksum_type):
        query = FileEventQuery.all(checksum_type.eq(checksum))
        query.sort_key = "@timestamp"
        query.sort_direction = "desc"
        response = self.search_file_events(query)
        return response

    def _stream_file(self, checksum, version_info):
        (device_guid, md5_hash, sha256_hash, path) = version_info
        version = self._get_file_version_for_stream(
            device_guid, md5_hash, sha256_hash, path
        )
        if version:
            return self._get_file_stream(version)

        raise Py42Error(f"No file with hash {checksum} available for download.")

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
        versions = (
            response.data.get("securityEventVersionsMatchingChecksum")
            or response.data.get("securityEventVersionsAtPath")
            or response.data.get("preservationVersions")
        )

        if versions:
            if not response.data.get("securityEventVersionsAtPath"):
                exact_match = _get_first_matching_version(versions, md5_hash)
                if exact_match:
                    return exact_match

            most_recent = sorted(
                versions, key=lambda i: i["versionTimestamp"], reverse=True
            )
            return most_recent[0]

    def _get_other_file_location_version(self, md5_hash, sha256_hash):
        response = self._file_event_service.get_file_location_detail_by_sha256(
            sha256_hash
        )
        locations = response["locations"]
        if locations:
            paths = _parse_file_location_response(locations)
            version = self._preservation_data_service.find_file_version(
                md5_hash, sha256_hash, paths
            )
            if version.status_code == 200:
                return version.data

    def _get_file_stream(self, version):
        if version.get("edsUrl"):
            return self._get_exfiltrated_file(version)

        return self._get_stored_file(version)

    def _get_exfiltrated_file(self, version):
        eds = self._storage_service_factory.create_exfiltrated_data_service(
            version["edsUrl"]
        )
        token = eds.get_download_token(
            version["eventId"],
            version["deviceUid"],
            version["filePath"],
            version["versionTimestamp"],
        )
        return eds.get_file(str(token))

    def _get_stored_file(self, version):
        pds = self._storage_service_factory.create_preservation_data_service(
            version["storageNodeURL"]
        )
        token = pds.get_download_token(
            version["archiveGuid"],
            version["fileId"],
            version["versionTimestamp"],
        )
        return pds.get_file(str(token))


def _parse_file_location_response(locations):
    devices = {}
    for location in locations:
        file_name = location["fileName"]
        file_path = f'{location["filePath"]}{file_name}'
        device_id = location["deviceUid"]
        device_entry = devices.get(device_id)
        if device_entry:
            devices[device_id]["paths"].append(file_path)
        else:
            devices[device_id] = {"deviceGuid": device_id, "paths": [file_path]}

    return [devices[key] for key in devices]


def _get_version_lookup_info(events):
    for event in events:
        device_guid = event["user"]["deviceUid"]
        md5 = event["file"]["hash"]["md5"]
        sha256 = event["file"]["hash"]["sha256"]
        fileName = event["file"]["name"]
        filePath = event["file"]["directory"]

        if device_guid and md5 and sha256 and fileName and filePath:
            path = f"{filePath}{fileName}"
            return device_guid, md5, sha256, path


def _get_first_matching_version(versions, md5_hash):
    exact_match = next((x for x in versions if x["fileMD5"] == md5_hash), None)
    if exact_match:
        return exact_match
