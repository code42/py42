from collections import namedtuple

AuthorityClient = namedtuple(
    u"AuthorityClient",
    [
        u"administration",
        u"archive",
        u"devices",
        u"legalhold",
        u"orgs",
        u"securitydata",
        u"users",
    ],
)
