import time

from py42.settings import debug
from py42.util import format_dict


def create_restore_job_manager(
    storage_archive_service, device_guid, archive_session_id
):
    return RestoreJobManager(storage_archive_service, device_guid, archive_session_id,)


def create_file_size_poller(storage_archive_service, device_guid):
    return FileSizePoller(storage_archive_service, device_guid)


class _RestorePoller(object):
    JOB_POLLING_INTERVAL_SECONDS = 1

    def __init__(self, storage_archive_service, device_guid, job_polling_interval=None):
        self._storage_archive_service = storage_archive_service
        self._device_guid = device_guid
        self._job_polling_interval = (
            job_polling_interval or self.JOB_POLLING_INTERVAL_SECONDS
        )


class FileSizePoller(_RestorePoller):
    def __init__(self, storage_archive_service, device_guid, job_polling_interval=None):
        super(FileSizePoller, self).__init__(
            storage_archive_service, device_guid, job_polling_interval
        )

    def get_file_sizes(self, file_ids, timeout):
        if not timeout:
            # Skips file size calculation
            return None

        job_ids = self._start_poll(file_ids)
        return self._wait_for_jobs(job_ids, timeout)

    def _start_poll(self, file_ids):
        job_ids = []
        for file_id in file_ids:
            response = self._storage_archive_service.create_file_size_job(
                self._device_guid, file_id
            )
            job_id = response[u"jobId"]
            job_ids.append(job_id)
        return job_ids

    def _wait_for_jobs(self, job_ids, timeout):
        t0 = time.time()
        sizes = []

        # Waits until the job_ids stack is empty
        while job_ids:
            for job_id in job_ids:
                response = self._get_job_status(job_id)
                size_dict = _create_size_dict(job_id, response)
                _print_file_size(size_dict)
                if response[u"status"].lower() == u"done":
                    job_ids.remove(job_id)
                    sizes.append(size_dict)

            # File size calculation is taking too long.
            if time.time() - t0 > timeout:
                return None

            if job_ids:
                time.sleep(self._job_polling_interval)
        return sizes

    def _get_job_status(self, job_id):
        return self._storage_archive_service.get_file_size_job(
            job_id, self._device_guid
        )


class RestoreJobManager(_RestorePoller):
    def __init__(
        self,
        storage_archive_service,
        device_guid,
        archive_session_id,
        job_polling_interval=None,
    ):
        super(RestoreJobManager, self).__init__(
            storage_archive_service=storage_archive_service,
            device_guid=device_guid,
            job_polling_interval=job_polling_interval,
        )
        self._archive_session_id = archive_session_id

    def get_stream(self, file_selections):
        response = self._start_web_restore(file_selections)
        job_id = self._wait_for_job(response)
        return self._get_stream(job_id)

    def send_stream(
        self, restore_path, node_guid, accepting_guid, file_selections, show_deleted
    ):
        num_files = sum([fs.num_files for fs in file_selections])
        size = sum([fs.num_bytes for fs in file_selections])
        return self._storage_archive_service.start_push_restore(
            self._device_guid,
            accepting_guid,
            self._archive_session_id,
            node_guid,
            [{u"backupSetId": -1, u"files": [f.file for f in file_selections]}],
            restore_path,
            num_files,
            size,
            show_deleted=show_deleted,
            file_permissions=u"CURRENT",
            permit_restore_to_different_os_version=True,
            restore_full_path=True,
        )

    def _wait_for_job(self, response):
        job_id = response[u"jobId"]
        while not self._is_job_complete(job_id):
            time.sleep(self._job_polling_interval)
        return job_id

    def _is_job_complete(self, job_id):
        response = self._storage_archive_service.get_restore_status(job_id)
        is_done = response[u"done"]
        percentage_dict = {
            u"jobId": job_id,
            u"status": response.data.get(u"status"),
            u"percentComplete": response[u"percentComplete"] if not is_done else 100,
        }
        debug.logger.debug(format_dict(percentage_dict))
        return is_done

    def _start_web_restore(self, file_selections):
        num_files = sum([fs.num_files for fs in file_selections])
        num_dirs = sum([fs.num_dirs for fs in file_selections])
        num_bytes = sum([fs.num_bytes for fs in file_selections])
        return self._storage_archive_service.start_restore(
            self._device_guid,
            self._archive_session_id,
            [{u"backupSetId": -1, u"files": [f.file for f in file_selections]}],
            num_files,
            num_dirs,
            num_bytes,
            show_deleted=True,
        )

    def _get_stream(self, job_id):
        response = self._storage_archive_service.stream_restore_result(job_id)
        return response


def _create_size_dict(job_id, size_response):
    size_dict = size_response.data
    size_dict[u"jobId"] = job_id
    return size_dict


def _print_file_size(size_dict):
    debug.logger.debug(format_dict(size_dict))
