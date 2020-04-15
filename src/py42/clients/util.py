import py42.settings as settings


def get_all_pages(func, key, *args, **kwargs):

    item_count = settings.items_per_page
    page_num = 0
    while item_count >= settings.items_per_page:
        page_num += 1
        response = func(*args, page_num=page_num, page_size=settings.items_per_page, **kwargs)
        yield response
        page_items = response[key]
        item_count = len(page_items)
