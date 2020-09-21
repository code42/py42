import json
import time

from requests import Response
from tests.clients._archiveaccess.conftest import DESKTOP_ID
from tests.clients._archiveaccess.conftest import DEVICE_GUID
from tests.clients._archiveaccess.conftest import DOWNLOADS_ID
from tests.clients._archiveaccess.conftest import WEB_RESTORE_SESSION_ID

from py42.clients._archiveaccess.restoremanager import FileSizePoller
from py42.clients._archiveaccess.restoremanager import RestoreJobManager
from py42.response import Py42Response


class GetWebRestoreJobResponses(object):
    MISSING_STATUS = """{
                "zipResult": false,
                "name": "WebRestore_13",
                "sourceId": "896477098509532085",
                "userId": 202011,
                "bytesZipped": 0,
                "jobId": "899350590659304988",
                "canceled": false,
                "done": true,
                "expirationDate": 1556888724979,
                "creationDate": 1556802324979,
                "percentComplete": 0
            }
        """
    NOT_DONE = """{
                "status": "preparing",
                "zipResult": false,
                "name": "WebRestore_13",
                "sourceId": "896477098509532085",
                "userId": 202011,
                "bytesZipped": 0,
                "jobId": "899350590659304988",
                "canceled": false,
                "done": false,
                "expirationDate": 1556888724979,
                "creationDate": 1556802324979,
                "percentComplete": 0
            }
        """
    DONE = """{
                "status": "done",
                "zipResult": false,
                "name": "WebRestore_13",
                "sourceId": "896477098509532085",
                "userId": 202011,
                "bytesZipped": 0,
                "jobId": "899350590659304988",
                "canceled": false,
                "done": true,
                "expirationDate": 1556888724979,
                "creationDate": 1556802324979
            }
        """


def mock_start_restore_response(mocker, storage_archive_service, response):
    def mock_start_restore(
        device_guid,
        web_restore_session_id,
        restore_groups,
        num_files,
        num_dirs,
        num_bytes,
        **kwargs
    ):
        start_restore_response = mocker.MagicMock(spec=Response)
        start_restore_response.text = response
        start_restore_response.status_code = 200
        return Py42Response(start_restore_response)

    storage_archive_service.start_restore.side_effect = mock_start_restore


def mock_get_restore_status_responses(mocker, storage_archive_service, json_responses):
    responses = []
    for json_response in json_responses:
        get_restore_status_response = mocker.MagicMock(spec=Response)
        get_restore_status_response.text = json_response
        get_restore_status_response.status_code = 200
        responses.append(Py42Response(get_restore_status_response))

    storage_archive_service.get_restore_status.side_effect = responses


def stream_restore_result_response_mock(mocker, storage_archive_service, chunks):
    stream_restore_result_response = mocker.MagicMock(spec=Py42Response)

    def mock_stream_restore_result(job_id, **kwargs):
        stream_restore_result_response.iter_content.return_value = chunks
        return stream_restore_result_response

    storage_archive_service.stream_restore_result.side_effect = (
        mock_stream_restore_result
    )

    return stream_restore_result_response


def get_response_job_id(response_str):
    return json.loads(response_str)["jobId"]


class TestFileSizePoller(object):
    DESKTOP_SIZE_JOB = "DESKTOP_SIZE_JOB"
    DOWNLOADS_SIZE_JOB = "DOWNLOADS_SIZE_JOB"
    DESKTOP_SIZES = {"numDirs": 1, "numFiles": 2, "size": 3}
    DOWNLOADS_SIZES = {"numDirs": 4, "numFiles": 5, "size": 6}

    def get_create_job_side_effect(self, mocker):
        def create_job(guid, file_id, *args, **kwargs):
            resp = mocker.MagicMock(spec=Response)
            if file_id == DESKTOP_ID:
                resp.text = json.dumps({"jobId": self.DESKTOP_SIZE_JOB})
            elif file_id == DOWNLOADS_ID:
                resp.text = json.dumps({"jobId": self.DOWNLOADS_SIZE_JOB})

            return Py42Response(resp)

        return create_job

    def get_file_sizes_polling_status_side_effect(
        self, mocker,
    ):
        def get_status(job_id, device_guid):
            resp = mocker.MagicMock(spec=Response)
            if job_id == self.DESKTOP_SIZE_JOB:
                self.DESKTOP_SIZES["status"] = "DONE"
                resp.text = json.dumps(self.DESKTOP_SIZES)
            elif job_id == self.DOWNLOADS_SIZE_JOB:
                self.DOWNLOADS_SIZES["status"] = "DONE"
                resp.text = json.dumps(self.DOWNLOADS_SIZES)
            return Py42Response(resp)

        return get_status

    def test_get_file_sizes_returns_sizes_for_each_id(
        self, mocker, storage_archive_service
    ):
        storage_archive_service.create_file_size_job.side_effect = self.get_create_job_side_effect(
            mocker
        )
        storage_archive_service.get_file_size_job.side_effect = self.get_file_sizes_polling_status_side_effect(
            mocker
        )
        poller = FileSizePoller(storage_archive_service, DEVICE_GUID)
        actual = poller.get_file_sizes([DESKTOP_ID, DOWNLOADS_ID], timeout=500)
        assert set(actual[0].values()) == {1, 2, 3, "DONE", "DESKTOP_SIZE_JOB"}
        assert set(actual[0].keys()) == {
            "numDirs",
            "numFiles",
            "size",
            "status",
            "jobId",
        }
        assert set(actual[1].values()) == {4, 5, 6, "DONE", "DOWNLOADS_SIZE_JOB"}
        assert set(actual[1].keys()) == {
            "numDirs",
            "numFiles",
            "size",
            "status",
            "jobId",
        }

    def test_get_file_sizes_waits_for_size_calculation(
        self, mocker, storage_archive_service
    ):
        storage_archive_service.create_file_size_job.side_effect = self.get_create_job_side_effect(
            mocker
        )

        desktop_statuses = ["DONE", "WORKING", "WORKING"]

        def get_file_sizes(job_id, device_id):
            resp = mocker.MagicMock(spec=Response)
            if job_id == self.DESKTOP_SIZE_JOB:
                status = desktop_statuses.pop()
                self.DESKTOP_SIZES["status"] = status
                resp.text = json.dumps(self.DESKTOP_SIZES)

            elif job_id == self.DOWNLOADS_SIZE_JOB:
                self.DESKTOP_SIZES["status"] = "DONE"
                resp.text = json.dumps(self.DESKTOP_SIZES)
            return Py42Response(resp)

        storage_archive_service.get_file_size_job.side_effect = get_file_sizes
        poller = FileSizePoller(storage_archive_service, DEVICE_GUID)
        poller.get_file_sizes([DESKTOP_ID, DOWNLOADS_ID], timeout=500)
        # Called 3 times for the DESKTOP and once for DOWNLOADS
        assert storage_archive_service.get_file_size_job.call_count == 4

    def test_get_file_sizes_when_taking_too_long_returns_none(
        self, mocker, storage_archive_service
    ):
        def take_too_long(*args, **kwargs):
            time.sleep(0.1)
            return self.get_file_sizes_polling_status_side_effect(mocker)(
                *args, **kwargs
            )

        storage_archive_service.create_file_size_job.side_effect = self.get_create_job_side_effect(
            mocker
        )
        storage_archive_service.get_file_size_job.side_effect = take_too_long
        poller = FileSizePoller(storage_archive_service, DEVICE_GUID)
        actual = poller.get_file_sizes([DESKTOP_ID, DOWNLOADS_ID], timeout=0.01)
        assert actual is None


class TestRestoreJobManager(object):
    def test_restore_job_manager_constructs_successfully(self, storage_archive_service):
        assert RestoreJobManager(
            storage_archive_service, DEVICE_GUID, WEB_RESTORE_SESSION_ID
        )

    def test_get_stream_calls_start_web_restore_with_correct_args(
        self, mocker, storage_archive_service, single_file_selection
    ):
        mock_start_restore_response(
            mocker, storage_archive_service, GetWebRestoreJobResponses.NOT_DONE
        )
        mock_get_restore_status_responses(
            mocker, storage_archive_service, [GetWebRestoreJobResponses.DONE]
        )
        restore_job_manager = RestoreJobManager(
            storage_archive_service, DEVICE_GUID, WEB_RESTORE_SESSION_ID
        )
        restore_job_manager.get_stream(single_file_selection)
        expected_restore_groups = [
            {u"backupSetId": -1, u"files": [single_file_selection[0].file]}
        ]
        storage_archive_service.start_restore.assert_called_once_with(
            DEVICE_GUID,
            WEB_RESTORE_SESSION_ID,
            expected_restore_groups,
            1,
            1,
            1,
            show_deleted=True,
        )

    def test_get_stream_when_multiple_files_selected_calls_start_web_restore_with_correct_args(
        self, mocker, storage_archive_service, double_file_selection
    ):
        mock_start_restore_response(
            mocker, storage_archive_service, GetWebRestoreJobResponses.NOT_DONE
        )
        mock_get_restore_status_responses(
            mocker, storage_archive_service, [GetWebRestoreJobResponses.DONE]
        )

        restore_job_manager = RestoreJobManager(
            storage_archive_service, DEVICE_GUID, WEB_RESTORE_SESSION_ID
        )
        restore_job_manager.get_stream(double_file_selection)
        expected_restore_groups = [
            {
                u"backupSetId": -1,
                u"files": [
                    double_file_selection[0].file,
                    double_file_selection[1].file,
                ],
            }
        ]
        storage_archive_service.start_restore.assert_called_once_with(
            DEVICE_GUID,
            WEB_RESTORE_SESSION_ID,
            expected_restore_groups,
            1 + 4,
            2 + 5,
            3 + 6,
            show_deleted=True,
        )

    def test_get_stream_polls_job_status_until_job_is_complete(
        self, mocker, storage_archive_service, single_file_selection
    ):
        mock_start_restore_response(
            mocker, storage_archive_service, GetWebRestoreJobResponses.NOT_DONE
        )
        mock_get_restore_status_responses(
            mocker,
            storage_archive_service,
            [
                GetWebRestoreJobResponses.NOT_DONE,
                GetWebRestoreJobResponses.NOT_DONE,
                GetWebRestoreJobResponses.DONE,
            ],
        )

        restore_job_manager = RestoreJobManager(
            storage_archive_service,
            DEVICE_GUID,
            WEB_RESTORE_SESSION_ID,
            job_polling_interval=0.000001,
        )
        restore_job_manager.get_stream(single_file_selection)
        job_id = get_response_job_id(GetWebRestoreJobResponses.DONE)
        expected_call = mocker.call(job_id)
        storage_archive_service.get_restore_status.assert_has_calls(
            [expected_call, expected_call, expected_call]
        )
        assert storage_archive_service.get_restore_status.call_count == 3

    def test_get_stream_when_response_missing_status_polls_job_status_until_job_is_complete(
        self, mocker, storage_archive_service, single_file_selection
    ):
        mock_start_restore_response(
            mocker, storage_archive_service, GetWebRestoreJobResponses.NOT_DONE
        )
        mock_get_restore_status_responses(
            mocker,
            storage_archive_service,
            [
                GetWebRestoreJobResponses.NOT_DONE,
                GetWebRestoreJobResponses.NOT_DONE,
                GetWebRestoreJobResponses.MISSING_STATUS,
            ],
        )

        restore_job_manager = RestoreJobManager(
            storage_archive_service,
            DEVICE_GUID,
            WEB_RESTORE_SESSION_ID,
            job_polling_interval=0.000001,
        )
        restore_job_manager.get_stream(single_file_selection)
        job_id = get_response_job_id(GetWebRestoreJobResponses.MISSING_STATUS)
        expected_call = mocker.call(job_id)
        storage_archive_service.get_restore_status.assert_has_calls(
            [expected_call, expected_call, expected_call]
        )
        assert storage_archive_service.get_restore_status.call_count == 3

    def test_get_stream_when_successful_returns_response(
        self,
        mocker,
        storage_archive_service,
        single_file_selection,
        file_content_chunks,
    ):
        mock_start_restore_response(
            mocker, storage_archive_service, GetWebRestoreJobResponses.NOT_DONE
        )
        mock_get_restore_status_responses(
            mocker, storage_archive_service, [GetWebRestoreJobResponses.DONE]
        )
        stream_restore_result_response_mock(
            mocker, storage_archive_service, file_content_chunks
        )
        restore_job_manager = RestoreJobManager(
            storage_archive_service, DEVICE_GUID, WEB_RESTORE_SESSION_ID
        )

        assert restore_job_manager.get_stream(single_file_selection)
