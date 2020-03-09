import json

from py42._internal.compat import reprlib, str


class Py42Response(object):
    def __init__(self, requests_response, json_key=None):
        self._response = requests_response
        self._json_key = json_key
        self._data_root = None
        if self._response.text:
            try:
                response_dict = json.loads(self._response.text)
                print(response_dict)
                self._data_root = response_dict.get(u"data") or response_dict
                if type(self._data_root) is dict:
                    self._data_root = self._data_root.get(json_key) or self._data_root
            except ValueError:
                pass

    def __getitem__(self, key):
        return self._data_root[key]

    @property
    def raw_response_text(self):
        return json.dumps(self._data_root) if self._data_root else self._response.text

    @property
    def api_response(self):
        return self._response

    def __str__(self):
        return str(self._data_root) if self._data_root else self._response.text

    def __repr__(self):
        data = self._data_root or self._response.text
        return u"<{} [status={}, data={}]>".format(
            self.__class__.__name__, self._response.status_code, reprlib.repr(data)
        )
