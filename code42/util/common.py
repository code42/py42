import json
import math
from code42.http import Session, BatchAsyncSession


def create_session(host_address, auth_handler, proxies, is_async):
    session_type = BatchAsyncSession if is_async else Session
    session = session_type(host_address, auth_handler=auth_handler, proxies=proxies)
    return session


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


def for_each_api_item(init_response, obj_retriever, foreach_pg_size, foreach_user_callback=None, foreach_datakey=None,
                      **kwargs):

        total_count = get_obj_from_response(init_response, "totalCount")
        _foreach_response(init_response, foreach_user_callback, foreach_datakey, **kwargs)
        pages = int(math.ceil(float(total_count) / float(foreach_pg_size)))
        if pages > 1:
            for i in range(1, pages):  # skip the first page since we already handled that above
                page_num = i + 1
                obj_retriever(page_num=page_num, page_size=foreach_pg_size, then=_foreach_response,
                              foreach_user_callback=foreach_user_callback, foreach_datakey=foreach_datakey,
                              **kwargs)


def _foreach_response(response, foreach_user_callback, foreach_datakey, **kwargs):
    items = get_obj_from_response(response, foreach_datakey)
    for item in items:
        foreach_user_callback(item, **kwargs)


class Mock(object):
    pass

# response = common.Mock()
# response.status_code = 200
# response.content = '{"data": { "planUid": "846303360879104736", "storageNodeGuids": ["702656942434102401"] }}'
