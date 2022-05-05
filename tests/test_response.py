import pytest
from requests import Response

from py42.exceptions import Py42Error
from py42.response import Py42Response

JSON_LIST_WITH_DATA_NODE = (
    '{"data": {"item_list_key": [{"foo": "foo_val"}, {"bar": "bar_val"}]}}'
)
JSON_DICT_WITH_DATA_NODE = '{"data": {"item_list_key": {"foo": "foo_val"}}}'

JSON_LIST_NO_DATA_NODE = '{"item_list_key": [{"foo": "foo_val"}, {"bar": "bar_val"}]}'
JSON_DICT_NO_DATA_NODE = '{"item_list_key": {"foo": "foo_val", "bar": "bar_val"}}'
JSON_DICT_EMPTY_DATA_NODE = '{"data": []}'

PLAIN_TEXT = "TEST_PLAIN_TEXT"


class TestPy42Response:
    @pytest.fixture
    def mock_response_list_data_node(self, mocker):
        mock_response = mocker.MagicMock(spec=Response)
        mock_response.content = JSON_LIST_WITH_DATA_NODE.encode("utf-8")
        mock_response.text = JSON_LIST_WITH_DATA_NODE
        return mock_response

    @pytest.fixture
    def mock_response_list_no_data_node(self, mocker):
        mock_response = mocker.MagicMock(spec=Response)
        mock_response.content = JSON_LIST_NO_DATA_NODE.encode("utf-8")
        mock_response.text = JSON_LIST_NO_DATA_NODE
        return mock_response

    @pytest.fixture
    def mock_response_dict_data_node(self, mocker):
        mock_response = mocker.MagicMock(spec=Response)
        mock_response.content = JSON_DICT_WITH_DATA_NODE.encode("utf-8")
        mock_response.text = JSON_DICT_WITH_DATA_NODE
        return mock_response

    @pytest.fixture
    def mock_response_dict_no_data_node(self, mocker):
        mock_response = mocker.MagicMock(spec=Response)
        mock_response.content = JSON_DICT_NO_DATA_NODE.encode("utf-8")
        mock_response.text = JSON_DICT_NO_DATA_NODE
        return mock_response

    @pytest.fixture
    def mock_response_dict_empty_data_node(self, mocker):
        mock_response = mocker.MagicMock(spec=Response)
        mock_response.content = JSON_DICT_EMPTY_DATA_NODE.encode("utf-8")
        mock_response.text = JSON_DICT_EMPTY_DATA_NODE
        return mock_response

    @pytest.fixture
    def mock_response_not_json(self, mocker):
        mock_response = mocker.MagicMock(spec=Response)
        mock_response.status_code = 200
        mock_response.text = PLAIN_TEXT
        mock_response.url = "http://www.example.com"
        mock_response.headers = [{"name": "value"}]
        return mock_response

    def test_getitem_returns_list_items_with_data_node(
        self, mock_response_list_data_node
    ):
        response = Py42Response(mock_response_list_data_node)
        assert type(response["item_list_key"]) == list

    def test_getitem_returns_dict_keys_with_data_node(
        self, mock_response_dict_data_node
    ):
        response = Py42Response(mock_response_dict_data_node)
        assert type(response["item_list_key"]) == dict

    def test_getitem_returns_list_items_no_data_node(
        self, mock_response_list_no_data_node
    ):
        response = Py42Response(mock_response_list_no_data_node)
        assert type(response["item_list_key"]) == list

    def test_getitem_returns_dict_keys_no_data_node(
        self, mock_response_dict_no_data_node
    ):
        response = Py42Response(mock_response_dict_no_data_node)
        assert type(response["item_list_key"]) == dict

    def test_getitem_returns_empty_list_empty_data_node(
        self, mock_response_dict_empty_data_node
    ):
        response = Py42Response(mock_response_dict_empty_data_node)
        assert response.data == []

    def test_setitem_modifies_dict_keys_with_data_node_to_expected_value(
        self, mock_response_dict_data_node
    ):
        response = Py42Response(mock_response_dict_data_node)
        response["item_list_key"]["foo"] = "newfooval"
        assert response["item_list_key"]["foo"] == "newfooval"

    def test_setitem_modifies_dict_keys_with_no_data_node_to_expected_value(
        self, mock_response_dict_no_data_node
    ):
        response = Py42Response(mock_response_dict_no_data_node)
        response["item_list_key"]["foo"] = "newfooval"
        assert response["item_list_key"]["foo"] == "newfooval"

    def test_setitem_modifies_list_items_with_data_node_to_expected_value(
        self, mock_response_list_data_node
    ):
        response = Py42Response(mock_response_list_data_node)
        response["item_list_key"][0] = "testmodifylistitem"
        assert response["item_list_key"][0] == "testmodifylistitem"

    def test_setitem_modifies_list_items_with_no_data_node_to_expected_value(
        self, mock_response_list_no_data_node
    ):
        response = Py42Response(mock_response_list_no_data_node)
        response["item_list_key"][0] = "testmodifylistitem"
        assert response["item_list_key"][0] == "testmodifylistitem"

    def test_text_json_no_data_node_returns_raw_json(
        self, mock_response_list_no_data_node
    ):
        response = Py42Response(mock_response_list_no_data_node)
        assert response.text == JSON_LIST_NO_DATA_NODE

    def test_raw_text_with_data_node_returns_raw_json_with_data_node(
        self, mock_response_list_data_node
    ):
        response = Py42Response(mock_response_list_data_node)
        assert response.raw_text == JSON_LIST_WITH_DATA_NODE

    def test_raw_text_no_data_node_returns_raw_json_no_data_node(
        self, mock_response_not_json
    ):
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

    def test_iter_can_be_looped_over_multiple_times(
        self, mock_response_dict_no_data_node
    ):
        response = Py42Response(mock_response_dict_no_data_node)
        items = 0
        for _ in response["item_list_key"]:
            items += 1
        assert items == 2

        items = 0

        for _ in response["item_list_key"]:
            items += 1
        assert items == 2

    def test_setitem_raises_py42_error_on_invalid_assignment(
        self, mock_response_not_json
    ):
        response = Py42Response(mock_response_not_json)
        with pytest.raises(Py42Error):
            response[0] = "test"

    def test_getitem_raises_py42_error_on_invalid_subscript(
        self, mock_response_not_json
    ):
        response = Py42Response(mock_response_not_json)
        with pytest.raises(Py42Error):
            response["test"]

    def test_content_dict_no_data_node_returns_expected_dict(
        self, mock_response_dict_no_data_node
    ):
        response = Py42Response(mock_response_dict_no_data_node)
        assert response.content == JSON_DICT_NO_DATA_NODE.encode("utf-8")

    def test_content_dict_data_node_returns_expected_dict(
        self, mock_response_dict_data_node
    ):
        response = Py42Response(mock_response_dict_data_node)
        assert response.content == JSON_DICT_WITH_DATA_NODE.encode("utf-8")

    def test_content_list_no_data_node_returns_expected_list(
        self, mock_response_list_no_data_node
    ):
        response = Py42Response(mock_response_list_no_data_node)
        assert response.content == JSON_LIST_NO_DATA_NODE.encode("utf-8")

    def test_content_list_data_node_returns_expected_list(
        self, mock_response_list_data_node
    ):
        response = Py42Response(mock_response_list_data_node)
        assert response.content == JSON_LIST_WITH_DATA_NODE.encode("utf-8")

    def test_data_with_data_node_returns_list_items(self, mock_response_list_data_node):
        response = Py42Response(mock_response_list_data_node)
        assert type(response.data["item_list_key"]) == list

    def test_data_with_data_node_returns_dict_keys(self, mock_response_dict_data_node):
        response = Py42Response(mock_response_dict_data_node)
        assert type(response.data["item_list_key"]) == dict

    def test_data_no_data_node_returns_list_items_(
        self, mock_response_list_no_data_node
    ):
        response = Py42Response(mock_response_list_no_data_node)
        assert type(response.data["item_list_key"]) == list

    def test_data_no_data_node_returns_dict_keys(self, mock_response_dict_no_data_node):
        response = Py42Response(mock_response_dict_no_data_node)
        assert type(response.data["item_list_key"]) == dict
