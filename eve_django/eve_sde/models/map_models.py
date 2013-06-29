from django.db.models import Model, Manager, ForeignKey, IntegerField, FloatField, CharField, TextField, ManyToManyField, OneToOneField, DateTimeField
from common_models import filtered_manager, StrMixin, AbstractMapItem, BaseMapItem


class Universe(Model, StrMixin):

    universe_id = IntegerField(primary_key=True, db_column='universeID')
    name = CharField(max_length=100, db_column='universeName', blank=True)

    x = FloatField(blank=True)
    y = FloatField(blank=True)
    z = FloatField(blank=True)
    x_min = FloatField(db_column='xMin', blank=True)
    x_max = FloatField(db_column='xMax', blank=True)
    y_min = FloatField(db_column='yMin', blank=True)
    y_max = FloatField(db_column='yMax', blank=True)
    z_min = FloatField(db_column='zMin', blank=True)
    z_max = FloatField(db_column='zMax', blank=True)
    radius = FloatField(blank=True)

    class Meta:
        db_table = 'mapUniverse'


class Region(BaseMapItem):
    map_item = OneToOneField('BaseMapItem', parent_link=True, to_field='map_item_id', db_column='regionID')
    region_id = IntegerField(primary_key=True, db_column='regionID')
    #name = CharField(max_length=100, db_column='regionName', blank=True)

    jumps = ManyToManyField('self', through='Jump', related_name='+', symmetrical=False)

    neighbors = ManyToManyField('self', through="RegionJump", symmetrical=False)

    #x = FloatField(blank=True)
    #y = FloatField(blank=True)
    #z = FloatField(blank=True)
    xmin = FloatField(db_column='xMin', blank=True)
    xmax = FloatField(db_column='xMax', blank=True)
    ymin = FloatField(db_column='yMin', blank=True)
    ymax = FloatField(db_column='yMax', blank=True)
    zmin = FloatField(db_column='zMin', blank=True)
    zmax = FloatField(db_column='zMax', blank=True)
    #radius = FloatField(blank=True)
    faction = ForeignKey('Faction', null=True, db_column='factionID', blank=True, related_name='faction_regions')

    class Meta:
        app_label = 'eve_sde'
        db_table = 'mapRegions'


class RegionJump(Model, StrMixin):

    from_region = ForeignKey('Region', primary_key=True, db_column='fromRegionID', related_name='+')
    to_region = ForeignKey('Region', primary_key=True, db_column='toRegionID', related_name='+')

    class Meta:
        app_label = 'eve_sde'
        db_table = 'mapRegionJumps'

    def _display_str(self):
        return "%s --> %s" % (self.from_region.name, self.to_reigon.name)


class Constellation(Model, StrMixin):

    constellation_id = IntegerField(primary_key=True, db_column='constellationID')
    name = CharField(max_length=100, db_column='constellationName', blank=True)

    region = ForeignKey('Region', null=True, db_column='regionID', blank=True, related_name='constellations')
    jumps = ManyToManyField('self', through='Jump', related_name='+', symmetrical=False)
    neighbors = ManyToManyField('self', through="ConstellationJump", symmetrical=False)

    x = FloatField(blank=True)
    y = FloatField(blank=True)
    z = FloatField(blank=True)
    xmin = FloatField(db_column='xMin', blank=True)
    xmax = FloatField(db_column='xMax', blank=True)
    ymin = FloatField(db_column='yMin', blank=True)
    ymax = FloatField(db_column='yMax', blank=True)
    zmin = FloatField(db_column='zMin', blank=True)
    zmax = FloatField(db_column='zMax', blank=True)
    radius = FloatField(blank=True)

    faction = ForeignKey('Faction', null=True, db_column='factionID', blank=True, related_name='faction_constellations')

    class Meta:
        app_label = 'eve_sde'
        db_table = 'mapConstellations'


class ConstellationJump(Model, StrMixin):

    from_region = ForeignKey('Region', null=True, db_column='fromRegionID', blank=True, related_name='+')
    from_constellation = ForeignKey('Constellation', primary_key=True, db_column='fromConstellationID', related_name='+')
    to_constellation = ForeignKey('Constellation', primary_key=True, db_column='toConstellationID', related_name='+')
    to_region = ForeignKey('Region', null=True, db_column='toRegionID', blank=True, related_name='+')

    class Meta:
        app_label = 'eve_sde'
        db_table = 'mapConstellationJumps'


class System(Model, StrMixin):

    system_id = IntegerField(primary_key=True, db_column='solarSystemID')
    name = CharField(max_length=100, db_column='solarSystemName', blank=True)

    region = ForeignKey('Region', null=True, db_column='regionID', blank=True, related_name='systems')
    constellation = ForeignKey('Constellation', null=True, db_column='constellationID', blank=True, related_name='constellations')
    jumps = ManyToManyField('self', through='Jump', related_name='+', symmetrical=False)

    x = FloatField(blank=True)
    y = FloatField(blank=True)
    z = FloatField(blank=True)
    xmin = FloatField(db_column='xMin', blank=True)
    xmax = FloatField(db_column='xMax', blank=True)
    ymin = FloatField(db_column='yMin', blank=True)
    ymax = FloatField(db_column='yMax', blank=True)
    zmin = FloatField(db_column='zMin', blank=True)
    zmax = FloatField(db_column='zMax', blank=True)
    luminosity = FloatField(blank=True)
    border = IntegerField(null=True, blank=True)
    fringe = IntegerField(null=True, blank=True)
    corridor = IntegerField(null=True, blank=True)
    hub = IntegerField(null=True, blank=True)
    international = IntegerField(null=True, blank=True)
    regional = IntegerField(null=True, blank=True)
    constellation = IntegerField(null=True, blank=True)
    security = FloatField(blank=True)
    faction = ForeignKey('Faction', null=True, db_column='factionID', blank=True, related_name='faction_systems')
    radius = FloatField(blank=True)
    sun_type = ForeignKey('Item', null=True, db_column='sunTypeID', blank=True, related_name='+')
    security_class = CharField(max_length=2, db_column='securityClass', blank=True)
    combat_zones = ManyToManyField('CombatZone', through='CombatZoneSystem')

    objects = filtered_manager()
    wormholes = filtered_manager(name__regex='^(J[0-9])')

    class Meta:
        app_label = 'eve_sde'
        db_table = 'mapSolarSystems'


class Jump(Model, StrMixin):

    from_region = ForeignKey('Region', null=True, db_column='fromRegionID', blank=True, related_name='outgoing_jumps')
    from_constellation = ForeignKey('Constellation', null=True, db_column='fromConstellationID', blank=True, related_name='outgoing_jumps')
    from_system = ForeignKey('System', primary_key=True, db_column='fromSolarSystemID', related_name='outgoing_jumps')
    to_system = ForeignKey('System', primary_key=True, db_column='toSolarSystemID', related_name='incoming_jumps')
    to_constellation = ForeignKey('Constellation', null=True, db_column='toConstellationID', blank=True, related_name='incoming_jumps')
    to_region = ForeignKey('Region', null=True, db_column='toRegionID', blank=True, related_name='incoming_jumps')

    class Meta:
        db_table = 'mapSolarSystemJumps'
        app_label = 'eve_sde'


class Stargate(AbstractMapItem):

    stargate_id = IntegerField(primary_key=True, db_column='itemID')

    system = ForeignKey('System', db_column='solarSystemID', related_name='stargates')
    constellation = ForeignKey('Constellation', null=True, db_column='constellationID', blank=True, related_name='stargates')
    region = ForeignKey('Region', null=True, db_column='regionID', blank=True, related_name='stargates')

    destination = ManyToManyField('self', through='StargateJump', related_name="+", symmetrical=False)

    objects = filtered_manager(base_type__group_id=10)

    class Meta:
        db_table = 'mapDenormalize'
        app_label = 'eve_sde'


class StargateJump(Model, StrMixin):

    from_stargate = OneToOneField('Stargate', primary_key=True, db_column='stargateID', related_name='+')
    to_stargate = OneToOneField('Stargate', null=True, db_column='celestialID', blank=True, related_name='+')

    class Meta:
        db_table = 'mapJumps'
        app_label = 'eve_sde'


class Star(AbstractMapItem):

    star_id = IntegerField(primary_key=True, db_column='itemID')

    system = ForeignKey('System', null=True, db_column='solarSystemID', blank=True, related_name='stars')
    constellation = ForeignKey('Constellation', null=True, db_column='constellationID', blank=True, related_name='stars')
    region = ForeignKey('Region', null=True, db_column='regionID', blank=True, related_name='stars')

    objects = filtered_manager(group_id=6)

    class Meta:
        db_table = 'mapDenormalize'
        app_label = 'eve_sde'


class Planet(AbstractMapItem):

    planet_id = IntegerField(primary_key=True, db_column='itemID')

    star = ForeignKey('Star', null=True, db_column='orbitID', blank=True, related_name='planets')
    system = ForeignKey('System', null=True, db_column='solarSystemID', blank=True, related_name='planets')
    constellation = ForeignKey('Constellation', null=True, db_column='constellationID', blank=True, related_name='planets')
    region = ForeignKey('Region', null=True, db_column='regionID', blank=True, related_name='planets')

    objects = filtered_manager(group_id=7)

    class Meta:
        db_table = 'mapDenormalize'
        app_label = 'eve_sde'


class AsteroidBelt(AbstractMapItem):

    belt_id = IntegerField(primary_key=True, db_column='itemID')

    planet = ForeignKey('Planet', null=True, db_column='orbitID', blank=True, related_name='asteroid_belts')
    system = ForeignKey('System', null=True, db_column='solarSystemID', blank=True, related_name='asteroid_belts')
    constellation = ForeignKey('Constellation', null=True, db_column='constellationID', blank=True, related_name='asteroid_belts')
    region = ForeignKey('Region', null=True, db_column='regionID', blank=True, related_name='asteroid_belts')

    objects = filtered_manager(group_id=9)

    class Meta:
        db_table = 'mapDenormalize'
        app_label = 'eve_sde'


class Moon(AbstractMapItem):

    moon_id = IntegerField(primary_key=True, db_column='itemID')

    planet = ForeignKey('Planet', null=True, db_column='orbitID', blank=True, related_name='moons')
    system = ForeignKey('System', null=True, db_column='solarSystemID', blank=True, related_name='moons')
    constellation = ForeignKey('Constellation', null=True, db_column='constellationID', blank=True, related_name='moons')
    region = ForeignKey('Region', null=True, db_column='regionID', blank=True, related_name='moons')

    objects = filtered_manager(group_id=8)

    class Meta:
        db_table = 'mapDenormalize'
        app_label = 'eve_sde'


class Landmark(Model, StrMixin):

    landmark_id = IntegerField(primary_key=True, db_column='landmarkID')
    name = CharField(max_length=100, db_column='landmarkName', blank=True)

    location = ForeignKey('System', null=True, db_column='locationID', blank=True, related_name='landmarks')

    description = TextField(max_length=7000, blank=True)
    x = FloatField(blank=True)
    y = FloatField(blank=True)
    z = FloatField(blank=True)
    radius = FloatField(blank=True)
    icon_id = IntegerField(null=True, db_column='iconID', blank=True)
    importance = IntegerField(null=True, blank=True)

    class Meta:
        app_label = 'eve_sde'
        db_table = 'mapLandmarks'


class CelestialStatistics(Model, StrMixin):

    celestial_id = IntegerField(primary_key=True, db_column='celestialID')

    temperature = FloatField(blank=True)
    spectral_class = CharField(max_length=10, db_column='spectralClass', blank=True)
    luminosity = FloatField(blank=True)
    age = FloatField(blank=True)
    life = FloatField(blank=True)
    orbit_radius = FloatField(db_column='orbitRadius', blank=True)
    eccentricity = FloatField(blank=True)
    mass_dust = FloatField(db_column='massDust', blank=True)
    mass_gas = FloatField(db_column='massGas', blank=True)
    fragmented = IntegerField(null=True, blank=True)
    density = FloatField(blank=True)
    surface_gravity = FloatField(db_column='surfaceGravity', blank=True)
    escape_velocity = FloatField(db_column='escapeVelocity', blank=True)
    orbit_period = FloatField(db_column='orbitPeriod', blank=True)
    rotation_rate = FloatField(db_column='rotationRate', blank=True)
    locked = IntegerField(null=True, blank=True)
    pressure = FloatField(blank=True)
    radius = FloatField(blank=True)
    mass = FloatField(blank=True)

    class Meta:
        db_table = 'mapCelestialStatistics'
        app_label = 'eve_sde'


class CombatZoneSystem(Model, StrMixin):

    system = ForeignKey('System', primary_key=True, db_column='solarSystemID', related_name='+')
    combat_zone = ForeignKey('CombatZone', primary_key=True, db_column='combatZoneID', blank=True, related_name='+')

    class Meta:
        app_label = 'eve_sde'
        db_table = 'warCombatZoneSystems'


class CombatZone(Model, StrMixin):

    combat_zone_id = IntegerField(primary_key=True, db_column='combatZoneID')
    name = CharField(max_length=100, db_column='combatZoneName', blank=True)

    faction = IntegerField(null=True, db_column='factionID', blank=True)
    center_system = OneToOneField('System', null=True, db_column='centerSystemID', blank=True, related_name='combat_zone')  # could use a better related_name
    description = TextField(max_length=500, blank=True)
    systems = ManyToManyField('System', through='CombatZoneSystem')

    class Meta:
        app_label = 'eve_sde'
        db_table = 'warCombatZones'


class RegionGraphic(Model, StrMixin):

    graphic_id = IntegerField(null=True, db_column='graphicID', blank=True)

    region = ForeignKey('Region', primary_key=True, db_column='locationID', related_name='region_graphics')
    map_item = OneToOneField('BaseMapItem', to_field='map_item_id', db_column='locationID')

    class Meta:
        app_label = 'eve_sde'
        db_table = 'mapLocationScenes'


class WormholeClass(Model, StrMixin):

    location = OneToOneField("BaseMapItem", primary_key=True, db_column='locationID', related_name='wormhole_class')
    wormhole_class = IntegerField(null=True, db_column='wormholeClassID', blank=True)

    class Meta:
        app_label = 'eve_sde'
        db_table = 'mapLocationWormholeClasses'

