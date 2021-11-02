import json as json_lib
from threading import Lock
from urllib.parse import urljoin
from urllib.parse import urlparse

from requests.adapters import HTTPAdapter
from requests.exceptions import HTTPError
from requests.models import Request
from requests.sessions import Session

import py42.settings as settings
from py42.exceptions import Py42DeviceNotConnectedError
from py42.exceptions import Py42Error
from py42.exceptions import Py42FeatureUnavailableError
from py42.exceptions import raise_py42_error
from py42.response import Py42Response
from py42.services._auth import C42RenewableAuth
from py42.settings import debug
from py42.util import format_dict

SESSION_ADAPTER = HTTPAdapter(pool_connections=200, pool_maxsize=4, pool_block=True)

ROOT_SESSION = Session()
ROOT_SESSION.mount("https://", SESSION_ADAPTER)
ROOT_SESSION.mount("http://", SESSION_ADAPTER)
ROOT_SESSION.headers = {
    "Accept-Encoding": "gzip, deflate",
    "Connection": "keep-alive",
}


class HostResolver:
    def get_host_address(self):
        raise NotImplementedError()


class KnownUrlHostResolver(HostResolver):
    def __init__(self, host_address):
        self._host_address = host_address

    def get_host_address(self):
        return self._host_address


class MicroservicePrefixHostResolver(HostResolver):
    def __init__(self, connection, prefix):
        self._connection = connection
        self._prefix = prefix

    def get_host_address(self):
        sts_url = self._get_sts_base_url()
        return sts_url.replace("sts", self._prefix, 1)

    def _get_sts_base_url(self):
        uri = "/api/v1/ServerEnv"
        response = self._connection.get(uri)

        response_json = json_lib.loads(response.text)
        sts_base_url = response_json.get("stsBaseUrl")

        if not sts_base_url:
            raise Py42FeatureUnavailableError(response)

        return sts_base_url


class MicroserviceKeyHostResolver(HostResolver):
    def __init__(self, kv_service, key):
        self._kv_service = kv_service
        self._key = key

    def get_host_address(self):
        return self._kv_service.get_stored_value(self._key).text


class ConnectedServerHostResolver(HostResolver):
    """A connection used in Push Restores to verify the accepting device is connected
    to the Authority server."""

    def __init__(self, connection, device_guid):
        self._connection = connection
        self._device_guid = device_guid
        super().__init__()

    def get_host_address(self):
        response = self._connection.get(
            "api/v1/connectedServerUrl", params={"guid": self._device_guid}
        )
        if response["serverUrl"] is None:
            raise Py42DeviceNotConnectedError(response, self._device_guid)
        return response["serverUrl"]


class Connection:
    def __init__(self, host_resolver, auth=None, session=None):
        self._host_resolver = host_resolver
        self._session = session or ROOT_SESSION
        self._headers = self._session.headers.copy()
        self._auth = auth
        self._resolve_lock = Lock()
        self._host_address = None

    @classmethod
    def from_host_address(cls, host_address, auth=None, session=None):
        host_resolver = KnownUrlHostResolver(host_address)
        return cls(host_resolver, auth=auth, session=session)

    @classmethod
    def from_microservice_key(cls, kv_service, key, auth=None, session=None):
        host_resolver = MicroserviceKeyHostResolver(kv_service, key)
        return cls(host_resolver, auth=auth, session=session)

    @classmethod
    def from_microservice_prefix(cls, connection, prefix, auth=None, session=None):
        host_resolver = MicroservicePrefixHostResolver(connection, prefix)
        return cls(host_resolver, auth=auth, session=session)

    @classmethod
    def from_device_connection(cls, connection, device_guid):
        host_resolver = ConnectedServerHostResolver(connection, device_guid)
        return cls(host_resolver, auth=connection._auth)

    @property
    def host_address(self):
        return self._get_host_address()

    def clone(self, host_address):
        host_resolver = KnownUrlHostResolver(host_address)
        return Connection(host_resolver, auth=self._auth)

    def get(self, url, **kwargs):
        return self.request("GET", url, **kwargs)

    def options(self, url, **kwargs):
        return self.request("OPTIONS", url, **kwargs)

    def head(self, url, **kwargs):
        return self.request("HEAD", url, **kwargs)

    def post(self, url, data=None, json=None, **kwargs):
        return self.request("POST", url, data=data, json=json, **kwargs)

    def put(self, url, data=None, json=None, **kwargs):
        return self.request("PUT", url, data=data, json=json, **kwargs)

    def patch(self, url, data=None, json=None, **kwargs):
        return self.request("PATCH", url, data=data, json=json, **kwargs)

    def delete(self, url, **kwargs):
        return self.request("DELETE", url, **kwargs)

    def request(
        self,
        method,
        url,
        params=None,
        data=None,
        json=None,
        headers=None,
        cookies=None,
        files=None,
        auth=None,
        hooks=None,
        stream=False,
        timeout=60,
        cert=None,
        proxies=None,
    ):
        response = None
        for _ in range(2):
            request = self._prepare_request(
                method,
                url,
                params=params,
                data=data,
                json=json,
                headers=headers,
                cookies=cookies,
                files=files,
                auth=auth,
                hooks=hooks,
            )
            response = self._session.send(
                request,
                stream=stream,
                timeout=timeout,
                verify=settings.verify_ssl_certs,
                cert=cert,
                proxies=proxies or settings.proxies,
            )

            if response is not None:
                debug.logger.info(f"Response status: {response.status_code}")
                if not stream:
                    # setting this manually speeds up read times
                    response.encoding = "utf-8"
                    debug.logger.debug(f"Response data: {response.text}")
                else:
                    debug.logger.debug("Response data: <streamed>")

                if 200 <= response.status_code <= 399:
                    return Py42Response(response)

                if response.status_code == 401:
                    if isinstance(self._auth, C42RenewableAuth):
                        self._auth.clear_credentials()
            else:
                debug.logger.debug("Error! Could not retrieve response.")

        # if nothing has been returned after two attempts, something went wrong
        _handle_error(method, url, response)

    def _prepare_request(
        self,
        method,
        url,
        params=None,
        data=None,
        json=None,
        headers=None,
        cookies=None,
        files=None,
        auth=None,
        hooks=None,
    ):
        url = urljoin(self.host_address, url)
        self._session.proxies = settings.proxies
        self._session.verify = settings.verify_ssl_certs

        headers = headers or {}
        headers.update(self._headers)
        if data and "Content-Type" not in headers:
            headers.update({"Content-Type": "application/json"})
        if "Accept" not in headers:
            headers.update({"Accept": "application/json"})
        headers = _create_user_headers(headers)

        _print_request(method, url, params=params, data=data, json=json)

        if isinstance(data, str):
            data = data.encode("utf-8")

        request = Request(
            method=method,
            url=url,
            headers=headers,
            files=files,
            data=data,
            json=json,
            params=params,
            auth=auth or self._auth,
            cookies=cookies,
            hooks=hooks,
        )

        return self._session.prepare_request(request)

    def _get_host_address(self):
        if not self._host_address:
            with self._resolve_lock:
                if not self._host_address:
                    host = self._host_resolver.get_host_address()
                    self._init_host_info(host)
        return self._host_address

    def _init_host_info(self, host):
        if not host.startswith("http://") and not host.startswith("https://"):
            host = f"https://{host}"
        parsed_host = urlparse(host)
        self._headers["Host"] = parsed_host.netloc
        self._host_address = host


def _create_user_headers(headers):
    user_headers = {"User-Agent": settings.get_user_agent_string()}
    if headers:
        user_headers.update(headers)
    return user_headers


def _handle_error(method, url, response):
    if response is None:
        msg = f"No response was returned for {method} request to {url}."
        raise Py42Error(msg)

    try:
        response.raise_for_status()
    except HTTPError as ex:
        raise_py42_error(ex)


def _print_request(method, url, params=None, data=None, json=None):
    debug.logger.info(f"{method.ljust(8)}{url}")
    if params:
        debug.logger.debug(format_dict(params, "  params"))
    if json:
        debug.logger.debug(format_dict(json, "  json"))
    if data:
        debug.logger.debug(data, "  data")
