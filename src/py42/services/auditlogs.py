from py42 import settings
from py42.services import BaseService
from py42.services.util import get_all_pages
from py42.util import convert_timestamp_to_str
from py42.util import to_list


class AuditLogsService(BaseService):
    def get_page(self, page_num, page_size=None, **kwargs):

        event_types = to_list(kwargs.pop(u"event_types"))
        user_ids = to_list(kwargs.pop(u"user_ids"))
        usernames = to_list(kwargs.pop(u"usernames"))
        user_ip_addresses = to_list(kwargs.pop(u"user_ip_addresses"))
        affected_user_ids = to_list(kwargs.pop(u"affected_user_ids"))
        affected_usernames = to_list(kwargs.pop(u"affected_usernames"))

        date_range = {}
        begin_time = kwargs.pop(u"begin_time")
        end_time = kwargs.pop(u"end_time")
        if begin_time:
            date_range["startTime"] = convert_timestamp_to_str(begin_time)
        if end_time:
            date_range["endTime"] = convert_timestamp_to_str(end_time)

        uri = u"/rpc/search/search-audit-log"
        page_size = page_size or settings.items_per_page
        params = dict(
            page=page_num - 1,
            pageSize=page_size,
            dateRange=date_range,
            eventTypes=event_types,
            actorIds=user_ids,
            actorNames=usernames,
            actorIpAddresses=user_ip_addresses,
            affectedUserIds=affected_user_ids,
            affectedUserNames=affected_usernames,
            **kwargs
        )
        return self._connection.post(uri, json=params)

    def get_all(
        self,
        begin_time=None,
        end_time=None,
        event_types=None,
        user_ids=None,
        usernames=None,
        user_ip_addresses=None,
        affected_user_ids=None,
        affected_usernames=None,
        **kwargs
    ):

        return get_all_pages(
            self.get_page,
            "events",
            begin_time=begin_time,
            end_time=end_time,
            event_types=event_types,
            user_ids=user_ids,
            usernames=usernames,
            user_ip_addresses=user_ip_addresses,
            affected_user_ids=affected_user_ids,
            affected_usernames=affected_usernames,
            **kwargs
        )
