from django.db.models import Model, Manager, ForeignKey, IntegerField, FloatField, CharField, TextField, ManyToManyField, OneToOneField, DateTimeField
from common_models import filtered_manager, StrMixin, UniqueName, BaseStaticItem, BaseMapItem, AbstractMapItem
from item_models import Item


class StationType(Item):
    item_type = OneToOneField('Item',  db_column='stationTypeID', to_field='item_id', parent_link=True, related_name='+')
    operation = ForeignKey('Operation', null=True, db_column='operationID', blank=True, related_name='station_types')
    station_type_id = IntegerField(primary_key=True, db_column='stationTypeID')
    dock_entry_x = FloatField(db_column='dockEntryX', blank=True)
    dock_entry_y = FloatField(db_column='dockEntryY', blank=True)
    dock_entry_z = FloatField(db_column='dockEntryZ', blank=True)
    dock_orientation_x = FloatField(db_column='dockOrientationX', blank=True)
    dock_orientation_y = FloatField(db_column='dockOrientationY', blank=True)
    dock_orientation_z = FloatField(db_column='dockOrientationZ', blank=True)
    office_slots = IntegerField(null=True, db_column='officeSlots', blank=True)
    reprocessing_efficiency = FloatField(db_column='reprocessingEfficiency', blank=True)
    conquerable = IntegerField(null=True, blank=True)

    class Meta:
        app_label = 'eve_sde'
        db_table = 'staStationTypes'


class StationDenorm(AbstractMapItem):

    station_denorm_id = IntegerField(primary_key=True, db_column='itemID')
    moon = ForeignKey('Moon', null=True, db_column='orbitID', blank=True, related_name='stations')

    objects = filtered_manager(group_id=15)

    class Meta:
        db_table = 'mapDenormalize'
        app_label = 'eve_sde'


class Station(StationDenorm):
    station_denorm = OneToOneField('StationDenorm', parent_link=True, to_field='station_denorm_id', db_column='stationID', related_name='station')

    station_id = IntegerField(primary_key=True, db_column='stationID')
    station_type = ForeignKey('StationType', null=True, db_column='stationTypeID', blank=True, related_name='stations')
    #name = CharField(max_length=100, db_column='stationName', blank=True) #  currently being pulled from parent
    #security = IntegerField(null=True, blank=True) #  currently being pulled from parent
    #x = FloatField(blank=True) #  currently being pulled from parent
    #y = FloatField(blank=True) #  currently being pulled from parent
    #z = FloatField(blank=True) #  currently being pulled from parent

    region = ForeignKey('Region', null=True, db_column='regionID', blank=True)
    constellation = ForeignKey('Constellation', null=True, db_column='constellationID', blank=True, related_name='stations')
    system = ForeignKey('System', null=True, db_column='solarSystemID', blank=True, related_name='stations')
    corporation = ForeignKey('Corporation', null=True, db_column='corporationID', blank=True, related_name='stations')
    operation = ForeignKey('Operation', null=True, db_column='operationID', blank=True, related_name='operation_stations')

    docking_cost_per_volume = FloatField(db_column='dockingCostPerVolume', blank=True)
    max_ship_volume_dockable = FloatField(db_column='maxShipVolumeDockable', blank=True)
    office_rental_cost = FloatField(null=True, db_column='officeRentalCost', blank=True)
    reprocessing_efficiency = FloatField(db_column='reprocessingEfficiency', blank=True)
    reprocessing_stations_take = FloatField(db_column='reprocessingStationsTake', blank=True)
    reprocessing_hangar_flag = FloatField(null=True, db_column='reprocessingHangarFlag', blank=True)

    class Meta:
        app_label = 'eve_sde'
        db_table = 'staStations'


class OperationService(Model, StrMixin):
    operation = ForeignKey('Operation', primary_key=True, db_column='operationID', related_name='+')
    service = ForeignKey('StationService', primary_key=True, db_column='serviceID', related_name='+')

    class Meta:
        app_label = 'eve_sde'
        db_table = 'staOperationServices'


class StationService(Model, StrMixin):
    service_id = IntegerField(primary_key=True, db_column='serviceID')
    name = CharField(max_length=100, db_column='serviceName', blank=True)
    description = TextField(max_length=1000, blank=True)
    operations = ManyToManyField('Operation', through='OperationService')

    class Meta:
        app_label = 'eve_sde'
        db_table = 'staServices'


class Operation(Model, StrMixin):
    activity_id = IntegerField(null=True, db_column='activityID', blank=True)
    operation_id = IntegerField(primary_key=True, db_column='operationID')
    name = CharField(max_length=100, db_column='operationName', blank=True)
    description = TextField(max_length=1000, blank=True)
    fringe = IntegerField(null=True, blank=True)
    corridor = IntegerField(null=True, blank=True)
    hub = IntegerField(null=True, blank=True)
    border = IntegerField(null=True, blank=True)
    ratio = IntegerField(null=True, blank=True)
    caldari_station_type = ForeignKey('Item', null=True, db_column='caldariStationTypeID', blank=True, related_name='caldari_station_operations')
    minmatar_station_type = ForeignKey('Item', null=True, db_column='minmatarStationTypeID', blank=True, related_name='minmatar_station_operations')
    amarr_station_type = ForeignKey('Item', null=True, db_column='amarrStationTypeID', blank=True, related_name='amarr_station_operations')
    gallente_station_type = ForeignKey('Item', null=True, db_column='gallenteStationTypeID', blank=True, related_name='gallente_station_operations')
    jove_station_type = ForeignKey('Item', null=True, db_column='joveStationTypeID', blank=True, related_name='jove_station_operations')
    services = ManyToManyField('StationService', through='OperationService')

    class Meta:
        app_label = 'eve_sde'
        db_table = 'staOperations'
