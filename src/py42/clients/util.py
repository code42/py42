import py42.settings as settings


def get_all_pages(func, key, *args, **kwargs):
    page_num = 0
    page_size = kwargs.get("page_size") or settings.items_per_page
    item_count = page_size
    while item_count >= page_size:
        page_num += 1
        response = func(*args, page_num=page_num, page_size=page_size, **kwargs)
        yield response
        page_items = response[key]
        item_count = len(page_items)
