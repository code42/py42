import Queue
import logging
from threading import Lock, Thread


class QueuedLogger(object):
    def __init__(self, logger=None):
        self._queue = Queue.Queue()
        self._logger = logger
        self.__started = False
        self.__start_lock = Lock()

    def debug(self, message):
        self.log(logging.DEBUG, message)

    def info(self, message):
        self.log(logging.INFO, message)

    def warn(self, message):
        self.log(logging.WARN, message)

    def error(self, message):
        self.log(logging.ERROR, message)

    def log(self, level, message):
        if not self.__started:
            self.__start_lock.acquire()
            if not self.__started:
                self.__start()
                self.__started = True
            self.__start_lock.release()
        log_item = {"level": level, "message": message}
        self._queue.put(log_item)

    def _process_queue(self):
        while True:
            try:
                log_item = self._queue.get()
                if self._logger is not None:
                    self._logger.log(log_item["level"], log_item["message"])
                else:
                    print(log_item["message"])
            finally:
                self._queue.task_done()

    def __start(self):
        t = Thread(target=self._process_queue)
        t.daemon = True
        t.start()

    def wait(self):
        self._queue.join()
        self.__started = False
