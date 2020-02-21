import json


def get_all_pages(func, page_size, key, *args, **kwargs):
    item_count = page_size
    page_num = 0
    while item_count >= page_size:
        page_num += 1
        response = func(*args, page_num=page_num, page_size=page_size, **kwargs)
        yield response
        response_dict = json.loads(response.text)
        response_dict = response_dict.get(u"data") if response_dict.get(u"data") else response_dict
        page_items = response_dict[key]
        item_count = len(page_items)
