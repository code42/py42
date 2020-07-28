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

    from urlparse import urljoin, urlparse

    str = unicode

    import repr as reprlib

    string_type = basestring
else:
    from urllib.parse import urljoin, urlparse, quote

    str = str

    import reprlib

    string_type = str
