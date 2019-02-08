import logging
from threading import Lock, Thread


class ScopedLock(object):
    def __init__(self):
        self._locks = {}
        self._counters = {}
        self._master_acq = Lock()
        self._master_rel = Lock()

    def acquire(self, key):
        self._master_acq.acquire()
        if key in self._locks:
            self._counters[key] += 1
        else:
            self._locks[key] = Lock()
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


class LogThread(Thread):
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
