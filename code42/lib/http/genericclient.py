from .authhandling import AuthHandler, BasicAuthProvider, HeaderApplier
import sessionfactory


class GenericClient(object):
    def __init__(self, session):
        self._session = session

    @classmethod
    def create_with_basic_auth(cls, host_address, username, password):
        fetcher = BasicAuthProvider(username, password)
        applier = HeaderApplier(value_format="Basic {}")
        handler = AuthHandler(fetcher, applier)
        session = sessionfactory.create_session(host_address, handler=handler)
        return cls(session)

    @property
    def host_address(self):
        return self._session.host_address

    @property
    def proxies(self):
        return self._session.proxies

    @property
    def session(self):
        return self._session

    def get(self, uri, **kwargs):
        return self.send("GET", uri, **kwargs)

    def head(self, uri, **kwargs):
        return self.send("HEAD", uri, **kwargs)

    def options(self, uri, **kwargs):
        return self.send("OPTIONS", uri, **kwargs)

    def put(self, uri, data=None, **kwargs):
        return self.send("PUT", uri, data=data, **kwargs)

    def post(self, uri, data=None, **kwargs):
        return self.send("POST", uri, data=data, **kwargs)

    def patch(self, uri, data=None, **kwargs):
        return self.send("PATCH", uri, data=data, **kwargs)

    def delete(self, uri, data=None, **kwargs):
        return self.send("DELETE", uri, data=data, **kwargs)

    def send(self, method, uri, **kwargs):
        try:
            return self._session.request(method, uri, **kwargs)
        except Exception as e:
            message = "Failed to get a success response from " + method + " request to " + uri + " or a request " \
                      + "sent by one of its callbacks"
            raise Exception(message + ", caused by: " + e.message)

    def wait(self):
        if "wait" in dir(self._session):
            self._session.wait()
