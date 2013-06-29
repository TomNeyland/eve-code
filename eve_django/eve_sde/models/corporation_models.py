from django.db.models import Model, Manager, ForeignKey, IntegerField, FloatField, CharField, TextField, ManyToManyField, OneToOneField, DateTimeField
from django.conf import settings
from common_models import StrMixin, filtered_manager, BaseStaticItem, BaseMapItem


class AgentType(Model, StrMixin):
    agent_type_id = IntegerField(primary_key=True, db_column='agentTypeID')
    name = CharField(max_length=50, db_column='agentType', blank=True)

    class Meta:
        app_label = 'eve_sde'
        db_table = 'agtAgentTypes'


class Agent(BaseStaticItem):
    static_item = OneToOneField('BaseStaticItem', parent_link=True, to_field='static_id', db_column='agentID')

    agent_id = IntegerField(primary_key=True, db_column='agentID')
    division = ForeignKey('Division', null=True, db_column='divisionID', blank=True, related_name='agents')
    corporation = ForeignKey('Corporation', null=True, db_column='corporationID', blank=True, related_name='agents')
    location = ForeignKey('BaseMapItem', db_column='locationID', blank=True, related_name='agents')
    level = IntegerField(null=True, blank=True)
    quality = IntegerField(null=True, blank=True)
    agent_type = ForeignKey('AgentType', null=True, db_column='agentTypeID', blank=True)
    is_locator = IntegerField(null=True, db_column='isLocator', blank=True)
    research_skills = ManyToManyField('Item', through='AgentResearchSkill', related_name='research_agents')

    class Meta:
        app_label = 'eve_sde'
        db_table = 'agtAgents'


class AgentResearchSkill(Model, StrMixin):
    agent = ForeignKey('Agent', primary_key=True, db_column='agentID', related_name='None')
    skill = ForeignKey('Item', db_column='typeID', related_name='None')

    class Meta:
        app_label = 'eve_sde'
        db_table = 'agtResearchAgents'


class ResearchField(Model, StrMixin):
    skill = ForeignKey('Item', primary_key=True, db_column='skillID', related_name='+')
    corporation = ForeignKey('Corporation', primary_key=True, db_column='corporationID', related_name='+')

    class Meta:
        app_label = 'eve_sde'
        db_table = 'crpNPCCorporationResearchFields'


class Faction(BaseStaticItem):
    static_item = OneToOneField('BaseStaticItem', parent_link=True, to_field='static_id', db_column='factionID')

    faction_id = IntegerField(primary_key=True, db_column='factionID')
    name = CharField(max_length=100, db_column='factionName', blank=True)
    description = TextField(max_length=1000, blank=True)
    race_ids = IntegerField(null=True, db_column='raceIDs', blank=True)
    solarsystem_id = IntegerField(null=True, db_column='solarSystemID', blank=True)
    corporation = ForeignKey('Corporation', null=True, db_column='corporationID', blank=True, related_name='factions')
    size_factor = FloatField(db_column='sizeFactor', blank=True)  # This field type is a guess.
    station_count = IntegerField(null=True, db_column='stationCount', blank=True)
    station_system_count = IntegerField(null=True, db_column='stationSystemCount', blank=True)
    militia_corporation = ForeignKey('Corporation', null=True, db_column='militiaCorporationID', blank=True, related_name='militia_corporations')
    icon_id = IntegerField(null=True, db_column='iconID', blank=True)

    class Meta:
        app_label = 'eve_sde'
        db_table = 'chrFactions'


class Corporation(BaseStaticItem):
    static_item = OneToOneField('BaseStaticItem', parent_link=True, to_field='static_id', db_column='corporationID')

    corporation_id = IntegerField(primary_key=True, db_column='corporationID')
    size = CharField(max_length=1, blank=True)
    extent = CharField(max_length=1, blank=True)
    system = ForeignKey('System', null=True, db_column='solarSystemID', blank=True, related_name='corporations')
    investor1 = ForeignKey('self', null=True, db_column='investorID1', blank=True, related_name='investments1')
    investor1_shares = IntegerField(null=True, db_column='investorShares1', blank=True)
    investor2 = ForeignKey('self', null=True, db_column='investorID2', blank=True, related_name='investments2')
    investor2_shares = IntegerField(null=True, db_column='investorShares2', blank=True)
    investor3 = ForeignKey('self', null=True, db_column='investorID3', blank=True, related_name='investments3')
    investor3_shares = IntegerField(null=True, db_column='investorShares3', blank=True)
    investor4 = ForeignKey('self', null=True, db_column='investorID4', blank=True, related_name='investments4')
    investor4_shares = IntegerField(null=True, db_column='investorShares4', blank=True)
    friend = ForeignKey('self', null=True, db_column='friendID', blank=True, related_name='friends') #  Should it be O2O?
    enemy = ForeignKey('self', null=True, db_column='enemyID', blank=True, related_name='enemies') #  Should it be O2O?
    public_shares = IntegerField(null=True, db_column='publicShares', blank=True)
    initial_price = IntegerField(null=True, db_column='initialPrice', blank=True)
    min_security = FloatField(db_column='minSecurity', blank=True) #This field type is a guess.
    scattered = IntegerField(null=True, blank=True)
    fringe = IntegerField(null=True, blank=True,)
    corridor = IntegerField(null=True, blank=True)
    hub = IntegerField(null=True, blank=True)
    border = IntegerField(null=True, blank=True)
    faction = ForeignKey('Faction', null=True, db_column='factionID', blank=True, related_name='corporations')
    size_factor = FloatField(db_column='sizeFactor', blank=True) #This field type is a guess.
    station_count = IntegerField(null=True, db_column='stationCount', blank=True)
    station_system_count = IntegerField(null=True, db_column='stationSystemCount', blank=True)
    description = TextField(max_length=4000, blank=True)
    icon_id = IntegerField(null=True, db_column='iconID', blank=True)
    divisions = ManyToManyField('Division', through='CorporationDivision')
    trades = ManyToManyField('Item', through='CorporationTrade')

    class Meta:
        app_label = 'eve_sde'
        db_table = 'crpNPCCorporations'


class Division(Model, StrMixin):
    division_id = IntegerField(primary_key=True, db_column='divisionID') #O2O may be the wrong type
    name = CharField(max_length=100, db_column='divisionName', blank=True)
    description = TextField(max_length=1000, blank=True)
    leader_type = CharField(max_length=100, db_column='leaderType', blank=True)

    class Meta:
        app_label = 'eve_sde'
        db_table = 'crpNPCDivisions'


class CorporationActivity(Model, StrMixin):
    activity_id = IntegerField(primary_key=True, db_column='activityID')
    name = CharField(max_length=100, db_column='activityName', blank=True)
    description = TextField(max_length=1000, blank=True)

    class Meta:
        app_label = 'eve_sde'
        db_table = 'crpActivities'


class CorporationDivision(Model, StrMixin):
    corporation = ForeignKey('Corporation', primary_key=True, db_column='corporationID',)
    division = ForeignKey('Division', primary_key=True, db_column='divisionID',)
    size = IntegerField(null=True, blank=True)

    class Meta:
        app_label = 'eve_sde'
        db_table = 'crpNPCCorporationDivisions'


class CorporationTrade(Model, StrMixin):
    corporation = ForeignKey('Corporation',primary_key=True, db_column='corporationID', related_name='+')
    item = ForeignKey('Item', primary_key=True, db_column='typeID', related_name='+')

    class Meta:
        app_label = 'eve_sde'
        db_table = 'crpNPCCorporationTrades'
