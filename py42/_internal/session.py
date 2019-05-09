import traceback
from urlparse import urljoin, urlparse
import json as json_lib
import requests.adapters

import py42.debug as debug
import py42.debug_level as debug_level
import py42.settings as settings
import py42.util as util


class Py42Session(object):

    def __init__(self, session, host_address, auth_handler=None):
        self._session = session
        adapter = requests.adapters.HTTPAdapter(pool_connections=500, pool_maxsize=500)
        if not host_address.startswith("http://") and not host_address.startswith("https://"):
            host_address = "https://{0}".format(host_address)

        self._host_address = host_address
        self._process_exception_message = settings.global_exception_message_receiver
        self._auth_handler = auth_handler

        self._session.proxies = settings.proxies
        self._session.verify = settings.verify_ssl_certs
        self._session.mount("https://", adapter)
        self._session.mount("http://", adapter)

        self._host_address = host_address
        parsed_host = urlparse(self._host_address)
        host = parsed_host.netloc

        self._session.headers = {"Accept": "application/json",
                                 "Content-Type": "application/json",
                                 "Host": host,
                                 "Accept-Encoding": "gzip, deflate",
                                 "Connection": "keep-alive"}

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
        return self.request("GET", url, **kwargs)

    def options(self, url, **kwargs):
        return self.request("OPTIONS", url, **kwargs)

    def head(self, url, **kwargs):
        return self.request("HEAD", url, **kwargs)

    def post(self, url, data=None, json=None, **kwargs):
        return self.request("POST", url, data=data, json=json, **kwargs)

    def put(self, url, data=None, **kwargs):
        return self.request("PUT", url, data=data, **kwargs)

    def patch(self, url, data=None, **kwargs):
        return self.request("PATCH", url, data=data, **kwargs)

    def delete(self, url, **kwargs):
        return self.request("DELETE", url, **kwargs)

    def request(self, method, url, params=None, data=None, headers=None, cookies=None, files=None, auth=None,
                timeout=None, allow_redirects=True, proxies=None, hooks=None, stream=None, verify=None, cert=None,
                json=None, force_sync=None, then=None, catch=None):
        max_tries = 2
        tries = 0
        try:
            url = urljoin(self._host_address, url)
            auth_needed = False

            if json is not None:
                data = json_lib.dumps(util.filter_out_none(json))

            while tries < max_tries:
                if self._auth_handler is not None:
                    auth_needed = self._auth_handler.try_authorize(self)

                if debug.will_print_for(debug_level.INFO):
                    self._print_request(method, url, params=params, data=data)

                response = self._session.request(method, url,
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

                tries += 1

                invalid_credentials = auth_needed and self._auth_handler.try_authorize(self, response=response)
                if invalid_credentials and tries < max_tries:
                    # retry one more time. if the credentials are valid but simply expired,
                    # we won't hit this condition next time.
                    continue
                elif response.status_code >= 400:
                    response.raise_for_status()

                if then is not None and response is not None:
                    return then(response)

                return response

        except requests.HTTPError as e:
            trace = traceback.format_exc()
            self._handle_error(e, trace, catch)
        except requests.RequestException as e:
            trace = traceback.format_exc()
            self._handle_error(e, trace, catch)
        except Exception as e:
            trace = traceback.format_exc()
            self._handle_error(e, trace, catch)

    def _handle_error(self, exception, exception_trace, request_handler):
        if request_handler is not None:
            request_handler(exception)
        else:
            # log unhandled exceptions
            if self._process_exception_message is not None:
                self._process_exception_message(exception_trace)
            # always raise unhandled exceptions when using a synchronous client
            raise exception

    def _print_request(self, method, url, params=None, data=None):
        print("{0}{1}".format(str(method).ljust(8), url))
        if debug.will_print_for(debug_level.TRACE):
            if self.headers:
                util.print_dict(self.headers, "  headers")
        if debug.will_print_for(debug_level.DEBUG):
            if params:
                util.print_dict(params, "  params")
            if data:
                util.print_dict(data, "  data")
