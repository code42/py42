from collections import namedtuple


class BaseClient(object):
    def __init__(self, cnxn):
        self._connection = cnxn


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
        u"filevents",
        u"savedsearch",
        u"preservationdata",
        u"departingemployee",
        u"highriskemployee",
        u"userprofile",
    ],
)
