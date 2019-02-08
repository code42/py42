import json
import Queue
from threading import Lock
from .api.handlers.http import Session, BatchAsyncSession
from .api.handlers.http.threadutils import LogThread


def create_session(host_address, auth_handler, proxies, is_async):
    session_type = BatchAsyncSession if is_async else Session
    session = session_type(host_address, auth_handler=auth_handler, proxies=proxies)
    return session


def get_obj_from_response(response, data_key):
    if response.content and 200 <= response.status_code < 300:
        response_json = json.loads(response.content)
        if "data" in response_json:
            data = response_json["data"]
            if data_key == "data":
                return data
            if data_key in data:
                return data[data_key]
    else:
        return []


class QueuedLogger(object):
    def __init__(self, file_name=None):
        self._queue = Queue.Queue()
        self._file_name = file_name
        self.__started = False
        self.__start_lock = Lock()

    def log(self, message):
        if not self.__started:
            self.__start_lock.acquire()
            if not self.__started:
                self.__start()
                self.__started = True
            self.__start_lock.release()
        self._queue.put(message)

    def _process_queue(self):
        while True:
            try:
                message = self._queue.get()
                if self._file_name is not None:
                    print >> self._file_name, message
                else:
                    print message
            finally:
                self._queue.task_done()

    def __start(self):
        t = LogThread(target=self._process_queue)
        t.daemon = True
        t.start()

    def wait(self):
        self._queue.join()
        self.__started = False
