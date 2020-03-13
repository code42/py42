import pytest
from requests import Response

from py42.sdk.response import Py42Response

JSON_LIST_WITH_DATA_NODE = '{"data": {"item_list_key": [{"foo": "foo_val"}, {"bar": "bar_val"}]}}'
JSON_DICT_WITH_DATA_NODE = '{"data": {"item_list_key": {"foo": "foo_val"}}}'

JSON_LIST_NO_DATA_NODE = '{"item_list_key": [{"foo": "foo_val"}, {"bar": "bar_val"}]}'
JSON_DICT_NO_DATA_NODE = '{"item_list_key": {"foo": "foo_val"}}'

PLAIN_TEXT = "TEST_PLAIN_TEXT"


class TestPy42Response(object):
    @pytest.fixture
    def mock_response_list_data_node(self, mocker):
        mock_response = mocker.MagicMock(spec=Response)
        mock_response.text = JSON_LIST_WITH_DATA_NODE
        return mock_response

    @pytest.fixture
    def mock_response_list_no_data_node(self, mocker):
        mock_response = mocker.MagicMock(spec=Response)
        mock_response.text = JSON_LIST_NO_DATA_NODE
        return mock_response

    @pytest.fixture
    def mock_response_dict_data_node(self, mocker):
        mock_response = mocker.MagicMock(spec=Response)
        mock_response.text = JSON_DICT_WITH_DATA_NODE
        return mock_response

    @pytest.fixture
    def mock_response_dict_no_data_node(self, mocker):
        mock_response = mocker.MagicMock(spec=Response)
        mock_response.text = JSON_DICT_NO_DATA_NODE
        return mock_response

    @pytest.fixture
    def mock_response_not_json(self, mocker):
        mock_response = mocker.MagicMock(spec=Response)
        mock_response.status_code = 200
        mock_response.text = PLAIN_TEXT
        mock_response.url = "http://www.example.com"
        mock_response.headers = [{"name": "value"}]
        return mock_response

    def test_getitem_returns_list_items_with_data_node(self, mock_response_list_data_node):
        response = Py42Response(mock_response_list_data_node)
        assert type(response["item_list_key"]) == list

    def test_getitem_returns_dict_keys_with_data_node(self, mock_response_dict_data_node):
        response = Py42Response(mock_response_dict_data_node)
        assert type(response["item_list_key"]) == dict

    def test_getitem_returns_list_items_no_data_node(self, mock_response_list_no_data_node):
        response = Py42Response(mock_response_list_no_data_node)
        assert type(response["item_list_key"]) == list

    def test_getitem_returns_dict_keys_no_data_node(self, mock_response_dict_no_data_node):
        response = Py42Response(mock_response_dict_no_data_node)
        assert type(response["item_list_key"]) == dict

    def test_text_json_no_data_node_returns_raw_json(self, mock_response_list_no_data_node):
        response = Py42Response(mock_response_list_no_data_node)
        assert response.text == JSON_LIST_NO_DATA_NODE

    def test_raw_text_with_data_node_returns_raw_json_with_data_node(
        self, mock_response_list_data_node
    ):
        response = Py42Response(mock_response_list_data_node)
        assert response.raw_text == JSON_LIST_WITH_DATA_NODE

    def test_raw_text_with_data_node_returns_raw_json_with_data_node(
        self, mock_response_list_data_node
    ):
        response = Py42Response(mock_response_list_data_node)
        assert response.raw_text == JSON_LIST_WITH_DATA_NODE

    def test_raw_text_no_data_node_returns_raw_json_no_data_node(self, mock_response_not_json):
        response = Py42Response(mock_response_not_json)
        assert response.raw_text == PLAIN_TEXT

    def test_status_code_returns_expected_value(self, mock_response_not_json):
        response = Py42Response(mock_response_not_json)
        assert response.status_code == 200

    def test_status_code_returns_expected_url(self, mock_response_not_json):
        response = Py42Response(mock_response_not_json)
        assert response.url == "http://www.example.com"

    def test_headers_returns_request_headers(self, mock_response_not_json):
        response = Py42Response(mock_response_not_json)
        assert response.headers == mock_response_not_json.headers

    def test_iter_content_calls_request_iter_content(self, mock_response_not_json):
        response = Py42Response(mock_response_not_json)
        response.iter_content(128, True)
        mock_response_not_json.iter_content.assert_called_once_with(
            chunk_size=128, decode_unicode=True
        )
