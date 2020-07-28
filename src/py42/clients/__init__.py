class BaseClient(object):

    __slots__ = ["_session"]

    def __init__(self, session):
        self._session = session
