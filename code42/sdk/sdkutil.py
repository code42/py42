import Queue
from threading import Lock
from .api.handlers.http.threadutils import LogThread


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
