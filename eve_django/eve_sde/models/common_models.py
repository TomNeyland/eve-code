from django.db.models import Model, Manager, ForeignKey, IntegerField, FloatField, CharField, TextField, ManyToManyField, OneToOneField, DateTimeField
from django.conf import settings


# This shouldn't be hardcoded
SKILL_GROUP_IDS = [255, 256, 257, 258, 266, 268, 269, 270, 271, 272, 273, 274, 275, 278, 505, 989, 1044, 1161]


class StrMixin(object):
    """This class mixin removes the need for boilerplate str/unicode methods"""

    def _display_str(self):
        out = ""

        if getattr(self, "display_name", None):
            out = out + self.display_name

        elif getattr(self, 'name', None):
            out = out + self.name
        else:
            out = self.__class__.__name__
            if hasattr(self, 'pk'):
                out = out + '<%s>' % (self.pk,)

        return out

    @classmethod
    def model_doc(self):
        meta = self._meta
        table_rows = []
        for field in sorted(meta.local_fields, key=lambda f: f.name):
            table_rows.append((field.name, field.db_column, "<strong>"+field.rel.to.__name__+"</strong>" if field.rel else field.__class__.__name__))
        table_rows = "\n".join([table_row_template % table_row for table_row in table_rows])
        return table_template % (meta.object_name, table_rows)

    def __str__(self):
        return self._display_str()

    def __unicode__(self):
        return u"%s" % self._display_str()

    def __repr__(self):
        return self._display_str()

    @classmethod
    def test_counts(model):
        total = model.objects.all().count()

        unique_max = UniqueName.objects.all().count()
        name_max = Name.objects.all().count()

        unique_count = UniqueName.objects.filter(unique_name_id__in=model.objects.all().values_list('pk', flat=True)).count()
        name_count = Name.objects.filter(item_id__in=model.objects.all().values_list('pk', flat=True)).count()

        unique_only = UniqueName.objects.filter(unique_name_id__in=model.objects.all().values_list('pk', flat=True)) \
            .exclude(pk__in=Name.objects.all().values_list('pk', flat=True)).count()

        name_only = Name.objects.filter(item_id__in=model.objects.all().values_list('pk', flat=True)) \
            .exclude(pk__in=UniqueName.objects.all().values_list('pk', flat=True)).count()

        print "%s %s Count\n(%s of %s) Name Count\n(%s of %s) Unique Count\n(%s of %s) Name Only\n(%s of %s) Unique Only" % (total, model.__name__, name_count, name_max, unique_count, unique_max, name_only, name_max, unique_only, unique_max)
        return total, name_count, unique_count


def filtered_manager(**filters):
    qfilters = {}
    qxfilters = {}
    qxfilters.update(filters.pop("exclude", {}))
    qfilters.update(filters)

    class FilteredManager(Manager):
        use_for_related_fields = True
        filters = qfilters
        xfilters = qxfilters

        def all(self):
            return self.get_query_set().all()

        def get_query_set(self):
            return super(FilteredManager, self).get_query_set().filter(**self.filters).exclude(**self.xfilters)

    return FilteredManager()


class Name(Model, StrMixin):

    item_id = IntegerField(primary_key=True, db_column='itemID')
    name = CharField(max_length=200, db_column='itemName')

    class Meta:
        db_table = 'invNames'
        app_label = 'eve_sde'


class UniqueName(Model, StrMixin):

    name_id = IntegerField(primary_key=True, db_column='itemID')
    group = ForeignKey('ItemGroup', null=True, db_column='groupID', related_name='unique_items')
    name = CharField(max_length=200, db_column='itemName')

    class Meta:
        db_table = 'invUniqueNames'
        app_label = 'eve_sde'


class BaseStaticItem(UniqueName):
    unique_name = OneToOneField('UniqueName', parent_link=True, to_field='name_id', db_column='itemID')
    static_id = IntegerField(primary_key=True, db_column='itemID')
    base_type = ForeignKey('Item', db_column='typeID', related_name='+')
    flag = ForeignKey('ItemFlag', db_column='flagID', related_name='flagged_static_items')
    quantity = IntegerField()

    class Meta:
        db_table = 'invItems'
        app_label = 'eve_sde'


class AbstractMapItem(Model, StrMixin):
    stats = OneToOneField('CelestialStatistics', to_field='celestial_id', db_column='itemID', related_name='+', null=True)
    name = CharField(max_length=100, db_column='itemName', blank=True)
    group = ForeignKey('ItemGroup', null=True, db_column='groupID', blank=True, related_name='+')
    base_type = ForeignKey('Item', null=True, db_column='typeID', blank=True, related_name='+')
    x = FloatField(blank=True)
    y = FloatField(blank=True)
    z = FloatField(blank=True)
    radius = FloatField(blank=True)
    security = FloatField(blank=True)
    celestial_index = FloatField(null=True, db_column='celestialIndex', blank=True)
    orbit_index = FloatField(null=True, db_column='orbitIndex', blank=True)

    class Meta:
        abstract = True
        db_table = 'mapDenormalize'
        app_label = 'eve_sde'


class BaseMapItem(Model, StrMixin):
    stats = OneToOneField('CelestialStatistics', to_field='celestial_id', db_column='itemID', related_name='map_item', null=True)
    name = CharField(max_length=100, db_column='itemName', blank=True)
    map_item_id = IntegerField(primary_key=True, db_column='itemID')
    group = ForeignKey('ItemGroup', null=True, db_column='groupID', blank=True, related_name='+')
    base_type = ForeignKey('Item', null=True, db_column='typeID', blank=True, related_name='+')
    x = FloatField(blank=True)
    y = FloatField(blank=True)
    z = FloatField(blank=True)
    radius = FloatField(blank=True)
    security = FloatField(blank=True)
    celestial_index = FloatField(null=True, db_column='celestialIndex', blank=True)
    orbit_index = FloatField(null=True, db_column='orbitIndex', blank=True)

    class Meta:
        db_table = 'mapDenormalize'
        app_label = 'eve_sde'


class StaticItemPosition(Model, StrMixin):
    item = OneToOneField('BaseMapItem', primary_key=True, db_column='itemID', related_name='+') #bad naming
    x = FloatField()
    y = FloatField()
    z = FloatField()
    yaw = FloatField(blank=True)
    pitch = FloatField(blank=True)
    roll = FloatField(blank=True)

    class Meta:
        app_label = 'eve_sde'
        db_table = 'invPositions'


class Unit(Model, StrMixin):
    unit_id = IntegerField(primary_key=True, db_column='unitID')
    name = CharField(max_length=100, db_column='unitName', blank=True)
    display_name = CharField(max_length=50, db_column='displayName', blank=True)
    description = TextField(max_length=1000, blank=True)

    class Meta:
        db_table = 'eveUnits'
        app_label = 'eve_sde'


table_template = \
"""
### %s ###
<table>
    <tr>
       <th>Field</th>
       <th>Type<th>
       <th>SDE Column</th>
    </tr>
%s
</table>
"""

table_row_template = \
"""    <tr>
        <td>%s</td>
        <td>%s</td>
        <td>%s</td>
    <tr>"""
