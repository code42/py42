import threading
import logging
import Queue
from threading import Lock


class ScopedLock(object):
    def __init__(self):
        self._locks = {}
        self._counters = {}
        self._master_acq = threading.Lock()
        self._master_rel = threading.Lock()

    def acquire(self, key):
        self._master_acq.acquire()
        if key in self._locks:
            self._counters[key] += 1
        else:
            self._locks[key] = threading.Lock()
            self._counters[key] = 1
        self._master_acq.release()
        self._locks[key].acquire()

    def release(self, key):
        if key in self._locks:
            self._master_rel.acquire()
            if self._counters[key] == 1:
                del self._counters[key]
                lock = self._locks.pop(key)
            else:
                self._counters[key] -= 1
                lock = self._locks[key]

            lock.release()
            self._master_rel.release()


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


class LogThread(threading.Thread):
    """LogThread should always be used in preference to threading.Thread.

    The interface provided by LogThread is identical to that of threading.Thread,
    however, if an exception occurs in the thread the error will be logged
    (using logging.exception) rather than printed to stderr.

    This is important in daemon style applications where stderr is redirected
    to /dev/null.

    """
    def __init__(self, **kwargs):
        super(LogThread, self).__init__(**kwargs)
        self._real_run = self.run
        self.run = self._wrap_run

    def _wrap_run(self):
        try:
            self._real_run()
        except Exception as e:
            logging.exception('Exception during LogThread.run')
