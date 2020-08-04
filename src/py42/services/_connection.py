from __future__ import print_function

import json

from requests.adapters import HTTPAdapter
from requests.exceptions import HTTPError
from requests.models import Request
from requests.sessions import Session

import py42.settings as settings
from py42._compat import urljoin
from py42._compat import urlparse
from py42.exceptions import Py42Error
from py42.exceptions import Py42FeatureUnavailableError
from py42.exceptions import Py42SessionInitializationError
from py42.exceptions import raise_py42_error
from py42.response import Py42Response
from py42.services._auth import C42AuthBase
from py42.settings import debug
from py42.util import format_dict

SESSION_ADAPTER = HTTPAdapter(pool_connections=200, pool_maxsize=4, pool_block=True)

ROOT_SESSION = Session()
ROOT_SESSION.mount(u"https://", SESSION_ADAPTER)
ROOT_SESSION.mount(u"http://", SESSION_ADAPTER)
ROOT_SESSION.headers = {
    u"Accept": u"application/json",
    u"Content-Type": u"application/json",
    u"Accept-Encoding": u"gzip, deflate",
    u"Connection": u"keep-alive",
}


class Connection(object):
    def __init__(self, auth=None, session=None):
        self._session = session or ROOT_SESSION
        self._auth = auth
        self._host_address = None

    @property
    def host_address(self):
        if not self._host_address:
            self._host_address = self._init_host_info()
        return self._host_address

    @property
    def headers(self):
        return self._session.headers

    @property
    def proxies(self):
        return self._session.proxies

    def get(self, url, **kwargs):
        return self.request(u"GET", url, **kwargs)

    def options(self, url, **kwargs):
        return self.request(u"OPTIONS", url, **kwargs)

    def head(self, url, **kwargs):
        return self.request(u"HEAD", url, **kwargs)

    def post(self, url, data=None, **kwargs):
        return self.request(u"POST", url, data=data, **kwargs)

    def put(self, url, data=None, **kwargs):
        return self.request(u"PUT", url, data=data, **kwargs)

    def patch(self, url, data=None, **kwargs):
        return self.request(u"PATCH", url, data=data, **kwargs)

    def delete(self, url, **kwargs):
        return self.request(u"DELETE", url, **kwargs)

    def request(
        self,
        method,
        url,
        params=None,
        data=None,
        headers=None,
        cookies=None,
        files=None,
        auth=None,
        hooks=None,
        stream=False,
        timeout=60,
        verify=True,
        cert=None,
        proxies=None,
    ):
        response = None
        request = self._prepare_request(
            method,
            url,
            params=params,
            data=data,
            headers=headers,
            cookies=cookies,
            files=files,
            auth=auth,
            hooks=hooks,
        )

        for _ in range(2):
            response = self._session.send(
                request,
                stream=stream,
                timeout=timeout,
                verify=verify,
                cert=cert,
                proxies=proxies,
            )

            if not stream:
                # setting this manually speeds up read times
                response.encoding = u"utf-8"

            if 200 <= response.status_code <= 299:
                return Py42Response(response)

            if isinstance(C42AuthBase, self._auth):
                self._auth.clear_credentials()

        # if nothing has been returned after two attempts, something went wrong
        _handle_error(response)

    def _prepare_request(
        self,
        method,
        url,
        params=None,
        data=None,
        headers=None,
        cookies=None,
        files=None,
        auth=None,
        hooks=None,
    ):
        url = urljoin(self.host_address, url)
        self._session.proxies = settings.proxies
        self._session.verify = settings.verify_ssl_certs

        additional_headers = {u"User-Agent": settings.get_user_agent_string()}
        if headers:
            additional_headers = additional_headers.update(headers)

        request = Request(
            method=method,
            url=url,
            headers=additional_headers,
            files=files,
            data=data,
            params=params,
            auth=auth or self._auth,
            cookies=cookies,
            hooks=hooks,
        )

        _print_request(method, url, params=params, data=data)

        return request.prepare()

    def _get_host_address(self):
        raise NotImplementedError()

    def _init_host_info(self):
        host = self._get_host_address()
        if not host.startswith(u"http://") and not host.startswith(u"https://"):
            host = u"https://{}".format(host)
        parsed_host = urlparse(host)
        self._session.headers[u"Host"] = parsed_host.netloc
        return host


class KnownUrlConnection(Connection):
    def __init__(self, host_address, auth=None, session=None):
        super(KnownUrlConnection, self).__init__(auth=auth, session=session)
        self._known_host_address = host_address

    def _get_host_address(self):
        return self._known_host_address


class KeyValueStoreConnection(Connection):
    def __init__(self, auth=None, session=None):
        super(KeyValueStoreConnection, self).__init__(auth=auth, session=session)

    def _get_host_address(self):
        sts_url = self._get_sts_base_url()
        return sts_url.replace(u"sts", u"key-value-store")

    def _get_sts_base_url(self):
        uri = u"/api/ServerEnv"
        try:
            response = self.get(uri)
        except HTTPError as ex:
            raise Py42SessionInitializationError(ex)

        response_json = json.loads(response.text)
        sts_base_url = response_json.get(u"stsBaseUrl")

        if not sts_base_url:
            raise Py42FeatureUnavailableError()

        return sts_base_url


class MicroserviceConnection(Connection):
    def __init__(self, kvs_connection, key, auth=None, session=None):
        super(MicroserviceConnection, self).__init__(auth=auth, session=session)
        self._kvs_connection = kvs_connection
        self._key = key

    def _get_host_address(self):
        return self._kvs_connection.get_stored_value(self._key).text


def _handle_error(method, url, response):
    if not response:
        msg = u"No response was returned for {} request to {}.".format(method, url)
        raise Py42Error(msg)

    try:
        response.raise_for_status()
    except HTTPError as ex:
        raise_py42_error(ex)


def _print_request(method, url, params=None, data=None):
    debug.logger.info(u"{}{}".format(method.ljust(8), url))
    if params:
        debug.logger.debug(format_dict(params, u"  params"))
    if data:
        debug.logger.debug(format_dict(data, u"  data"))
