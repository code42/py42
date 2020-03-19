import json

from py42._internal.compat import reprlib, str


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

        # looping over a Py42Response will loop through list items, dict keys, or str characters
        self._iter = iter(self._data_root)

    def __getitem__(self, key):
        return self._data_root[key]

    def __iter__(self):
        return self._iter

    @property
    def encoding(self):
        return self._response.encoding

    @property
    def headers(self):
        return self._response.headers

    def iter_content(self, chunk_size=1, decode_unicode=False):
        return self._response.iter_content(chunk_size=chunk_size, decode_unicode=decode_unicode)

    @property
    def raw_text(self):
        return self._response.text

    @property
    def text(self):
        return json.dumps(self._data_root) if type(self._data_root) != str else self._data_root

    @property
    def url(self):
        return self._response.url

    @property
    def status_code(self):
        return self._response.status_code

    def __str__(self):
        return str(self._data_root)

    def __repr__(self):
        data = self._data_root
        return u"<{} [status={}, data={}]>".format(
            self.__class__.__name__, self._response.status_code, reprlib.repr(data)
        )
