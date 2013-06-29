from django.db.models import Model, Manager, ForeignKey, IntegerField, FloatField, CharField, TextField, ManyToManyField, OneToOneField, DateTimeField
from django.conf import settings
from common_models import SKILL_GROUP_IDS, StrMixin, filtered_manager, BaseStaticItem, BaseMapItem, Unit
from item_models import Item
from station_models import *

skill_filter = {"material__group__pk__in": SKILL_GROUP_IDS}


class Blueprint(Model, StrMixin):
    blueprint_id = IntegerField(primary_key=True, db_column='blueprintTypeID')
    #parentblueprinttypeid = IntegerField(null=True, db_column='parentBlueprintTypeID', blank=True)
    item = OneToOneField('Item', null=True, db_column='productTypeID', related_name='blueprint')
    production_time = IntegerField(null=True, db_column='productionTime', blank=True)
    tech_level = IntegerField(null=True, db_column='techLevel', blank=True)
    research_productivity_time = IntegerField(null=True, db_column='researchProductivityTime', blank=True)
    research_material_time = IntegerField(null=True, db_column='researchMaterialTime', blank=True)
    research_copy_time = IntegerField(null=True, db_column='researchCopyTime', blank=True)
    research_tech_time = IntegerField(null=True, db_column='researchTechTime', blank=True)
    productivity_modifier = IntegerField(null=True, db_column='productivityModifier', blank=True)
    material_modifier = IntegerField(null=True, db_column='materialModifier', blank=True)
    waste_factor = IntegerField(null=True, db_column='wasteFactor', blank=True)
    max_production_limit = IntegerField(null=True, db_column='maxProductionLimit', blank=True)

    class Meta:
        app_label = 'eve_sde'
        db_table = 'invBlueprintTypes'


####
# Standard production material requirements, based on an item's item_id
####


class MaterialRequirement(Model, StrMixin):

    item = ForeignKey('Item', primary_key=True, db_column='typeID', related_name='required_materials')
    material = ForeignKey('Item', primary_key=True, db_column='materialTypeID', related_name='used_in')
    quantity = IntegerField()

    def me_waste(self, me=0, waste_factor=10):

        waste = 0

        if me >= 0:
            waste = round(self.quantity * (waste_factor / 100.0) * (1.0 / (me + 1.0)))
        else:
            waste = round(self.quantity * (waste_factor / 100.0) * (1.0 - me))

        return waste

    def pe_waste(self, skill=5):

        waste = round(((25.0 - (5.0 * skill)) * self.quantity) / 100.0)

        return waste

    def real_quantity(self, me=0, waste_factor=10, skill=5):
        return self.quantity + self.me_waste(me=me, waste_factor=waste_factor) + self.pe_waste(skill=skill)

    def _display_str(self):
        return "%s x %s" % (self.material.name, self.quantity)

    class Meta:
        app_label = 'eve_sde'
        db_table = 'invTypeMaterials'


#####
# An Item's extra materials, and other requirements, are usually stored via it's blueprint_id
#####


class IndustryActivity(Model, StrMixin):

    activity_id = IntegerField(primary_key=True, db_column='activityID')
    name = CharField(max_length=100, db_column='activityName', blank=True)
    description = TextField(max_length=1000, blank=True)
    published = IntegerField(null=True, blank=True)
    icon_no = CharField(max_length=5, db_column='iconNo', blank=True)

    class Meta:
        app_label = 'eve_sde'
        db_table = 'ramActivities'


class AbstractRequirement(Model, StrMixin):

    material_id = IntegerField(db_column='requiredTypeID', primary_key=True, blank=True)
    activity_id = IntegerField(primary_key=True, db_column='activityID')
    #material = ForeignKey('Item', primary_key=False, db_column='requiredTypeID')

    quantity = IntegerField(null=True, blank=True)
    damage_per_job = FloatField(null=True, db_column='damagePerJob', blank=True)
    recycle = IntegerField(null=True, blank=True)

    class Meta:
        abstract = True
        db_table = 'ramTypeRequirements'

    def _display_str(self):
        return "%s x %s" % (self.material.name, self.quantity * self.damage_per_job)


class ExtraMaterial(AbstractRequirement):

    blueprint = ForeignKey('Blueprint', primary_key=True, db_column='typeID', related_name='extra_materials')
    activity = ForeignKey('IndustryActivity', primary_key=False, db_column='activityID', related_name='+')
    material = ForeignKey('Item', primary_key=False, db_column='requiredTypeID')

    objects = filtered_manager(activity_id=1, exclude=skill_filter)

    class Meta:
        app_label = 'eve_sde'
        db_table = 'ramTypeRequirements'


class ExtraSkill(AbstractRequirement):

    blueprint = ForeignKey('Blueprint', primary_key=True, db_column='typeID', related_name='extra_skills')
    activity = ForeignKey('IndustryActivity', primary_key=False, db_column='activityID', related_name='+')
    material = ForeignKey('Item', primary_key=False, db_column='requiredTypeID')

    objects = filtered_manager(activity_id=1, **skill_filter)

    class Meta:
        app_label = 'eve_sde'
        db_table = 'ramTypeRequirements'


class CopyMaterial(AbstractRequirement):

    blueprint = ForeignKey('Blueprint', primary_key=True, db_column='typeID', related_name='copy_materials')
    activity = ForeignKey('IndustryActivity', primary_key=False, db_column='activityID', related_name='+')
    material = ForeignKey('Item', primary_key=False, db_column='requiredTypeID')

    objects = filtered_manager(activity_id=5, exclude=skill_filter)

    class Meta:
        app_label = 'eve_sde'
        db_table = 'ramTypeRequirements'


class CopySkill(AbstractRequirement):

    blueprint = ForeignKey('Blueprint', primary_key=True, db_column='typeID', related_name='copy_skills')
    activity = ForeignKey('IndustryActivity', primary_key=False, db_column='activityID', related_name='+')
    material = ForeignKey('Item', primary_key=False, db_column='requiredTypeID')

    objects = filtered_manager(activity_id=5, **skill_filter)

    class Meta:
        app_label = 'eve_sde'
        db_table = 'ramTypeRequirements'


class InventionMaterial(AbstractRequirement):

    blueprint = ForeignKey('Blueprint', primary_key=True, db_column='typeID', related_name='invention_materials')
    activity = ForeignKey('IndustryActivity', primary_key=False, db_column='activityID', related_name='+')
    material = ForeignKey('Item', primary_key=False, db_column='requiredTypeID')

    objects = filtered_manager(activity_id=8, exclude=skill_filter)

    class Meta:
        app_label = 'eve_sde'
        db_table = 'ramTypeRequirements'


class InventionSkill(AbstractRequirement):

    blueprint = ForeignKey('Blueprint', primary_key=True, db_column='typeID', related_name='invention_skills')
    activity = ForeignKey('IndustryActivity', primary_key=False, db_column='activityID', related_name='+')
    material = ForeignKey('Item', primary_key=False, db_column='requiredTypeID')

    objects = filtered_manager(activity_id=8, **skill_filter)

    class Meta:
        app_label = 'eve_sde'
        db_table = 'ramTypeRequirements'


class ReverseEngineeringMaterial(AbstractRequirement):

    item = ForeignKey('Blueprint', primary_key=True, db_column='typeID', related_name='reverse_engineering_materials')
    activity = ForeignKey('IndustryActivity', primary_key=False, db_column='activityID', related_name='+')
    material = ForeignKey('Item', primary_key=False, db_column='requiredTypeID')

    objects = filtered_manager(activity_id=7, exclude=skill_filter)

    class Meta:
        app_label = 'eve_sde'
        db_table = 'ramTypeRequirements'


class ReverseEngineeringSkill(AbstractRequirement):

    item = ForeignKey('Blueprint', primary_key=True, db_column='typeID', related_name='reverse_engineering_skills')
    activity = ForeignKey('IndustryActivity', primary_key=False, db_column='activityID', related_name='+')
    material = ForeignKey('Item', primary_key=False, db_column='requiredTypeID')

    objects = filtered_manager(activity_id=7, **skill_filter)

    class Meta:
        app_label = 'eve_sde'
        db_table = 'ramTypeRequirements'


class Reaction(Item):

    objects = filtered_manager(group_id__in=[436, 484, 661, 662, 977])
    default_manager = objects

    class Meta:
        app_label = 'eve_sde'
        proxy = True

    def build_info(self):

        return {
            "inputs": dict((rinput.material, rinput.quantity) for rinput in self.inputs.select_related('material')),
            "products": dict((rinput.material, rinput.quantity) for rinput in self.inputs.select_related('material')),
        }


class ReactionInput(Model, StrMixin):
    reaction = ForeignKey('Reaction', primary_key=True, db_column='reactionTypeID', related_name='inputs')
    is_input = IntegerField(primary_key=True, db_column='input')
    material = ForeignKey('Item', primary_key=True, db_column='typeID', related_name='input_reactions')
    raw_quantity = IntegerField(null=True, blank=True, db_column='quantity')

    objects = filtered_manager(is_input=1)
    default_manager = objects

    class Meta:
        app_label = 'eve_sde'
        db_table = 'invTypeReactions'

    @property
    def quantity(self):
        return self.raw_quantity * (self.material.moon_mining_amount or 1)

    def _display_str(self):
        return "%s x %s" % (self.material.name, self.quantity)


class ReactionProduct(Model, StrMixin):
    reaction = ForeignKey('Reaction', primary_key=True, db_column='reactionTypeID', related_name='products')
    is_input = IntegerField(primary_key=True, db_column='input')
    material = ForeignKey('Item', primary_key=True, db_column='typeID', related_name='product_reactions')
    quantity = IntegerField(null=True, blank=True)

    objects = filtered_manager(is_input=0)
    default_manager = objects

    @property
    def quantity(self):
        return self.raw_quantity * (self.material.moon_mining_amount or 1)

    def _display_str(self):
        return "%s x %s" % (self.material.name, self.quantity)

    class Meta:
        app_label = 'eve_sde'
        db_table = 'invTypeReactions'


class Schematic(Model, StrMixin):

    schematic_id = IntegerField(primary_key=True, db_column='schematicID')
    name = CharField(max_length=255, db_column='schematicName', blank=True)
    cycle_time = IntegerField(null=True, db_column='cycleTime', blank=True)
    facility_types = ManyToManyField('Item', through='SchematicFacility')

    class Meta:
        app_label = 'eve_sde'
        db_table = 'planetSchematics'


class SchematicFacility(Model, StrMixin):

    schematic = ForeignKey('Schematic', primary_key=True, db_column='schematicID', related_name="+")
    facility = ForeignKey('Item', db_column='pinTypeID',  related_name="+")

    class Meta:
        app_label = 'eve_sde'
        db_table = 'planetSchematicsPinMap'


class SchematicInput(Model, StrMixin):

    schematic = ForeignKey('Schematic', primary_key=True, db_column='schematicID', related_name='inputs')
    material = ForeignKey('Item', primary_key=True, db_column='typeID', related_name='input_schematics')
    quantity = IntegerField(null=True, blank=True)
    is_input = IntegerField(null=True, db_column='isInput', blank=True)

    objects = filtered_manager(is_input=1)
    default_manager = objects

    class Meta:
        app_label = 'eve_sde'
        db_table = 'planetSchematicsTypeMap'

    def _display_str(self):
        return "%s x %s" % (self.material.name, self.quantity)


class SchematicProduct(Model, StrMixin):
    schematic = ForeignKey('Schematic', primary_key=True, db_column='schematicID', related_name='products')
    material = ForeignKey('Item', primary_key=True, db_column='typeID', related_name='product_schematics')
    quantity = IntegerField(null=True, blank=True)
    is_input = IntegerField(null=True, db_column='isInput', blank=True)

    objects = filtered_manager(is_input=0)
    default_manager = objects

    class Meta:
        app_label = 'eve_sde'
        db_table = 'planetSchematicsTypeMap'

    def _display_str(self):
        return "%s x %s" % (self.material.name, self.quantity)


class AssemblyLineType(Model, StrMixin):
    assembly_line_type_id = IntegerField(primary_key=True, db_column='assemblyLineTypeID')
    name = CharField(max_length=100, db_column='assemblyLineTypeName', blank=True)
    description = TextField(max_length=1000, blank=True)
    base_time_multiplier = FloatField(db_column='baseTimeMultiplier', blank=True)
    base_material_multiplier = FloatField(db_column='baseMaterialMultiplier', blank=True)
    volume = FloatField(blank=True)
    activity = ForeignKey('IndustryActivity', null=True, db_column='activityID', blank=True)
    min_cost_per_hour = FloatField(db_column='minCostPerHour', blank=True)

    class Meta:
        app_label = 'eve_sde'
        db_table = 'ramAssemblyLineTypes'


class AssemblyLine(Model, StrMixin):
    assembly_line_id = IntegerField(primary_key=True, db_column='assemblyLineID')
    assembly_line_type = ForeignKey('AssemblyLineType', null=True, db_column='assemblyLineTypeID', blank=True, related_name='assembly_lines')
    container_id = IntegerField(null=True, db_column='containerID', blank=True)
    next_free_time = DateTimeField(null=True, db_column='nextFreeTime', blank=True)
    ui_grouping_id = IntegerField(null=True, db_column='UIGroupingID', blank=True)
    cost_install = FloatField(db_column='costInstall', blank=True)
    cost_per_hour = FloatField(db_column='costPerHour', blank=True)
    restriction_mask = IntegerField(null=True, db_column='restrictionMask', blank=True)
    discount_per_good_standing_point = FloatField(db_column='discountPerGoodStandingPoint', blank=True)
    surcharge_per_bad_standing_point = FloatField(db_column='surchargePerBadStandingPoint', blank=True)
    minimum_standing = FloatField(db_column='minimumStanding', blank=True)
    minimum_char_security = FloatField(db_column='minimumCharSecurity', blank=True)
    minimum_corp_security = FloatField(db_column='minimumCorpSecurity', blank=True)
    maximum_char_security = FloatField(db_column='maximumCharSecurity', blank=True)
    maximum_corp_security = FloatField(db_column='maximumCorpSecurity', blank=True)
    owner = ForeignKey('Corporation', null=True, db_column='ownerID', blank=True, related_name='owned_assembly_lines')
    activity = ForeignKey('IndustryActivity', null=True, db_column='activityID', blank=True, related_name='assembly_lines')

    class Meta:
        app_label = 'eve_sde'
        db_table = 'ramAssemblyLines'


class StationAssemblyLine(Model, StrMixin):
    owner = ForeignKey('Corporation', null=True, db_column='ownerID', blank=True, related_name='owned_station_assembly_lines')
    region = ForeignKey('Region', null=True, db_column='regionID', blank=True)
    system = ForeignKey('System', null=True, db_column='solarSystemID', blank=True, related_name='station_assembly_lines')
    station = ForeignKey('Station', primary_key=True, db_column='stationID', related_name='station_assembly_lines')
    station_type = ForeignKey('StationType', null=True, db_column='stationTypeID', blank=True, related_name='+')
    assembly_line_type = ForeignKey('AssemblyLineType', primary_key=True, db_column='assemblyLineTypeID', related_name='station_assembly_lines')
    quantity = IntegerField(null=True, blank=True)

    class Meta:
        app_label = 'eve_sde'
        db_table = 'ramAssemblyLineStations'


class AssemblyLineCategoryDetail(Model, StrMixin):
    assembly_line_type = ForeignKey('AssemblyLineType', primary_key=True, db_column='assemblyLineTypeID', related_name='category_details')
    category = ForeignKey('ItemCategory', primary_key=True, db_column='categoryID', related_name='assembly_line_multipliers')
    time_multiplier = FloatField(db_column='timeMultiplier', blank=True)
    material_multiplier = FloatField(db_column='materialMultiplier', blank=True)

    class Meta:
        app_label = 'eve_sde'
        db_table = 'ramAssemblyLineTypeDetailPerCategory'


class AssemblyLineGroupDetail(Model, StrMixin):
    assembly_line_type = ForeignKey('AssemblyLineType', primary_key=True, db_column='assemblyLineTypeID', related_name='group_details')
    group = ForeignKey('ItemGroup', primary_key=True, db_column='groupID', related_name='assembly_line_multipliers')
    time_multiplier = FloatField(db_column='timeMultiplier', blank=True)
    material_multiplier = FloatField(db_column='materialMultiplier', blank=True)

    class Meta:
        app_label = 'eve_sde'
        db_table = 'ramAssemblyLineTypeDetailPerGroup'