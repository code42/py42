class BaseClient(object):

    __slots__ = ["_session"]

    def __init__(self, connection):
        self._connection = connection
