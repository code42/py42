import time
import traceback
from threading import Lock, Thread

from py42._internal.compat import queue
from .session import Py42Session


class Py42AsyncSession(Py42Session):
    def __init__(
        self,
        session,
        host_address,
        auth_handler=None,
        concurrent_threads=4,
        max_requests_per_second=36,
    ):

        super(Py42AsyncSession, self).__init__(session, host_address, auth_handler=auth_handler)
        # Lifo makes it so that callbacks happen sooner after being called instead of being placed all the way
        # to the back of the queue and having to wait again.
        self._request_queue = queue.LifoQueue()
        self._concurrent_threads = concurrent_threads
        self._max_requests_per_second = max_requests_per_second
        self.__started = False
        self.__start_lock = Lock()

    def request(self, method, url, force_sync=False, *args, **kwargs):
        if not self.__started:
            self.__start_lock.acquire()
            if not self.__started:
                self.__start()
                self.__started = True
            self.__start_lock.release()
        if not force_sync:
            self._request_queue.put(
                {u"method": method, u"path": url, u"args": args, u"kwargs": kwargs}
            )
        else:
            return super(Py42AsyncSession, self).request(method, url, *args, **kwargs)

    def _process_queue(self):
        new_request = self._request_queue.get
        send = super(Py42AsyncSession, self).request
        # To avoid having calls dropped because of rate limits, we can tweak the number of concurrent threads and
        # the max requests allowed per second and intentionally throttle dispatching requests if
        # they are completing too quickly.
        min_request_time = float(self._concurrent_threads) / float(self._max_requests_per_second)
        while True:
            try:
                request = new_request()
                start = time.time()
                send(request[u"method"], request[u"path"], *request[u"args"], **request[u"kwargs"])
                end = time.time()
                elapsed = end - start
                if elapsed < min_request_time:
                    diff = min_request_time - elapsed
                    time.sleep(diff)
            except Exception as ex:
                # should never happen (TM) since exceptions that happen in the superclass should call
                # self._handle_error without reaching here
                trace = traceback.format_exc()
                self._handle_error(ex, trace, None)
            finally:
                self._request_queue.task_done()

    def _handle_error(self, exception, exception_trace, request_handler):
        try:
            if request_handler is not None:
                request_handler(exception)
            elif self._process_exception_message is not None:
                exception_message = self._build_exception_message_with_exception_and_trace(
                    exception, exception_trace
                )
                self._process_exception_message(exception_message)  # pylint: disable=not-callable
        except:
            # handle errors that occur in the user-supplied exception handlers.
            trace = traceback.format_exc()
            print(u"UNHANDLED ERROR: {0}".format(trace))

    def __start(self):
        for _ in range(self._concurrent_threads):
            thread = Thread(target=self._process_queue)
            thread.daemon = True
            thread.start()

    def wait(self):
        self._request_queue.join()
        self.__started = False
