import json
import math


def get_obj_from_response(response, data_key):
    if response.content and 200 <= response.status_code < 300:
        response_json = json.loads(response.content)
        if "data" in response_json:
            data = response_json["data"]
            if data_key == "data":
                return data
            if data_key in data:
                return data[data_key]
    else:
        return []


def for_each_api_item(init_response, obj_retriever, foreach_page_size, foreach_user_callback=None, foreach_datakey=None,
                      foreach_return_each_page=False, **kwargs):
    total_count = get_obj_from_response(init_response, "totalCount")
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
    items = get_obj_from_response(response, foreach_datakey)
    if foreach_return_each_page:
        foreach_user_callback(items, **kwargs)
    else:
        for item in items:
            foreach_user_callback(item, **kwargs)


def format_json(json_string):
    parsed = json.loads(json_string)
    return json.dumps(parsed, indent=4)


def print_response(response):
    try:
        print format_json(response.content)
    except ValueError, e:
        print response


def print_dict(dict_):
    print json.dumps(dict_, indent=4)
