from copy import deepcopy

from apis_bibsonomy.models import Reference
from apis_core.collections.models import SkosCollection
from apis_core.entities.abc import E21_Person, E53_Place, E74_Group, Entity
from apis_core.generic.abc import GenericModel, SimpleLabelModel
from apis_core.history.models import VersionMixin
from apis_core.relations.models import Relation
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models, transaction
from django.template.loader import render_to_string
from django_interval.fields import FuzzyDateParserField
from django_json_editor_field.fields import JSONEditorField

# The default options for JSONEditorFields, which are used
# in multiple models
jsoneditorfield_options = {
    "theme": "bootstrap4",
    "disable_collapse": True,
    "disable_edit_json": True,
    "disable_properties": True,
    "disable_array_reorder": True,
    "disable_array_delete_last_row": True,
    "disable_array_delete_all_rows": True,
    "prompt_before_delete": False,
}


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


class Profession(SimpleLabelModel): ...


class Title(SimpleLabelModel): ...


class Person(VersionMixin, E21_Person):
    """
    Person class, imported from old viecpro instance
    Decided to drop the `status` field
    `start` & `end` will become `date_of_birth` and `date_of_death`
    Decided to replace the pointers to texts with a JSON field containing the texts
    Decided to replace pointers to labels with `labels` JSON field
    Decided to replace pointer to "data merged from" relation with `merged_into` field
    """

    review = models.BooleanField(default=False)
    date_of_birth = FuzzyDateParserField(blank=True, null=True)
    date_of_death = FuzzyDateParserField(blank=True, null=True)
    references = models.TextField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    published = models.BooleanField(default=False)

    title = models.ManyToManyField(Title, blank=True)
    professions = models.ManyToManyField(Profession, blank=True)

    texts_schema = {
        "title": "Texts",
        "type": "array",
        "format": "table",
        "items": {
            "type": "object",
            "properties": {
                "text-type": {
                    "type": "string",
                    "pattern": "^.+$",
                    "options": {
                        "inputAttributes": {
                            "required": True,
                        },
                    },
                },
                "text": {
                    "type": "string",
                    "pattern": "^.+$",
                    "options": {
                        "inputAttributes": {
                            "required": True,
                        },
                    },
                },
            },
        },
    }

    texts = JSONEditorField(
        schema=texts_schema, options=jsoneditorfield_options, null=True
    )

    labels_schema = {
        "title": "Labels",
        "type": "array",
        "format": "table",
        "items": {
            "type": "object",
            "properties": {
                "label-type": {
                    "type": "string",
                    "pattern": "^.+$",
                    "options": {
                        "inputAttributes": {
                            "required": True,
                        },
                    },
                },
                "label": {
                    "type": "string",
                    "pattern": "^.+$",
                    "options": {
                        "inputAttributes": {
                            "required": True,
                        },
                    },
                },
            },
        },
    }

    # imported from pointers to labels
    labels = JSONEditorField(
        schema=labels_schema, options=jsoneditorfield_options, null=True
    )

    # imported from "data merged from" relation
    merged_into = models.ForeignKey(
        "Person",
        on_delete=models.PROTECT,
        editable=False,
        null=True,
        related_name="merged",
    )
    # for the django-grouper logic
    grouped_into = models.ForeignKey(
        "Person",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="grouped",
    )

    # helper attribute, to know what the old entity was
    legacy_metainfo_id = models.IntegerField(editable=False, null=True)

    def djg_merge_preview(self):
        return render_to_string(
            "apis_instance_viecpro/djg_person_merge_preview.html", {"object": self}
        )

    @transaction.atomic
    def djg_merge(self, others):
        new_pers = deepcopy(self)
        new_pers.pk = None
        new_pers.id = None
        new_pers._state.adding = True
        new_pers.save()
        for m2m in ["professions", "title"]:
            m2m_objcts = getattr(self, m2m).all()
            if m2m_objcts.count() > 0:
                getattr(new_pers, m2m).add(*m2m_objcts)
        col, _ = SkosCollection.objects.get_or_create(name="Vorfinale Einträge")
        col.add(new_pers)

        save = False
        for field in ["notes", "references"]:
            for person in others:
                if getattr(person, field) and len(getattr(person, field)) > 0:
                    add_value = f"\n--\n{person.id}: {getattr(person, field)}"
                    orig_value = getattr(new_pers, field) or ""
                    setattr(new_pers, field, orig_value + add_value)
                    save = True
        for person in others:
            if person.labels:
                new_pers.labels += person.labels
                save = True
            if person.texts:
                new_pers.texts += person.texts
                save = True
            for profession in person.professions.all():
                new_pers.professions.add(profession)
            for title in person.title.all():
                new_pers.title.add(title)
        if save:
            new_pers.save()

        pers_ids = [pers.id for pers in others + [self]]
        subj_relations = Relation.objects.filter(
            subj_content_type=self.get_self_content_type, subj_object_id__in=pers_ids
        ).select_subclasses()
        for rel in subj_relations:
            rel.pk = rel.id = None
            rel.subj_object_id = new_pers.pk
            rel._state.adding = True
            rel.save()
        obj_relations = Relation.objects.filter(
            obj_content_type=self.get_self_content_type, obj_object_id__in=pers_ids
        ).select_subclasses()
        for rel in obj_relations:
            rel.pk = rel.id = None
            rel.obj_object_id = new_pers.pk
            rel._state.adding = True
            rel.save()

        for ref in Reference.objects.filter(
            content_type=self.get_self_content_type, object_id__in=pers_ids
        ):
            ref.pk = ref.id = None
            ref._state.adding = True
            ref.object_id = new_pers.pk
            ref.save()

        for person in others + [self]:
            person.grouped_into = new_pers
            person.save()

        coldub, _ = SkosCollection.objects.get_or_create(name="Dubletten")
        for person in others + [self]:
            coldub.add(person)
        return new_pers.get_absolute_url()


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

    labels_schema = {
        "title": "Labels",
        "type": "array",
        "format": "table",
        "items": {
            "type": "object",
            "properties": {
                "label-type": {
                    "type": "string",
                    "pattern": "^.+$",
                    "options": {
                        "inputAttributes": {
                            "required": True,
                        },
                    },
                },
                "label": {
                    "type": "string",
                    "pattern": "^.+$",
                    "options": {
                        "inputAttributes": {
                            "required": True,
                        },
                    },
                },
            },
        },
    }

    # imported from pointers to labels
    labels = JSONEditorField(
        schema=labels_schema, options=jsoneditorfield_options, null=True
    )

    # helper attribute, to know what the old entity was
    legacy_metainfo_id = models.IntegerField(editable=False, null=True)


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

    labels_schema = {
        "title": "Labels",
        "type": "array",
        "format": "table",
        "items": {
            "type": "object",
            "properties": {
                "label-type": {
                    "type": "string",
                    "pattern": "^.+$",
                    "options": {
                        "inputAttributes": {
                            "required": True,
                        },
                    },
                },
                "label": {
                    "type": "string",
                    "pattern": "^.+$",
                    "options": {
                        "inputAttributes": {
                            "required": True,
                        },
                    },
                },
            },
        },
    }

    # imported from pointers to labels
    labels = JSONEditorField(
        schema=labels_schema, options=jsoneditorfield_options, null=True
    )

    # helper attribute, to know what the old entity was
    legacy_metainfo_id = models.IntegerField(editable=False, null=True)

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

    labels_schema = {
        "title": "Labels",
        "type": "array",
        "format": "table",
        "items": {
            "type": "object",
            "properties": {
                "label-type": {
                    "type": "string",
                    "pattern": "^.+$",
                    "options": {
                        "inputAttributes": {
                            "required": True,
                        },
                    },
                },
                "label": {
                    "type": "string",
                    "pattern": "^.+$",
                    "options": {
                        "inputAttributes": {
                            "required": True,
                        },
                    },
                },
            },
        },
    }

    # imported from pointers to labels
    labels = JSONEditorField(
        schema=labels_schema, options=jsoneditorfield_options, null=True
    )

    # helper attribute, to know what the old entity was
    legacy_metainfo_id = models.IntegerField(editable=False, null=True)


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
