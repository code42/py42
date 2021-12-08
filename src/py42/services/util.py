import re

import py42.settings as settings


def get_all_pages(func, key, *args, **kwargs):
    if kwargs.get("page_size") is None:
        kwargs["page_size"] = settings.items_per_page

    item_count = page_size = kwargs["page_size"]
    page_num = 0
    while item_count >= page_size:
        page_num += 1
        response = func(*args, page_num=page_num, **kwargs)
        yield response
        page_items = response[key] if key else response.data
        item_count = len(page_items)


def escape_quote_chars(token):
    """
    The `nextPgToken` returned in Forensic Search requests with > 10k results is the eventId
    of the last event returned in the response. Some eventIds have double-quote chars in
    them, which need to be escaped when passing the token in the next search request.
    """
    if not isinstance(token, (str, bytes)):
        return token

    unescaped_quote_pattern = r'[^\\]"'

    return re.sub(
        pattern=unescaped_quote_pattern,
        repl=lambda match: match.group().replace('"', r"\""),
        string=token,
    )
