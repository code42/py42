import py42.settings as settings


def get_all_pages(func, key, *args, **kwargs):
    if kwargs.get("page_num") is None:
        kwargs["page_num"] = 0
    if kwargs.get("page_size") is None:
        kwargs["page_size"] = settings.items_per_page
    item_count = kwargs["page_size"]
    while item_count >= kwargs["page_size"]:
        kwargs["page_num"] += 1
        response = func(*args, **kwargs)
        yield response
        page_items = response[key]
        item_count = len(page_items)
