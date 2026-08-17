from apis_core.entities.abc import E21_Person, E53_Place, E74_Group, Entity
from apis_core.generic.abc import GenericModel
from apis_core.history.models import VersionMixin
from apis_core.relations.models import Relation
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django_interval.fields import FuzzyDateParserField


class Ampel(GenericModel):
    status = models.CharField(max_length=300)
    note = models.TextField(blank=True, null=True)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True)
    object_id = models.PositiveIntegerField(null=True)
    content_object = GenericForeignKey("content_type", "object_id")

    def __str__(self):
        return f"{self.content_object} -> {self.status}"


class Source(GenericModel):
    orig_filename = models.CharField(max_length=255)
    indexed = models.IntegerField()
    pubinfo = models.CharField(max_length=400)
    author = models.CharField(max_length=255)
    orig_id = models.PositiveIntegerField(blank=True, null=True)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True)
    object_id = models.PositiveIntegerField(null=True)
    content_object = GenericForeignKey("content_type", "object_id")

    def __str__(self):
        return (
            f"{self.orig_filename or ''}: {self.pubinfo or ''} -> {self.content_object}"
        )


class Person(VersionMixin, E21_Person):
    """
    Person class, imported from old viecpro instance
    Decided to drop the `status` field
    `start` & `end` will become `date_of_birth` and `date_of_death`
    Decided to replace the pointers to texts with types `diverses`, `ereignisdatum` & `quellenzitat`
    with attributes on the model
    Decided to replace pointers to labels with `labels` JSON field
    Decided to replace pointer to "data merged from" relation with `merged_into` field
    """

    review = models.BooleanField(default=False)
    date_of_birth = FuzzyDateParserField(null=True)
    date_of_death = FuzzyDateParserField(null=True)
    references = models.TextField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    published = models.BooleanField(default=False)

    # imported from texts with types `diverses`, `ereignisdatum` & `quellenzitat`
    diverses = models.TextField()
    ereignisdatum = models.TextField()
    quellenzitat = models.TextField()

    # imported from pointers to labels
    labels = models.JSONField(null=True)

    # imported from "data merged from" relation
    merged_into = models.IntegerField(editable=False, null=True)


class Institution(VersionMixin, E74_Group):
    """
    Institution class, imported from old viecpro instance `ApisEntitiesInstitution`
    `name` will become `label`
    """

    type = models.CharField(max_length=255, null=True)

    review = models.BooleanField(default=False)
    start = FuzzyDateParserField(null=True)
    end = FuzzyDateParserField(null=True)
    status = models.CharField(max_length=100, null=True)
    references = models.TextField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    published = models.BooleanField(default=False)


class Event(VersionMixin, Entity):
    """
    Event class, imported from old viecpro instance `ApisEntitiesEvent`
    The `type` attribute will be sourced from `ApisVocabulariesbaseclass.name`
    it should be a choicefield in the form afterwards
    """

    type = models.CharField(null=True)

    name = models.CharField(max_length=255, null=True)
    review = models.BooleanField(default=False)
    start = FuzzyDateParserField(null=True)
    end = FuzzyDateParserField(null=True)
    status = models.CharField(max_length=100, null=True)
    references = models.TextField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    published = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Place(VersionMixin, E53_Place):
    """
    Place class, imported from old viecrpo instance `ApisEntitiesPlace`
    `name` becomes `label`
    `kind` should become `feature_code`, but it contains german names
    that probably have to be mapped to `feature_code` at some point
    """

    review = models.BooleanField(default=False)
    kind = models.CharField(max_length=100, null=True)
    start = FuzzyDateParserField(null=True)
    end = FuzzyDateParserField(null=True)
    status = models.CharField(max_length=100, null=True)
    references = models.TextField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    published = models.BooleanField(default=False)


class Payment(VersionMixin, Entity): ...


class FunctionTopic(VersionMixin, GenericModel):
    label = models.CharField()
    definition = models.TextField()
    source = models.TextField()

    def __str__(self):
        return self.label or "Unlabelled FunctionTopic"


class FunctionType(VersionMixin, GenericModel):
    label = models.CharField()
    topic = models.ForeignKey(FunctionTopic, on_delete=models.PROTECT, null=True)
    alternative_labels = models.JSONField(null=True)
    comment = models.TextField(null=True)

    def __str__(self):
        return self.label or "Unlabelled FunctionType"


#############
# Relations #
#############


class LegacyRelation(VersionMixin, Relation):
    class Meta:
        abstract = True

    label = models.CharField(max_length=255, blank=True, null=True)
    start = FuzzyDateParserField(max_length=255, blank=True, null=True)
    end = FuzzyDateParserField(max_length=255, blank=True, null=True)
    review = models.BooleanField(default=False, editable=False)
    status = models.CharField(max_length=100, blank=True, null=True, editable=False)
    references = models.TextField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    legacy_relation_vocab_label = models.CharField(
        max_length=255, blank=True, null=True
    )
    legacy_relation_vocab_label_reverse = models.CharField(
        max_length=255, blank=True, null=True
    )


class InstitutionInstitutionRelation(LegacyRelation):
    # 1684 ApisRelationsInstitutioninstitution
    subj_model = Institution
    obj_model = Institution


class InstitutionPlaceRelation(LegacyRelation):
    # 903 ApisRelationsInstitutionplace
    subj_model = Institution
    obj_model = Place


class PersonEventRelation(LegacyRelation):
    # 80 ApisRelationsPersonevent
    subj_model = Person
    obj_model = Event


class PersonInstitutionRelation(LegacyRelation):
    # 80088 ApisRelationsPersoninstitution
    # ApisRelationsPersoninstitution.relation_type = Funktionstyp
    # ApisVocabulariesVocabsbaseclass.description = FunctionType.comment (falls das ausefüllt ist)
    subj_model = Person
    obj_model = Institution


class PersonPersonRelation(LegacyRelation):
    # 21811 ApisRelationsPersonperson
    subj_model = Person
    obj_model = Person


class PersonPlaceRelation(LegacyRelation):
    # 8150 ApisRelationsPersonplace
    subj_model = Person
    obj_model = Place


class PlaceEventRelation(LegacyRelation):
    # 14 ApisRelationsPlaceevent
    subj_model = Place
    obj_model = Event


class PlacePlaceRelation(LegacyRelation):
    # 3045 ApisRelationsPlaceplace
    subj_model = Place
    obj_model = Place


# Relationen
#
# class PaymentTo(Relationen):
#    subj_model = Payment
#    obj_model = Person
#
# class PaymentFrom(Relationen):
#    subj_model = Payment
#    obj_model = Person


class HasFunction(LegacyRelation):
    subj_model = Person
    obj_model = Institution

    legacy_relation_vocab_label = None
    legacy_relation_vocab_label_reverse = None
    type = models.ForeignKey(FunctionType, on_delete=models.PROTECT)
