from requests.models import Response, Request
import requests

from py42._internal.session import Py42Session


def successful_request(func):
    def mock_request(method, url, headers=None, files=None, data=None, params=None, auth=None, cookies=None,
                     hooks=None, json=None, **kwargs):
        request = Request(method=method, url=url, headers=headers, files=files, data=data, params=params, auth=auth,
                          cookies=cookies, hooks=hooks, json=json)
        response = Response()
        response.status_code = 200
        response.request = request
        response.url = url
        if func:
            response = func(response)
        return response

    return mock_request


class MockRequestsSession(requests.Session):
    def __init__(self, request_handler=None):
        self._request_handler = request_handler
        super(MockRequestsSession, self).__init__()

    def request(self, method, url, params=None, data=None, headers=None, cookies=None, files=None, auth=None,
                timeout=None, allow_redirects=True, proxies=None, hooks=None, stream=None, verify=None, cert=None,
                json=None):
        return self._request_handler(method, url,
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
                                     json=None)


class MockPy42Session(Py42Session):
    def __init__(self, host_address, auth_handler=None, request_handler=None):
        super(MockPy42Session, self).__init__(MockRequestsSession(request_handler), host_address,
                                              auth_handler=auth_handler)
