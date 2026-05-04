from django.db import models
from apis_core.apis_entities.abc import E53_Place, SimpleLabelModel, E21_Person, E74_Group
from apis_core.history.models import VersionMixin
from apis_core.relations.models import Relation
from apis_core.generic.abc import GenericModel
from django_interval.fields import FuzzyDateParserField


class Person(VersionMixin, E21_Person):
    diverses = models.TextField()
    ereignisdatum = models.TextField()
    quellenzitat = models.TextField()

    labels = models.JSONField()
    notes = models.TextField()
    merged_into = models.IntegerField(editable=False)


class Institution(VersionMixin, E74_Group): ...


class Event: ...


class Place(E53_Place): ...


class Payment: ...


class FunctionTopic(GenericModel):
    label = models.CharField()
    definition = models.TextField()
    source = models.TextField()


class FunctionType(GenericModel):
    label = models.CharField()
    topic = models.ForeignKey(FunctionTopic, on_delete=models.PROTECT)
    alternative_labels = mdoels.JSONField()
    comment = models.TextField()


# Relationen
#
#class PaymentTo(Relationen):
#    subj_model = Payment
#    obj_model = Person
#
#class PaymentFrom(Relationen):
#    subj_model = Payment
#    obj_model = Person

class HasFunction(Relation):
    subj_model = Person
    obj_model = Institution

    start = FuzzyDateParserField()
    end = FuzzyDateParserField()
    type = models.ForeignKey(FunctionType, on_delete=models.PROTECT)
