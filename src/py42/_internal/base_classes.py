class BaseClient(object):
    def __init__(self, default_session):
        self._default_session = default_session


class BaseAuthorityClient(BaseClient):
    def __init__(self, default_session, v3_required_session):
        super(BaseAuthorityClient, self).__init__(default_session)
        self._default_session = default_session
        self._v3_required_session = v3_required_session
