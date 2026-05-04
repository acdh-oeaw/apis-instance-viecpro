from django.db import models
from apis_core.apis_entities.abc import E53_Place, E21_Person, E74_Group
from apis_core.history.models import VersionMixin
from apis_core.relations.models import Relation
from apis_core.entities.abc import Entity
from apis_core.generic.abc import GenericModel
from django_interval.fields import FuzzyDateParserField


class Person(VersionMixin, Entity, E21_Person):
    diverses = models.TextField()
    ereignisdatum = models.TextField()
    quellenzitat = models.TextField()

    labels = models.JSONField()
    notes = models.TextField()
    merged_into = models.IntegerField(editable=False)


class Institution(VersionMixin, Entity, E74_Group): ...


class Event(VersionMixin, Entity): ...


class Place(VersionMixin, Entity, E53_Place): ...


class Payment(VersionMixin, Entity): ...


class FunctionTopic(VersionMixin, GenericModel):
    label = models.CharField()
    definition = models.TextField()
    source = models.TextField()


class FunctionType(VersionMixin, GenericModel):
    label = models.CharField()
    topic = models.ForeignKey(FunctionTopic, on_delete=models.PROTECT)
    alternative_labels = models.JSONField()
    comment = models.TextField()


# Relationen
#
# class PaymentTo(Relationen):
#    subj_model = Payment
#    obj_model = Person
#
# class PaymentFrom(Relationen):
#    subj_model = Payment
#    obj_model = Person


class HasFunction(VersionMixin, Relation):
    subj_model = Person
    obj_model = Institution

    start = FuzzyDateParserField()
    end = FuzzyDateParserField()
    type = models.ForeignKey(FunctionType, on_delete=models.PROTECT)
