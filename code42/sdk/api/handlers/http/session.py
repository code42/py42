import requests.adapters
import threading
from urlparse import urlparse, urljoin


class Session(requests.Session):

    def __init__(self, host_address, auth_handler=None, proxies=None):
        super(Session, self).__init__()
        self._host_address = host_address
        self._auth_handler = auth_handler
        self._valid_auth = self._auth_handler is None
        self._max_tries = 2
        self._auth_lock = threading.Lock()
        adapter = requests.adapters.HTTPAdapter(pool_connections=500, pool_maxsize=500)
        self.mount("https://", adapter)
        self.mount("http://", adapter)
        parsed_host = urlparse(self._host_address)
        if parsed_host.port is None:
            host = parsed_host.hostname
        else:
            host = "%s:%d" % (parsed_host.hostname, parsed_host.port)

        self.proxies = proxies
        self.headers = {"Accept": "*/*",
                        "Content-Type": "application/json",
                        "Host": host,
                        "Accept-Encoding": "gzip, deflate",
                        "Connection": "keep-alive"}

        self._add_auth_if_missing()

    @property
    def host_address(self):
        return self._host_address

    def request(self, method, url,
                params=None,
                data=None,
                headers=None,
                cookies=None,
                files=None,
                auth=None,
                timeout=None,
                allow_redirects=True,
                proxies=None,
                hooks=None,
                stream=None,
                verify=None,
                cert=None,
                then=None,
                catch=None,
                **kwargs):

        url = urljoin(self._host_address, url)
        times_try = 0
        response = None
        while times_try < self._max_tries:

            try:
                if times_try > 0:
                    self._add_auth_if_missing()

                response = super(Session, self).request(method, url,
                                                        params=params,
                                                        data=data,
                                                        headers=headers,
                                                        cookies=cookies,
                                                        files=files,
                                                        auth=auth,
                                                        timeout=timeout,
                                                        allow_redirects=allow_redirects,
                                                        proxies=proxies,
                                                        hooks=hooks,
                                                        stream=stream,
                                                        verify=verify,
                                                        cert=cert)

            except Exception as e:
                message = method + " request to " + url + " was not received or timed out against the remote server."
                ex = Exception(message + ", caused by: " + e.message)
                if catch is not None:
                    catch(ex)
                    return
                else:
                    raise ex

            times_try += 1
            handler = self._auth_handler
            no_auth = handler is not None and handler.response_indicates_unauthorized(response)
            if no_auth and times_try < self._max_tries:
                self._valid_auth = False
            else:
                status_code = response.status_code
                if (times_try >= self._max_tries and no_auth) or (status_code >= 400 and not status_code == 404):
                    message = method + " request to " + url + " failed with status code " + str(response.status_code)
                    ex = Exception(message)
                    if catch is not None:
                        catch(ex)
                        return
                    else:
                        raise ex
                else:
                    break

        if then is not None and response is not None:
            return then(response, **kwargs)

        return response

    def _add_auth_if_missing(self):
        if self._auth_handler is not None and not self._valid_auth:
            try:
                self._auth_lock.acquire()
                if not self._valid_auth:
                    self._auth_handler.handle_unauthorized(self)
                    self._valid_auth = True
            finally:
                self._auth_lock.release()
