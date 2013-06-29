from django.db.models import Model, Manager, ForeignKey, IntegerField, FloatField, CharField, TextField, ManyToManyField, OneToOneField, DateTimeField
from django.conf import settings
from common_models import StrMixin, filtered_manager, BaseStaticItem, BaseMapItem, Unit


class MarketGroup(Model, StrMixin):
    marketgroup_id = IntegerField(primary_key=True, db_column='marketGroupID')
    parent = ForeignKey('self', null=True, db_column='parentGroupID', blank=True, related_name='children')
    name = CharField(max_length=100, db_column='marketGroupName', blank=True)
    description = TextField(max_length=3000, blank=True)
    icon_id = IntegerField(null=True, db_column='iconID', blank=True)
    has_types = IntegerField(null=True, db_column='hasTypes', blank=True)

    class Meta:
    	app_label = 'eve_sde'
        db_table = 'invMarketGroups'


class ItemCategory(Model, StrMixin):
    category_id = IntegerField(primary_key=True, db_column='categoryID')
    name = CharField(max_length=100, db_column='categoryName', blank=True)
    description = TextField(max_length=3000, blank=True)
    icon_id = IntegerField(null=True, db_column='iconID', blank=True)
    is_published = IntegerField(null=True, blank=True, db_column='published')

    objects = filtered_manager()
    published = filtered_manager(is_published=1)
    unpublished = filtered_manager(is_published=0)

    class Meta:
        db_table = 'invCategories'
        app_label = 'eve_sde'


class ItemGroup(Model, StrMixin):
    group_id = IntegerField(primary_key=True, db_column='groupID')
    category = ForeignKey('ItemCategory', null=True, db_column='categoryID', blank=True, related_name='groups')
    name = CharField(max_length=100, db_column='groupName', blank=True)
    description = TextField(max_length=3000, blank=True)
    icon_id = IntegerField(null=True, db_column='iconID', blank=True)
    use_base_price = IntegerField(null=True, db_column='useBasePrice', blank=True)
    allow_manufacture = IntegerField(null=True, db_column='allowManufacture', blank=True)
    allow_recycler = IntegerField(null=True, db_column='allowRecycler', blank=True)
    anchored = IntegerField(null=True, blank=True)
    anchorable = IntegerField(null=True, blank=True)
    fittable_non_singleton = IntegerField(null=True, db_column='fittableNonSingleton', blank=True)
    is_published = IntegerField(null=True, blank=True, db_column='published')

    objects = filtered_manager()
    published = filtered_manager(is_published=1)
    unpublished = filtered_manager(is_published=0)

    class Meta:
        db_table = 'invGroups'
        app_label = 'eve_sde'


class Item(Model, StrMixin):
    item_id = IntegerField(primary_key=True, db_column='typeID')
    group = ForeignKey('ItemGroup', null=True, db_column='groupID', blank=True, related_name='items')
    name = CharField(max_length=100, db_column='typeName', blank=True)
    description = TextField(max_length=3000, blank=True)
    mass = FloatField(blank=True) # #This field type is a guess.
    volume = FloatField(blank=True) # #This field type is a guess.
    capacity = FloatField(blank=True) # #This field type is a guess.
    portion_size = IntegerField(null=True, db_column='portionSize', blank=True)
    race = ForeignKey('Race', null=True, db_column='raceID', blank=True, related_name='racial_items')
    base_price = FloatField(db_column='basePrice', blank=True) #This field type is a guess.
    is_published = IntegerField(null=True, blank=True, db_column='published')
    marketgroup = ForeignKey('MarketGroup', null=True, db_column='marketGroupID', blank=True, related_name='items')
    chance_of_duplicating = FloatField(db_column='chanceOfDuplicating', blank=True) #This field type is a guess.

    objects = filtered_manager()
    published = filtered_manager(is_published=1)
    unpublished = filtered_manager(is_published=0)

    class Meta:
        app_label = 'eve_sde'
        db_table = 'invTypes'


class MetaGroup(Model, StrMixin):
    metagroup_id = IntegerField(primary_key=True, db_column='metaGroupID')
    name = CharField(max_length=100, db_column='metaGroupName', blank=True)
    description = TextField(max_length=1000, blank=True)
    icon_id = IntegerField(null=True, db_column='iconID', blank=True)

    class Meta:
        db_table = 'invMetaGroups'


class MetaType(Model, StrMixin):
    item = OneToOneField('Item', primary_key=True, db_column='typeID', related_name='metatype')
    base_item = ForeignKey('Item', null=True, db_column='parentTypeID', blank=True, related_name='metatypes')
    metagroup = ForeignKey('MetaGroup', null=True, db_column='metaGroupID', blank=True)

    class Meta:
        db_table = 'invMetaTypes'

    def _display_str(self):
        return "%s (%s)" % (self.item.name, self.metagroup.name)


class Contraband(Model, StrMixin):
    faction = ForeignKey('Faction', primary_key=True, db_column='factionID', related_name='contraband')
    item = ForeignKey('Item', db_column='typeID')
    standing_loss = FloatField(db_column='standingLoss', blank=True)
    confiscate_min_sec = FloatField(db_column='confiscateMinSec', blank=True)
    fine_by_value = FloatField(db_column='fineByValue', blank=True)
    attack_min_sec = FloatField(db_column='attackMinSec', blank=True)

    class Meta:
        app_label = 'eve_sde'
        db_table = 'invContrabandTypes'


class ItemFlag(Model, StrMixin):
    flag_id = IntegerField(primary_key=True, db_column='flagID')
    name = CharField(max_length=200, db_column='flagName', blank=True)
    flag_text = CharField(max_length=100, db_column='flagText', blank=True)
    order_id = IntegerField(null=True, db_column='orderID', blank=True)

    class Meta:
        db_table = 'invFlags'
        app_label = 'eve_sde'


class AttributeCategory(Model, StrMixin):
    category_id = IntegerField(primary_key=True, db_column='categoryID')
    name = CharField(max_length=50, db_column='categoryName', blank=True)
    description = TextField(max_length=200, db_column='categoryDescription', blank=True)

    class Meta:
    	app_label = 'eve_sde'
        db_table = 'dgmAttributeCategories'


class AttributeType(Model, StrMixin):
    attribute_id = IntegerField(primary_key=True, db_column='attributeID')
    name = CharField(max_length=100, db_column='attributeName', blank=True)
    description = TextField(max_length=1000, blank=True)
    icon_id = IntegerField(null=True, db_column='iconID', blank=True)
    default_value = FloatField(db_column='defaultValue', blank=True)
    published = IntegerField(null=True, blank=True)
    name = CharField(max_length=100, db_column='displayName', blank=True)
    unit = ForeignKey('Unit', null=True, db_column='unitID', blank=True, related_name='attribute_types')
    stackable = IntegerField(null=True, blank=True)
    high_is_good = IntegerField(null=True, db_column='highIsGood', blank=True)
    category_id = IntegerField(null=True, db_column='categoryID', blank=True)

    class Meta:
    	app_label = 'eve_sde'
        db_table = 'dgmAttributeTypes'


class Effect(Model, StrMixin):
    effect_id = IntegerField(primary_key=True, db_column='effectID')
    name = CharField(max_length=400, db_column='effectName', blank=True)
    effect_category = IntegerField(null=True, db_column='effectCategory', blank=True)
    pre_expression = IntegerField(null=True, db_column='preExpression', blank=True)
    post_expression = IntegerField(null=True, db_column='postExpression', blank=True)
    description = TextField(max_length=1000, blank=True)
    guid = CharField(max_length=60, blank=True)
    icon_id = IntegerField(null=True, db_column='iconID', blank=True)
    is_offensive = IntegerField(null=True, db_column='isOffensive', blank=True)
    is_assistance = IntegerField(null=True, db_column='isAssistance', blank=True)
    duration = ForeignKey('AttributeType', null=True, db_column='durationAttributeID', blank=True, related_name='effect_durations')
    tracking_speed = ForeignKey('AttributeType', null=True, db_column='trackingSpeedAttributeID', blank=True, related_name='tracking_speed_effects')
    discharge = ForeignKey('AttributeType', null=True, db_column='dischargeAttributeID', blank=True, related_name='discharge_effects')
    range = ForeignKey('AttributeType', null=True, db_column='rangeAttributeID', blank=True, related_name='range_effects') #  bad name for a python variable
    falloff = ForeignKey('AttributeType', null=True, db_column='falloffAttributeID', blank=True)
    disallow_autorepeat = IntegerField(null=True, db_column='disallowAutoRepeat', blank=True)
    published = IntegerField(null=True, blank=True)
    display_name = CharField(max_length=100, db_column='displayName', blank=True)
    is_warp_safe = IntegerField(null=True, db_column='isWarpSafe', blank=True)
    range_chance = IntegerField(null=True, db_column='rangeChance', blank=True)
    electronic_chance = IntegerField(null=True, db_column='electronicChance', blank=True)
    propulsion_chance = IntegerField(null=True, db_column='propulsionChance', blank=True)
    distribution = IntegerField(null=True, blank=True)
    sfx_name = CharField(max_length=20, db_column='sfxName', blank=True)
    npc_usage_chance = ForeignKey('AttributeType', null=True, db_column='npcUsageChanceAttributeID', blank=True, related_name='npc_usage_chance_effects')
    npc_activation_chance = ForeignKey('AttributeType', null=True, db_column='npcActivationChanceAttributeID', blank=True, related_name="npc_activation_chance_effects")
    fitting_usage_chance = ForeignKey('AttributeType', null=True, db_column='fittingUsageChanceAttributeID', blank=True, related_name='fitting_usage_chance_effects')

    class Meta:
    	app_label = 'eve_sde'
        db_table = 'dgmEffects'


class ItemAttribute(Model, StrMixin):
    item = ForeignKey('Item', primary_key=True, db_column='typeID', related_name='attributes')
    attribute = ForeignKey('AttributeType', primary_key=True, db_column='attributeID', related_name='item_attributes')
    value_int = IntegerField(null=True, db_column='valueInt', blank=True)
    value_float = FloatField(db_column='valueFloat', blank=True)

    class Meta:
    	app_label = 'eve_sde'
        db_table = 'dgmTypeAttributes'


class ItemEffect(Model, StrMixin):
    item = ForeignKey('Item', primary_key=True, db_column='typeID', related_name='effects')
    effect = ForeignKey('Effect', primary_key=True, db_column='effectID', related_name='items')
    is_default = IntegerField(null=True, db_column='isDefault', blank=True)

    class Meta:
    	app_label = 'eve_sde'
        db_table = 'dgmTypeEffects'
        
