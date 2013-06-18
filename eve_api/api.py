import logging
import requests
from lxml import etree as xml
import datetime

logger = logging.getLogger(__name__)


class EveApi(object):

    API_URL_FORMAT = "https://api.eveonline.com/%(group)s/%(name)s%(suffix)s"

    def api_url(self, group=None, name=None, **kwargs):

        suffix = kwargs.get("suffix", ".xml.aspx")

        return self.API_URL_FORMAT % {"group": group, "name": name, "suffix": suffix}

    def api_call(self, group=None, name=None, **kwargs):

        url = self.api_url(group=group, name=name, **kwargs)

        request = requests.get(url, params=kwargs)

        logger.debug("Requests (GET) %s", request.url)

        xml_text = str(request.text)

        xml_data = xml.fromstring(xml_text)

        data_dict = etree_to_dict(xml_data)

        data_dict = clean_response(data_dict)

        return data_dict


class PublicApi(EveApi):

    def __init__(self, **kwargs):
        self.extra = kwargs

    def alliance_list(self, **kwargs):
        return self.api_call(group="eve", name="AllianceList",)

    def certificate_tree(self, **kwargs):
        return self.api_call(group="eve", name="CertificateTree", **kwargs)

    def conquerable_station_list(self, **kwargs):
        return self.api_call(group="eve", name="ConquerableStationList",)

    def character_name(self, *character_ids, **kwargs):
        ids = ",".join([str(character_id) for character_id in character_ids])
        return self.api_call(group="eve", name="CharacterName", ids=ids)

    def character_ids(self, *character_names, **kwargs):
        names = ",".join(character_names)
        return self.api_call(group="eve", name="CharacterID", names=names, **kwargs)

    def character_info(self, character_id=None, **kwargs):

        if 'name' in kwargs:
            character_id = self.character_ids(kwargs.pop('name'))['characters'][0]['characterID']
        return self.api_call(group="eve", name="CharacterInfo", characterID=character_id, **kwargs)

    def error_list(self, **kwargs):
        return self.api_call(group="eve", name="ErrorList", **kwargs)

    def fac_war_stats(self, **kwargs):
        return self.api_call(group="eve", name="FacWarStats",)

    def fac_war_top_stats(self, **kwargs):
        return self.api_call(group="eve", name="FacWarTopStats",)

    def fac_war_systems(self, **kwargs):
        return self.api_call(group="map", name="FacWarSystems",)

    def jumps(self, as_dict=True, **kwargs):
        result = self.api_call(group="map", name="Jumps",)
        if as_dict:
            result = dict((data['solarSystemID'], data) for data in result['children'][0]['rowset'])
            for r in result.values():
                if 'row' in r:
                    del r['row']
        return result

    def kills(self, as_dict=True, **kwargs):
        result = self.api_call(group="map", name="Kills",)
        if as_dict:
            result = dict((data['solarSystemID'], data) for data in result['children'][0]['rowset'])
            for r in result.values():
                if 'row' in r:
                    del r['row']
        return result

    def ref_types(self, **kwargs):
        return self.api_call(group="eve", name="RefTypes", **kwargs)

    def skill_tree(self, **kwargs):
        return self.api_call(group="eve", name="SkillTree")

    def sovereignty(self, **kwargs):
        return self.api_call(group="map", name="Sovereignty",)

    def type_names(self, *item_ids, **kwargs):
        ids = ",".join([str(item_id) for item_id in item_ids])
        return self.api_call(group="eve", name="TypeName", ids=ids)


class PrivateApi(EveApi):

    keyID = ""
    vCode = ""
    group = ""

    def __init__(self, **kwargs):

        for k, v in kwargs.items():
            setattr(self, k, v)

    def api_call(self, name="", auth=True, **kwargs):

        args = {}

        group = kwargs.pop('group', self.group)

        args.update(kwargs)

        if auth:
            args['keyID'] = self.keyID
            args['vCode'] = self.vCode

        return super(PrivateApi, self).api_call(group=group, name=name, **args)

    def key_info(self, **kwargs):
        return self.api_call(group="account", name="APIKeyInfo", **kwargs)

    def account_status(self, *args, **kwargs):
        pass

    def account_balance(self, accountKey=1000, **kwargs):
        return self.api_call('AccountBalance', accountKey=accountKey, **kwargs)

    def asset_list(self, **kwargs):
        return self.api_call(name='AssetList', **kwargs)

    def contact_list(self, **kwargs):
        return self.api_call(name='ContactList', **kwargs)

    def contracts(self, **kwargs):
        return self.api_call(name='Contracts', **kwargs)

    def fac_war_stats(self, **kwargs):
        return self.api_call('FacWarStats', **kwargs)

    def industry_jobs(self, **kwargs):
        return self.api_call('IndustryJobs', **kwargs)

    def kill_log(self, **kwargs):
        return self.api_call('KillLog', **kwargs)

    def locations(self, **kwargs):
        return self.api_call('Locations', **kwargs)

    def market_orders(self, **kwargs):
        return self.api_call('MarketOrders', **kwargs)

    def medals(self, **kwargs):
        return self.api_call('Medals', **kwargs)

    def standings(self, **kwargs):
        return self.api_call('Standings', **kwargs)

    def wallet_journal(self, accountKey=1000, **kwargs):
        return self.api_call('WalletJournal', accountKey=accountKey, **kwargs)

    def wallet_transactions(self, accountKey=1000, **kwargs):
        return self.api_call('WalletTransactions', accountKey=accountKey, **kwargs)


class CharacterApi(PrivateApi):

    characterID = None
    group = "char"

    def api_call(self, name="", auth=True, **kwargs):

        characterID = kwargs.pop("characterID", self.characterID)

        return super(CharacterApi, self).api_call(name=name, auth=auth, characterID=characterID, **kwargs)

    def account_status(self, **kwargs):
        return self.api_call(group='account', name='AccountStatus', **kwargs)

    def calendar_event_attendees(self, **kwargs):
        return self.api_call('CalendarEventAttendees', **kwargs)

    def character_info(self, **kwargs):
        return self.api_call(group='eve', name='CharacterInfo', **kwargs)

    def character_sheet(self, **kwargs):
        return self.api_call('CharacterSheet', **kwargs)

    def contact_notifications(self, **kwargs):
        return self.api_call('ContactNotifications', **kwargs)

    def mail_bodies(self, **kwargs):
        return self.api_call('MailBodies', **kwargs)

    def mail_messages(self, **kwargs):
        return self.api_call('MailMessages', **kwargs)

    def mailing_lists(self, **kwargs):
        return self.api_call('MailingLists', **kwargs)

    def notification_texts(self, **kwargs):
        return self.api_call('NotificationTexts', **kwargs)

    def notifications(self, **kwargs):
        return self.api_call('Notifications', **kwargs)

    def research(self, **kwargs):
        return self.api_call('Research', **kwargs)

    def skill_in_training(self, **kwargs):
        return self.api_call('SkillInTraining', **kwargs)

    def skill_queue(self, **kwargs):
        return self.api_call('SkillQueue', **kwargs)

    def upcoming_calendar_events(self, **kwargs):
        return self.api_call('UpcomingCalendarEvents', **kwargs)


class CorporationApi(PrivateApi):

    group = "corp"

    def container_log(self, **kwargs):
            return self.api_call('ContainerLog', **kwargs)

    def corporation_sheet(self, **kwargs):
            return self.api_call('CorporationSheet', **kwargs)

    def member_medals(self, **kwargs):
            return self.api_call('MemberMedals', **kwargs)

    def member_security(self, **kwargs):
            return self.api_call('MemberSecurity', **kwargs)

    def member_security_log(self, **kwargs):
            return self.api_call('MemberSecurityLog', **kwargs)

    def member_tracking_extended(self, **kwargs):
            return self.api_call('MemberTrackingExtended', **kwargs)

    def member_tracking_limited(self, **kwargs):
            return self.api_call('MemberTrackingLimited', **kwargs)

    def outpost_list(self, **kwargs):
            return self.api_call('OutpostList', **kwargs)

    def outpost_service_detail(self, **kwargs):
            return self.api_call('OutpostServiceDetail', **kwargs)

    def shareholders(self, **kwargs):
            return self.api_call('Shareholders', **kwargs)

    def starbase_detail(self, **kwargs):
            return self.api_call('StarbaseDetail', **kwargs)

    def starbase_list(self, **kwargs):
            return self.api_call('StarbaseList', **kwargs)

    def titles(self, **kwargs):
            return self.api_call('Titles', **kwargs)


bool_types = set(["bid"])
int_types = set(["volRemaining", "volEntered", "accountKey", "accessMask", "memberCount", "memberLimit" "accountKey", "accountID", "orderState", "characterID", "corporationID"])
date_types = set(["date", "transactionDateTime", "cachedUntil", "currentTime", "createDate", "paidUntil", "dataTime", "DoB", "startDate", "corporationDate"])


def convert_type(obj, key=None):
    # There is likely a better way to do this

    if key in bool_types:
        #looks like php
        if obj == '1' or obj == True or obj == "true" or obj == 1:
            return True
        else:
            return False
    if key in int_types or (key and any((key.endswith("ID"), key.endswith("ID1"), key.endswith("ID2"))) and obj):
        return int(obj)
    elif key in date_types:
        try:
            return datetime.datetime.strptime(obj, "%Y-%m-%d %H:%M:%S")
        except:
            pass
    try:
        val = float(obj)
    except:
        val = obj

    return val


def etree_to_dict(t, p=None):
    # There is a better way to do this

    d = {}
    d[t.tag] = map(lambda x: etree_to_dict(x, d), t.iterchildren())

    if not d[t.tag] and t.text:
        d[t.tag] = convert_type(t.text)

    d.update(dict((k, convert_type(v, key=k)) for k, v in t.attrib.iteritems() if k != "row"))
    if t.getchildren() and t.get('name') != None:
        if p:
            p[t.get('name')] = [etree_to_dict(child, p) for child in t.getchildren()]
        else:
            d[t.get('name')] = [etree_to_dict(child, d) for child in t.getchildren()]

    elif t.getchildren():
        d['children'] = [etree_to_dict(child, d) for child in t.getchildren()]

    convert_types(d)

    return d


def convert_types(parent, key=None):
    # There is a better way to do this

    if isinstance(parent, dict):
        for key, value in parent.items():
            parent[key] = convert_types(value, key=key)
    elif isinstance(parent, list):
        parent = [convert_types(i) for i in parent]
    else:
        parent = convert_type(parent, key=key)

    return parent


def clean_response(d):
    # There is a better way to do this

    result = {}

    for data in d['eveapi']:

        for key, value in data.items():
            if key == 'result':
                for result_row in value:
                    if 'rowset' in result_row:
                        for item in result_row['rowset']:
                            del item['row']
                        result[result_row['name']] = result_row['rowset']
                    else:
                        result.update(result_row)

            else:
                result[key] = value
    for date_type in date_types:
        if date_type in result:
            result[date_type] = convert_type(result[date_type], key=date_type)

    return result
