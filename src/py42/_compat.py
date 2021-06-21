"""
This module handles import compatibility issues between Python 2 and
Python 3.
"""
import sys

_ver = sys.version_info

#: Python 2.x?
is_py2 = _ver[0] == 2

if is_py2:
    from urllib import quote
    from urllib import urlencode

    from urlparse import urljoin
    from urlparse import urlparse

    original_str = str
    str = unicode
    str_options = (original_str, str)

    import repr as reprlib

    string_type = basestring

    from UserDict import UserDict

    from UserList import UserList

else:
    from urllib.parse import urljoin
    from urllib.parse import urlparse
    from urllib.parse import quote
    from urllib.parse import urlencode

    str = str
    str_options = (str,)

    import reprlib

    string_type = str

    from collections import UserDict
    from collections import UserList
