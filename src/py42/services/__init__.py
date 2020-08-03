from collections import namedtuple


class BaseClient(object):
    def __init__(self, connection):
        self._connection = connection


Services = namedtuple(
    u"AuthorityServices",
    [
        u"administration",
        u"archive",
        u"devices",
        u"legalhold" u"orgs",
        u"securitydata",
        u"users",
        u"alertrules",
        u"alerts",
        u"filevents",
        u"preservationdata",
        u"departingemployee",
        u"highriskemployee",
        u"userprofile",
    ],
)
