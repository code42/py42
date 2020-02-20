import json


def get_all_pages(func, page_size, key, *args, **kwargs):
    item_count = page_size
    page_num = 0
    while item_count >= page_size:
        page_num += 1
        response = func(*args, page_num=page_num, page_size=page_size, **kwargs)
        yield response
        page_items = json.loads(response.text)["data"][key]
        item_count = len(page_items)
