from django.db.models import Model, Manager, ForeignKey, IntegerField, FloatField, CharField, TextField, ManyToManyField, OneToOneField, DateTimeField
from common_models import StrMixin


class ControlTowerResourcePurpose(Model, StrMixin):

    purpose = IntegerField(primary_key=True, db_column='purpose')
    purpose_text = CharField(max_length=100, db_column='purposeText', blank=True)

    class Meta:
        app_label = 'eve_sde'
        db_table = 'invControlTowerResourcePurposes'


class ControlTowerResource(Model, StrMixin):

    control_tower = ForeignKey('Item', primary_key=True, db_column='controlTowerTypeID', related_name='control_tower_resources')
    resource = ForeignKey('Item', primary_key=True, db_column='resourceTypeID', related_name='control_tower_usage')
    purpose = ForeignKey('ControlTowerResourcePurpose', db_column='purpose', null=True, blank=True)
    quantity = IntegerField(null=True, blank=True)
    min_security_level = FloatField(db_column='minSecurityLevel', blank=True)
    faction = ForeignKey('Faction', null=True, db_column='factionID', blank=True, related_name='control_tower_requirements')

    class Meta:
        app_label = 'eve_sde'
        db_table = 'invControlTowerResources'


class TranslationTable(Model, StrMixin):

    source_table = CharField(max_length=200, primary_key=True, db_column='sourceTable')
    destination_table = CharField(max_length=200, db_column='destinationTable', blank=True)
    translated_key = CharField(max_length=200, primary_key=True, db_column='translatedKey')
    tc_group_id = IntegerField(null=True, db_column='tcGroupID', blank=True)
    tc_id = IntegerField(null=True, db_column='tcID', blank=True)

    class Meta:
        app_label = 'eve_sde'
        db_table = 'translationTables'


class TranslationColumn(Model, StrMixin):

    tc_group_id = IntegerField(null=True, db_column='tcGroupID', blank=True)
    tc_id = IntegerField(primary_key=True, db_column='tcID')
    table_name = CharField(max_length=256, db_column='tableName')
    column_name = CharField(max_length=128, db_column='columnName')
    master_id = CharField(max_length=128, db_column='masterID', blank=True)

    class Meta:
        app_label = 'eve_sde'
        db_table = 'trnTranslationColumns'


class TranslationLanguage(Model, StrMixin):

    numeric_language_id = IntegerField(primary_key=True, db_column='numericLanguageID')
    language_id = CharField(max_length=50, db_column='languageID', blank=True)
    language_name = CharField(max_length=200, db_column='languageName', blank=True)

    class Meta:
        app_label = 'eve_sde'
        db_table = 'trnTranslationLanguages'


class Translation(Model, StrMixin):

    tc_id = IntegerField(primary_key=True, db_column='tcID')
    key_id = IntegerField(primary_key=True, db_column='keyID')
    language_id = CharField(max_length=50, primary_key=True, db_column='languageID')
    text = TextField(blank=True)

    class Meta:
        app_label = 'eve_sde'
        db_table = 'trnTranslations'
