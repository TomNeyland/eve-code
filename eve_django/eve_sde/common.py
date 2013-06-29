from django.db.models import Model, Manager, ForeignKey, IntegerField, FloatField, CharField, TextField, ManyToManyField, OneToOneField, DateTimeField
from django.conf import settings


# This shouldn't be hardcoded
SKILL_GROUP_IDS = [255, 256, 257, 258, 266, 268, 269, 270, 271, 272, 273, 274, 275, 278, 505, 989, 1044, 1161]

#Needs to be removed
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


def filtered_manager(**filters):
    qfilters = {}
    qfilters.update(filters)
    class FilteredManager(Manager):
        use_for_related_fields = True
        filters = qfilters

        def all(self):
            return self.get_query_set().all()

        def get_query_set(self):
            print self
            return super(FilteredManager, self).get_query_set().filter(**self.filters)
    return FilteredManager()


class UniqueName(Model, StrMixin):
    name_id = IntegerField(primary_key=True, db_column='itemID')
    group = ForeignKey('ItemGroup', null=True, db_column='groupID', related_name='unique_items')
    name = CharField(max_length=200, db_column='itemName')

    class Meta:
        db_table = 'invUniqueNames'
