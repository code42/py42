import json

from py42._internal.compat import reprlib, str
from py42.exceptions import Py42Error


class Py42Response(object):
    def __init__(self, requests_response):
        self._response = requests_response
        self._data_root = None
        try:
            response_dict = json.loads(self._response.text)
            if type(response_dict) == dict:
                self._data_root = response_dict.get(u"data") or response_dict
            else:
                self._data_root = response_dict
        except ValueError:
            self._data_root = self._response.text or u""

    def __getitem__(self, key):
        try:
            return self._data_root[key]
        except TypeError as e:
            data_root_type = type(self._data_root)
            message = u"The Py42Response root is of type {0}, but __getitem__ got a key of {1}, which is incompatible.".format(
                data_root_type, key
            )
            raise Py42Error(message)

    def __setitem__(self, key, value):
        try:
            self._data_root[key] = value
        except TypeError as e:
            data_root_type = type(self._data_root)
            message = u"The Py42Response root is of type {0}, but __setitem__ got a key of {1} and value of {2}, which is incompatible.".format(
                data_root_type, key, value
            )
            raise Py42Error(message)

    def __iter__(self):
        # looping over a Py42Response will loop through list items, dict keys, or str characters
        return iter(self._data_root)

    @property
    def encoding(self):
        """The encoding used to decode the response text."""
        return self._response.encoding

    @property
    def headers(self):
        """A case-insensitive dictionary of response headers."""
        return self._response.headers

    def iter_content(self, chunk_size=1, decode_unicode=False):
        """Iterates over the response data. When ``stream=True`` is set on the request, this avoids
        reading the content at once into memory for large responses.

        Args:
            chunk_size (int, optional): The number of bytes it should read into memory. A value of
                None will function differently depending on the value of `stream`. stream=True will
                read data as it arrives in whatever size the chunks are received. If stream=False,
                data is returned as a single chunk. This is not necessarily the length of each
                item. Defaults to 1.
            decode_unicode (bool, optional): If True, content will be decoded using the best
                available encoding based on the response. Defaults to False.
        """
        return self._response.iter_content(chunk_size=chunk_size, decode_unicode=decode_unicode)

    @property
    def raw_text(self):
        """The ``response.Response.text`` property. It contains raw metadata that is not included in
        the Py42Response.text property."""
        return self._response.text

    @property
    def text(self):
        """The more useful parts of the HTTP response dumped into a dictionary."""
        return json.dumps(self._data_root) if type(self._data_root) != str else self._data_root

    @property
    def url(self):
        """The final URL location of response."""
        return self._response.url

    @property
    def status_code(self):
        """An integer code of the response HTTP Status, e.g. 404 or 200."""
        return self._response.status_code

    def __str__(self):
        return str(self._data_root)

    def __repr__(self):
        data = self._data_root
        return u"<{} [status={}, data={}]>".format(
            self.__class__.__name__, self._response.status_code, reprlib.repr(data)
        )
