from collections import namedtuple


class BaseService(object):

    __slots__ = ["_connection"]

    def __init__(self, connection):
        self._connection = connection


Services = namedtuple(
    u"Services",
    [
        u"administration",
        u"archive",
        u"devices",
        u"legalhold",
        u"orgs",
        u"securitydata",
        u"users",
        u"alertrules",
        u"alerts",
        u"fileevents",
        u"savedsearch",
        u"preservationdata",
        u"departingemployee",
        u"highriskemployee",
        u"userprofile",
    ],
)
