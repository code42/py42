import json


def get_all_pages(func, key, *args, **kwargs):
    import py42.sdk.settings as settings

    item_count = settings.items_per_page
    page_num = 0
    while item_count >= settings.items_per_page:
        page_num += 1
        response = func(*args, page_num=page_num, page_size=settings.items_per_page, **kwargs)
        yield response
        response_dict = json.loads(response.text)
        data_node = response_dict.get(u"data")
        response_dict = data_node or response_dict
        page_items = response_dict[key]
        item_count = len(page_items)
