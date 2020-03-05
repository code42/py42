import json
from py42._internal.compat import reprlib, str


class Py42Response(object):
    def __init__(self, requests_response, json_key=None):
        self._response = requests_response
        self._json_key = json_key
        response_dict = json.loads(self.api_response.text)
        self._data_root = response_dict.get(u"data") or response_dict

    def __getitem__(self, key):
        item_root = self._data_root[self._json_key] if self._json_key else self._data_root
        return item_root[key]

    @property
    def raw_json(self):
        return json.dumps(self._data_root)

    @property
    def api_response(self):
        return self._response

    def __str__(self):
        return str(self._data_root)

    def __repr__(self):
        return u"<{} [status={}, data={}]>".format(
            self.__class__.__name__, self._response.status_code, reprlib.repr(self._data_root)
        )
