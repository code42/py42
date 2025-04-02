import pytest
from tests.conftest import create_mock_response

import pycpg.settings as settings
from pycpg.services.util import get_all_pages


@pytest.fixture
def empty_response(mocker):
    return create_mock_response(mocker, '{"items": []}')


@pytest.fixture
def get_three_three_item_pages(mocker, empty_response):
    response = create_mock_response(mocker, '{"items": [1, 2, 3]}')
    mock = mocker.MagicMock()
    mock.side_effect = [response, response, response, empty_response]
    return mock


def verify_calls(func, page_size):
    assert func.call_args_list[0][1]["page_num"] == 1
    assert func.call_args_list[1][1]["page_num"] == 2
    assert func.call_args_list[2][1]["page_num"] == 3
    assert func.call_args_list[3][1]["page_num"] == 4
    assert func.call_args_list[0][1]["page_size"] == page_size
    assert func.call_args_list[1][1]["page_size"] == page_size
    assert func.call_args_list[2][1]["page_size"] == page_size
    assert func.call_args_list[3][1]["page_size"] == page_size
    assert func.call_count == 4


def test_get_all_pages_with_no_input_page_size_calls_callback_with_expected_values(
    get_three_three_item_pages,
):
    settings.items_per_page = 3
    for _ in get_all_pages(get_three_three_item_pages, "items"):
        pass

    settings.items_per_page = 500
    verify_calls(get_three_three_item_pages, 3)


def test_get_all_pages_with_input_page_size_less_than_default_calls_callback_with_expected_values(
    get_three_three_item_pages,
):
    settings.items_per_page = 100
    for _ in get_all_pages(get_three_three_item_pages, "items", page_size=3):
        pass

    settings.items_per_page = 500
    verify_calls(get_three_three_item_pages, 3)


def test_get_all_pages_with_input_page_size_greater_than_default_calls_callback_with_expected_values(
    get_three_three_item_pages,
):
    settings.items_per_page = 1
    for _ in get_all_pages(get_three_three_item_pages, "items", page_size=3):
        pass

    settings.items_per_page = 500
    verify_calls(get_three_three_item_pages, 3)
