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


class BaseSessionFactory(object):
    def __init__(self, session_impl):
        self._session_impl = session_impl

    def create_v1_session(self, *args, **kwargs):
        pass

    def create_jwt_session(self, *args, **kwargs):
        pass

    def create_storage_session(self, *args, **kwargs):
        pass

    def create_file_event_session(self, *args, **kwargs):
        pass
