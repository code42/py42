class BaseAuthorityClient(object):
    def __init__(self, default_session, v3_required_session):
        self._default_session = default_session
        self._v3_required_session = v3_required_session


class BaseStorageClient(object):
    def __init__(self, session):
        self._session = session


class BaseFileEventClient(object):
    def __init__(self, session):
        self._session = session
