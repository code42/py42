from collections import namedtuple

AuthorityClient = namedtuple(
    "AuthorityClient",
    ["administration", "archive", "devices", "legalhold", "orgs", "users"],
)
