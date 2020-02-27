import json as json_lib
from threading import Lock

import requests.adapters

import py42.debug as debug
import py42.debug_level as debug_level
import py42.settings as settings
import py42.util as util
from py42._internal.compat import str, urljoin, urlparse


class Py42Session(object):
    def __init__(self, session, host_address, auth_handler=None):
        self._initialized = False
        self._needs_auth_renewal_check = False
        self._auth_lock = Lock()
        self._session = session
        adapter = requests.adapters.HTTPAdapter(pool_connections=500, pool_maxsize=500)
        if not host_address.startswith(u"http://") and not host_address.startswith(u"https://"):
            host_address = u"https://{0}".format(host_address)

        self._host_address = host_address
        self._auth_handler = auth_handler

        self._session.proxies = settings.proxies
        self._session.verify = settings.verify_ssl_certs
        self._session.mount(u"https://", adapter)
        self._session.mount(u"http://", adapter)

        self._host_address = host_address
        parsed_host = urlparse(self._host_address)
        host = parsed_host.netloc

        self._session.headers = {
            u"Accept": u"application/json",
            u"Content-Type": u"application/json",
            u"Host": host,
            u"User-Agent": settings.get_user_agent_string(),
            u"Accept-Encoding": u"gzip, deflate",
            u"Connection": u"keep-alive",
        }

    @property
    def host_address(self):
        return self._host_address

    @property
    def headers(self):
        return self._session.headers

    @property
    def cookies(self):
        return self._session.cookies

    @property
    def proxies(self):
        return self._session.proxies

    def get(self, url, **kwargs):
        return self.request(u"GET", url, **kwargs)

    def options(self, url, **kwargs):
        return self.request(u"OPTIONS", url, **kwargs)

    def head(self, url, **kwargs):
        return self.request(u"HEAD", url, **kwargs)

    def post(self, url, data=None, json=None, **kwargs):
        return self.request(u"POST", url, data=data, json=json, **kwargs)

    def put(self, url, data=None, **kwargs):
        return self.request(u"PUT", url, data=data, **kwargs)

    def patch(self, url, data=None, **kwargs):
        return self.request(u"PATCH", url, data=data, **kwargs)

    def delete(self, url, **kwargs):
        return self.request(u"DELETE", url, **kwargs)

    def request(self, method, url, **kwargs):
        try:
            url = urljoin(self._host_address, url)
            json = kwargs.get("json")

            if json is not None:
                kwargs["data"] = json_lib.dumps(util.filter_out_none(json))

            self._renew_authentication(use_cache=True)

            tries = 0
            max_tries = 2
            while tries < max_tries:
                response, unauthorized = self._try_make_request(method, url, **kwargs)
                tries += 1

                if unauthorized and tries < max_tries:
                    self._renew_authentication()
                    continue

                if response.status_code >= 400:
                    response.raise_for_status()

                if not kwargs.get("stream"):
                    response.encoding = "utf-8"  # setting this manually speeds up read times

                return response

        except (requests.HTTPError, requests.RequestException, Exception) as ex:
            raise ex

    def _try_make_request(
        self,
        method,
        url,
        params=None,
        data=None,
        headers=None,
        cookies=None,
        files=None,
        auth=None,
        timeout=60,
        allow_redirects=True,
        proxies=None,
        hooks=None,
        stream=None,
        verify=None,
        cert=None,
        json=None,
    ):
        if debug.will_print_for(debug_level.INFO):
            self._print_request(method, url, params=params, data=data)

        response = self._session.request(
            method,
            url,
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
            cert=cert,
        )

        unauthorized = self._auth_handler and self._auth_handler.response_indicates_unauthorized(
            response
        )

        return response, unauthorized

    def _renew_authentication(self, use_cache=False):
        if self._auth_handler:
            # if multiple threads try to authenticate at once, only the first one actually does.
            # the rest will just wait for that authentication to complete.
            self._needs_auth_renewal_check = True
            with self._auth_lock:
                # only get new credentials if this is the first time or we want fresh ones
                should_renew = (
                    not self._initialized or not use_cache
                ) and self._needs_auth_renewal_check
                if should_renew:
                    self._auth_handler.renew_authentication(self, use_cache=use_cache)
                    self._needs_auth_renewal_check = False

        # if there's no auth handler or we handled auth without errors, initialization is done.
        self._initialized = True

    def _print_request(self, method, url, params=None, data=None):
        print(u"{0}{1}".format(str(method).ljust(8), url))
        if debug.will_print_for(debug_level.TRACE):
            if self.headers:
                util.print_dict(self.headers, u"  headers")
        if debug.will_print_for(debug_level.DEBUG):
            if params:
                util.print_dict(params, u"  params")
            if data:
                util.print_dict(data, u"  data")
