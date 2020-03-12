import pytest
from requests import Response

from py42.sdk.response import Py42Response

JSON_LIST_WITH_DATA_NODE = '{"data": {"item_list_key": [{"foo": "foo_val"}, {"bar": "bar_val"}]}}'
JSON_DICT_WITH_DATA_NODE = '{"data": {"item_list_key": {"foo": "foo_val"}}}'
JSON_LIST_NO_DATA_NODE = '{"item_list_key": [{"foo": "foo_val"}, {"bar": "bar_val"}]}'
JSON_DICT_NO_DATA_NODE = '{"item_list_key": {"foo": "foo_val"}}'


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

    def test_body_content_with_data_node_returns_raw_json(self, mock_response_list_data_node):
        response = Py42Response(mock_response_list_data_node)
        assert response.body_content == JSON_LIST_WITH_DATA_NODE
