from django.db.models import Model, Manager, ForeignKey, IntegerField, FloatField, CharField, TextField, ManyToManyField, OneToOneField, DateTimeField
from django.conf import settings
from common_models import StrMixin, filtered_manager, BaseStaticItem, BaseMapItem


class Race(Model, StrMixin):
    race_id = IntegerField(primary_key=True, db_column='raceID')
    name = CharField(max_length=100, db_column='raceName', blank=True)
    description = TextField(max_length=1000, blank=True)
    icon_id = IntegerField(null=True, db_column='iconID', blank=True)
    short_description = TextField(max_length=500, db_column='shortDescription', blank=True)

    class Meta:
        app_label = 'eve_sde'
        db_table = 'chrRaces'


class CharacterBloodline(Model, StrMixin):
    bloodline_id = IntegerField(primary_key=True, db_column='bloodlineID')
    name = CharField(max_length=100, db_column='bloodlineName', blank=True)
    race = ForeignKey('Race', null=True, db_column='raceID', blank=True, related_name='bloodlines')
    description = TextField(max_length=1000, blank=True)
    male_description = TextField(max_length=1000, db_column='maleDescription', blank=True)
    female_description = TextField(max_length=1000, db_column='femaleDescription', blank=True)
    ship_type = ForeignKey('Item', null=True, db_column='shipTypeID', blank=True)
    corporation = ForeignKey('Corporation', null=True, db_column='corporationID', blank=True, related_name='bloodlines')
    perception = IntegerField(null=True, blank=True)
    willpower = IntegerField(null=True, blank=True)
    charisma = IntegerField(null=True, blank=True)
    memory = IntegerField(null=True, blank=True)
    intelligence = IntegerField(null=True, blank=True)
    iconid = IntegerField(null=True, db_column='iconID', blank=True)
    short_description = TextField(max_length=500, db_column='shortDescription', blank=True)
    short_male_description = TextField(max_length=500, db_column='shortMaleDescription', blank=True)
    short_female_description = TextField(max_length=500, db_column='shortFemaleDescription', blank=True)

    class Meta:
        app_label = 'eve_sde'
        db_table = 'chrBloodlines'


class Ancestry(Model, StrMixin):
    ancestry_id = IntegerField(primary_key=True, db_column='ancestryID')
    name = CharField(max_length=100, db_column='ancestryName', blank=True)
    bloodline = ForeignKey('CharacterBloodline', null=True, db_column='bloodlineID', blank=True, related_name='ancestries')
    description = TextField(max_length=1000, blank=True)
    perception = IntegerField(null=True, blank=True)
    willpower = IntegerField(null=True, blank=True)
    charisma = IntegerField(null=True, blank=True)
    memory = IntegerField(null=True, blank=True)
    intelligence = IntegerField(null=True, blank=True)
    icon_id = IntegerField(null=True, db_column='iconID', blank=True)
    short_description = TextField(max_length=500, db_column='shortDescription', blank=True)

    class Meta:
        app_label = 'eve_sde'
        db_table = 'chrAncestries'


class CharacterAttribute(Model, StrMixin):
    attribute_id = IntegerField(primary_key=True, db_column='attributeID')
    name = CharField(max_length=100, db_column='attributeName', blank=True)
    description = TextField(max_length=1000, blank=True)
    icon_id = IntegerField(null=True, db_column='iconID', blank=True)
    short_description = TextField(max_length=500, db_column='shortDescription', blank=True)
    notes = CharField(max_length=500, blank=True)

    class Meta:
        app_label = 'eve_sde'
        db_table = 'chrAttributes'


class CertificateCategory(Model, StrMixin):
    
    category_id = IntegerField(primary_key=True, db_column='categoryID')
    description = TextField(max_length=500, blank=True)
    name = CharField(max_length=256, db_column='categoryName', blank=True)

    class Meta:
        app_label = 'eve_sde'
        db_table = 'crtCategories'


class Certificate(Model, StrMixin):
    certificate_id = IntegerField(primary_key=True, db_column='certificateID')
    cert_category = ForeignKey('CertificateCategory', null=True, db_column='categoryID', blank=True, related_name='certificates') #  meh cert_
    cert_class = ForeignKey('CertificateClass', null=True, db_column='classID', blank=True, related_name='certificates')
    grade = IntegerField(null=True, blank=True)
    corporation = ForeignKey('Corporation', null=True, db_column='corpID', blank=True, related_name='certificates')
    icon_id = IntegerField(null=True, db_column='iconID', blank=True)
    description = TextField(max_length=500, blank=True)

    class Meta:
        app_label = 'eve_sde'
        db_table = 'crtCertificates'


class CertificateClass(Model, StrMixin):
    class_id = IntegerField(primary_key=True, db_column='classID')
    description = TextField(max_length=500, blank=True)
    name = CharField(max_length=256, db_column='className', blank=True)

    class Meta:
        app_label = 'eve_sde'
        db_table = 'crtClasses'


class CertificateRecommendation(Model, StrMixin):
    recommendation_id = IntegerField(primary_key=True, db_column='recommendationID')
    ship = ForeignKey('Item', null=True, db_column='shipTypeID', blank=True, related_name='certificate_recommendations')
    certificate = ForeignKey('Certificate', null=True, db_column='certificateID', blank=True)
    recommendation_level = IntegerField(db_column='recommendationLevel')

    class Meta:
        app_label = 'eve_sde'
        db_table = 'crtRecommendations'


class CertificateRelationship(Model, StrMixin):
    relationship_id = IntegerField(primary_key=True, db_column='relationshipID')
    required_certificate = ForeignKey('Certificate', null=True, db_column='parentID', blank=True, related_name='child_certificates')
    required_skill = ForeignKey('Item', null=True, db_column='parentTypeID', blank=True, related_name='child_certificates')
    required_level = IntegerField(null=True, db_column='parentLevel', blank=True)
    child_certificate = ForeignKey('Certificate', null=True, db_column='childID', blank=True)

    class Meta:
        app_label = 'eve_sde'
        db_table = 'crtRelationships'
