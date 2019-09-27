import math

import py42.util as util


def for_each_api_item(
    init_response,
    obj_retriever,
    py42_page_size,
    py42_callback=None,
    py42_datakey=None,
    py42_return_each_page=False,
    **kwargs
):
    def process_page(response):
        _foreach_response(response, py42_callback, py42_datakey, py42_return_each_page)

    total_count = util.get_obj_from_response(init_response, "totalCount")

    process_page(init_response)

    pages = int(math.ceil(float(total_count) / float(py42_page_size)))

    if pages > 1:
        for i in range(1, pages):  # skip the first page since we already handled that above
            page_num = i + 1
            obj_retriever(page_num=page_num, page_size=py42_page_size, then=process_page, **kwargs)


def _foreach_response(response, py42_callback, py42_datakey, py42_return_each_page):
    items = util.get_obj_from_response(response, py42_datakey)
    if py42_return_each_page:
        py42_callback(items)
    else:
        for item in items:
            py42_callback(item)
