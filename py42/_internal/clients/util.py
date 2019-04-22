import math

import py42.util as util


def for_each_api_item(init_response, obj_retriever, foreach_page_size, foreach_user_callback=None, foreach_datakey=None,
                      foreach_return_each_page=False, **kwargs):
    total_count = util.get_obj_from_response(init_response, "totalCount")
    _foreach_response(init_response, foreach_user_callback, foreach_datakey, foreach_return_each_page, **kwargs)
    pages = int(math.ceil(float(total_count) / float(foreach_page_size)))
    if pages > 1:
        for i in range(1, pages):  # skip the first page since we already handled that above
            page_num = i + 1

            def get_page(response):
                _foreach_response(response, foreach_user_callback, foreach_datakey,
                                  foreach_return_each_page, **kwargs)

            obj_retriever(page_num=page_num, page_size=foreach_page_size, then=get_page)


def _foreach_response(response, foreach_user_callback, foreach_datakey, foreach_return_each_page, **kwargs):
    items = util.get_obj_from_response(response, foreach_datakey)
    if foreach_return_each_page:
        foreach_user_callback(items, **kwargs)
    else:
        for item in items:
            foreach_user_callback(item, **kwargs)
