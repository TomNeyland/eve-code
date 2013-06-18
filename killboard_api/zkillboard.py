import json
import requests
from copy import copy
from collections import defaultdict
import itertools
import zlib
import logging

logger = logging.getLogger(__name__)


class Indexable(object):
    def __init__(self, it):
        self.it = it
        self.already_computed = []

    def __iter__(self):
        for elt in self.it:
            self.already_computed.append(elt)
            yield elt

    def __getitem__(self, index):
        try:
            max_idx = index.stop
        except AttributeError:
            max_idx = index
        n = max_idx - len(self.already_computed) + 1
        if n > 0:
            self.already_computed.extend(itertools.islice(self.it, n))
        return self.already_computed[index]


class KillboardApi(object):

    API_URL_FORMAT = "https://zkillboard.com/api/%(less)s%(fetch_type)s%(fetch_modifier)s%(time)s%(limit)s%(order)s"

    fetch_types = set(('kills', 'losses', 'w-space', 'solo'))
    fetch_modifiers = set(('characterID', 'corporationID', 'allianceID', 'factionID', 'shipTypeID', "shipID", 'groupID', 'solarSystemID', 'regionID'))
    order_modifiers = set(("orderDirection"))
    less_modifiers = set(("no-items", "no-attackers", "api-only"))
    time_modifiers = set(("startTime", "endTime", "year", "month", "week", "pastSeconds"))
    limit_modifiers = set(("limit", "beforeKillID", "afterKillID", "page"))

    request_headers = {
        "Accept-Encoding": "gzip",
        "User-Agent": "Python Zkillboard Api Wrapper (Under Development)"
    }

    def api_url(self, fetch_type=None, less=None, **kwargs):

        params = {
            "fetch_type": "",
            "fetch_modifier": "",
            "less": "",
            "time": "",
            "limit": "",
            "order": "",
        }

        if isinstance(fetch_type, (set, list, tuple)):
            fetch_type = "/".join((f for f in fetch_type if f in self.fetch_types))
            if fetch_type:
                params['fetch_type'] = "%s/" % (fetch_type,)
        elif fetch_type in self.fetch_types:
            params['fetch_type'] = "%s/" % (fetch_type,)

        if isinstance(less, (set, list, tuple)):
            less = "/".join((l for l in less if l in self.less_modifiers))
            if less:
                params['less'] = "%s/" % (less,)
        elif less in self.less_modifiers:
            params['less'] = "%s/" % (less,)

        for key, value in kwargs.items():

            if key in self.fetch_modifiers:
                if isinstance(value, (set, list, tuple)):
                    value = ",".join((str(v) for v in value))
                params['fetch_modifier'] = params.get("fetch_modifier", "") + "%s/%s/" % (key, value)

            elif key in self.order_modifiers:
                params['order'] = "orderDirection/%s/" % (value)

            elif key in self.time_modifiers:
                if isinstance(value, (set, list, tuple)):
                    value = ",".join((str(v) for v in value))
                params['time'] = params.get("time", "") + "%s/%s/" % (key, value)

            elif key in self.limit_modifiers:
                if isinstance(value, (set, list, tuple)):
                    value = ",".join((str(v) for v in value))
                params['limit'] = params.get("limit", "") + "%s/%s/" % (key, value)

        return self.API_URL_FORMAT % params

    def api_call(self, fetch="", headers=None, **kwargs):

        headers = headers or self.request_headers

        url = self.api_url(fetch=fetch, **kwargs)

        request = requests.get(url, headers=headers)

        logger.debug("Requests (GET) %s", request.url)

        json_text = str(request.text)

        #data = json.loads(json_text)
        try:
            data = request.json()
        except Exception as e:
            print e
            return None

        return data


def chained(func):

    def func_wrapper(self, *args, **kwargs):
        clone = self._clone()
        return func(clone, *args, **kwargs)
    func_wrapper.func_name = func.func_name
    return func_wrapper


def chained_property(func):
    chained_func = chained(func)
    chained_func_property = property(chained_func)
    return chained_func_property


class KillboardQuery(object):
    """This is buggy..."""

    def __init__(self, api=None, params=None, max_page=None):
        self.api = api or KillboardApi()
        self.params = defaultdict(set)
        self.result = None
        self.max_page = max_page
        self._iter_cache = []

        if params:
            self.params.update(params)

    def __iter__(self):

        page_num = self.params['page']
        if not page_num:
            #iterate to max_pages
            self.params['page'] = page_num = 1
            had_page = False
        else:
            had_page = page_num

        page_data = self._query_api(force=True)
        while page_data:

            for item in page_data:
                self._iter_cache.append(item)
                yield item

            page_num = page_num + 1
            self.params['page'] = page_num

            if self.max_page != None and page_num > self.max_page:
                break
            else:
                page_data = self._query_api(force=True, cache=False)

            if had_page:
                self.params['page'] = had_page

    def __getitem__(self, index):
            print index
            try:
                max_idx = index.stop
            except AttributeError:
                max_idx = index
            n = max_idx - len(self._iter_cache) + 1
            if n > 0:
                self._iter_cache.extend(itertools.islice(self, n))
            return self._iter_cache[index]

    def all(self):
        #fix max-page's interaction with this
        if getattr(self, "_all_cache", None) == None:
            print "caching all"
            self._all_cache = list(self)

        return self._all_cache

    def _clone(self):
        clone = copy(self)

        clone.params = copy(self.params)
        clone._result = None
        clone._all_cache = None
        clone._iter_cache = []

        return clone

    def _query_api(self, force=False, cache=True):
        if force or getattr(self, '_result', None) == None:
            result = self.api.api_call(**self.params)
            if cache:
                self._result = result
        else:
            result = self._result

        return result

    @chained
    def w_space(self):
        self.params['fetch_type'].add('w-space')
        return self

    @chained
    def solo(self):
        self.params['fetch_type'].add('solo')
        return self

    @chained
    def losses(self):
        self.params['fetch_type'].add('losses')
        return self

    @chained
    def kills(self):
        self.params['fetch_type'].add('kills')
        return self

    @chained
    def api_only(self):
        self.params['less'].add('api-only')
        return self

    @chained
    def no_attackers(self):
        self.params['less'].add('no-attackers')
        return self

    @chained
    def no_items(self):
        self.params['less'].add('no-items')
        return self

    @chained
    def page(self, num, max_page=None):
        self.params['page'] = num
        self.max_page = max_page
        return self

    @chained
    def character_ids(self, *char_ids):
        self.params['characterID'].update(char_ids)
        return self

    @chained
    def corporation_ids(self, *corp_ids):
        self.params['corporationID'].update(corp_ids)
        return self

    @chained
    def alliance_ids(self, *ally_ids):
        self.params['allianceID'].update(ally_ids)
        return self

    @chained
    def faction_ids(self, *fac_ids):
        self.params['factionID'].update(fac_ids)
        return self

    @chained
    def ship_type_ids(self, *ship_ids):
        self.params['shipTypeID'].update(ship_ids)
        return self

    @chained
    def group_ids(self, *group_ids):
        self.params['groupID'].update(group_ids)
        return self

    @chained
    def solar_system_ids(self, *system_ids):
        self.params['solarSystemID'].update(system_ids)
        return self

    @chained
    def region_ids(self, *regions):
        self.params['regionID'].update(regions)
        return self
