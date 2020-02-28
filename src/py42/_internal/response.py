import json


class Py42Response(object):
    def __init__(self, requests_response, json_key):
        self._response = requests_response
        self._json_key = json_key
        response_dict = json.loads(self._response.text)
        self._data_root = response_dict.get("data") or response_dict

    def __getitem__(self, key):
        item_root = self._data_root[self._json_key]
        return item_root[key]

    @property
    def raw_json(self):
        return json.dumps(self._data_root)

    @property
    def api_response(self):
        return self._response
