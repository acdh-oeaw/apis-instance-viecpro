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
from django.utils.translation import gettext_lazy as _
from django_interval.fields import FuzzyDateParserField
from django_json_editor_field.fields import JSONEditorField

from apis_instance_viecpro.DateParser import parse_date_wrapper
from apis_instance_viecpro.jsonschemata import labels_schema

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
    STATUS_CHOICES = [
        ("red", "red"),
        ("yellow", "yellow"),
        ("green", "green"),
    ]
    status = models.CharField(max_length=300, choices=STATUS_CHOICES)
    note = models.TextField(blank=True, null=True)

    content_type = models.ForeignKey(
        ContentType, on_delete=models.CASCADE, null=True, db_index=True
    )
    object_id = models.PositiveIntegerField(null=True, db_index=True)
    content_object = GenericForeignKey("content_type", "object_id")

    class Meta:
        verbose_name = _("Status")
        verbose_name_plural = _("Statuses")
        constraints = [
            models.UniqueConstraint(
                fields=("content_type", "object_id"), name="unique_content_object"
            )
        ]

    def __str__(self):
        return f"{self.content_object} -> {self.status}"


class Source(GenericModel):
    class Meta:
        verbose_name = _("Source")
        verbose_name_plural = _("Sources")

    orig_filename = models.CharField(
        max_length=255, verbose_name=_("original filename")
    )
    indexed = models.IntegerField(verbose_name=_("indexed"))
    pubinfo = models.CharField(max_length=400, verbose_name=_("pubinfo"))
    author = models.CharField(max_length=255, verbose_name=_("author"))
    orig_id = models.PositiveIntegerField(
        blank=True, null=True, verbose_name=_("original ID")
    )

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True)
    object_id = models.PositiveIntegerField(null=True)
    content_object = GenericForeignKey("content_type", "object_id")

    def __str__(self):
        return (
            f"{self.orig_filename or ''}: {self.pubinfo or ''} -> {self.content_object}"
        )


class Profession(SimpleLabelModel):
    class Meta:
        verbose_name = _("Profession")
        verbose_name_plural = _("Professions")


class Title(SimpleLabelModel):
    class Meta:
        verbose_name = _("Title")
        verbose_name_plural = _("Titles")


class ViecrproModelManager(models.Manager):
    def get_queryset(self):
        qs = super().get_queryset()
        content_type = ContentType.objects.get_for_model(qs.model)
        return qs.annotate(
            ampel_value=models.Subquery(
                Ampel.objects.filter(
                    content_type=content_type, object_id=models.OuterRef("pk")
                ).values("status")
            )
        )


class Person(E21_Person, VersionMixin):
    """
    Person class, imported from old viecpro instance
    Decided to drop the `status` field
    `start` & `end` will become `date_of_birth` and `date_of_death`
    Decided to replace the pointers to texts with a JSON field containing the texts
    Decided to replace pointers to labels with `labels` JSON field
    Decided to replace pointer to "data merged from" relation with `merged_into` field
    """

    date_of_birth = FuzzyDateParserField(
        blank=True,
        null=True,
        parser=parse_date_wrapper,
        verbose_name=_("date of birth"),
    )
    date_of_death = FuzzyDateParserField(
        blank=True,
        null=True,
        parser=parse_date_wrapper,
        verbose_name=_("date of death"),
    )
    references = models.TextField(blank=True, null=True, verbose_name=_("references"))
    notes = models.TextField(blank=True, null=True, verbose_name=_("notes"))
    published = models.BooleanField(default=False, verbose_name=_("published"))

    title = models.ManyToManyField(Title, blank=True, verbose_name=_("title"))
    professions = models.ManyToManyField(
        Profession, blank=True, verbose_name=_("professions")
    )

    objects = ViecrproModelManager()

    texts_schema = {
        "title": "Texts",
        "type": "array",
        "format": "table",
        "items": {
            "type": "object",
            "properties": {
                "type": {
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
                    "format": "textarea",
                    "pattern": "^.+$",
                    "options": {
                        "inputAttributes": {
                            "required": True,
                            "rows": 1,
                            "class": "grow form-control",
                        },
                    },
                },
            },
        },
    }

    texts = JSONEditorField(
        schema=texts_schema,
        options=jsoneditorfield_options,
        null=True,
        verbose_name=_("texts"),
    )

    # imported from pointers to labels
    labels = JSONEditorField(
        schema=labels_schema,
        options=jsoneditorfield_options,
        null=True,
        verbose_name=_("labels"),
    )

    # imported from "data merged from" relation
    merged_into = models.ForeignKey(
        "Person",
        on_delete=models.PROTECT,
        editable=False,
        null=True,
        related_name="merged",
        verbose_name=_("merged into"),
    )
    # for the django-grouper logic
    grouped_into = models.ForeignKey(
        "Person",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="grouped",
        verbose_name=_("grouped into"),
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


class InstitutionType(SimpleLabelModel):
    class Meta:
        verbose_name = _("institution type")
        verbose_name_plural = _("institution types")

    legacy_vocab_id = models.IntegerField(null=True, editable=False)


class Institution(E74_Group, VersionMixin):
    """
    Institution class, imported from old viecpro instance `ApisEntitiesInstitution`
    `name` will become `label`
    """

    institution_type = models.ForeignKey(
        InstitutionType,
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        verbose_name=_("institution type"),
    )

    start = FuzzyDateParserField(
        null=True, blank=True, parser=parse_date_wrapper, verbose_name=_("start")
    )
    end = FuzzyDateParserField(
        null=True, blank=True, parser=parse_date_wrapper, verbose_name=_("end")
    )
    status = models.CharField(
        max_length=100, null=True, blank=True, verbose_name=_("status")
    )
    references = models.TextField(blank=True, null=True, verbose_name=_("references"))
    notes = models.TextField(blank=True, null=True, verbose_name=_("notes"))
    published = models.BooleanField(default=False, verbose_name=_("published"))

    # imported from pointers to labels
    labels = JSONEditorField(
        schema=labels_schema,
        options=jsoneditorfield_options,
        null=True,
        verbose_name=_("labels"),
    )

    # helper attribute, to know what the old entity was
    legacy_metainfo_id = models.IntegerField(editable=False, null=True)
    objects = ViecrproModelManager()


class EventType(SimpleLabelModel):
    class Meta:
        verbose_name = _("event type")
        verbose_name_plural = _("event types")

    legacy_vocab_id = models.IntegerField(null=True, editable=False)


class Event(VersionMixin, Entity):
    """
    Event class, imported from old viecpro instance `ApisEntitiesEvent`
    The `type` attribute will be sourced from `ApisVocabulariesbaseclass.name`
    it should be a choicefield in the form afterwards
    """

    class Meta:
        verbose_name = _("event")
        verbose_name_plural = _("events")

    event_type = models.ForeignKey(
        EventType,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        verbose_name=_("event type"),
    )

    name = models.CharField(max_length=255, null=True, verbose_name=_("name"))
    start = FuzzyDateParserField(
        null=True, blank=True, parser=parse_date_wrapper, verbose_name=_("start")
    )
    end = FuzzyDateParserField(
        null=True, blank=True, parser=parse_date_wrapper, verbose_name=_("end")
    )
    status = models.CharField(
        max_length=100, null=True, blank=True, verbose_name=_("status")
    )
    references = models.TextField(blank=True, null=True, verbose_name=_("references"))
    notes = models.TextField(blank=True, null=True, verbose_name=_("notes"))
    published = models.BooleanField(default=False, verbose_name=_("published"))

    # imported from pointers to labels
    labels = JSONEditorField(
        schema=labels_schema,
        options=jsoneditorfield_options,
        null=True,
        verbose_name=_("labels"),
    )

    # helper attribute, to know what the old entity was
    legacy_metainfo_id = models.IntegerField(editable=False, null=True)
    objects = ViecrproModelManager()

    def __str__(self):
        return self.name


class PlaceType(SimpleLabelModel):
    class Meta:
        verbose_name = _("place type")
        verbose_name_plural = _("place types")

    legacy_vocab_id = models.IntegerField(null=True, editable=False)


class Place(E53_Place, VersionMixin):
    """
    Place class, imported from old viecrpo instance `ApisEntitiesPlace`
    `name` becomes `label`
    `kind` should become `feature_code`, but it contains german names
    that probably have to be mapped to `feature_code` at some point
    """

    place_type = models.ForeignKey(
        PlaceType,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        verbose_name=_("place type"),
    )
    start = FuzzyDateParserField(
        null=True, blank=True, parser=parse_date_wrapper, verbose_name=_("start")
    )
    end = FuzzyDateParserField(
        null=True, blank=True, parser=parse_date_wrapper, verbose_name=_("end")
    )
    status = models.CharField(
        max_length=100, null=True, blank=True, verbose_name=_("status")
    )
    references = models.TextField(blank=True, null=True, verbose_name=_("references"))
    notes = models.TextField(blank=True, null=True, verbose_name=_("notes"))
    published = models.BooleanField(default=False, verbose_name=_("published"))

    # imported from pointers to labels
    labels = JSONEditorField(
        schema=labels_schema,
        options=jsoneditorfield_options,
        null=True,
        verbose_name=_("labels"),
    )

    # helper attribute, to know what the old entity was
    legacy_metainfo_id = models.IntegerField(editable=False, null=True)
    objects = ViecrproModelManager()


class Payment(VersionMixin, Entity): ...


# class FunctionTopic(VersionMixin, GenericModel):
#    label = models.CharField()
#    definition = models.TextField()
#    source = models.TextField()
#
#    def __str__(self):
#        return self.label or "Unlabelled FunctionTopic"
#
#
# class FunctionType(VersionMixin, GenericModel):
#    label = models.CharField()
#    topic = models.ForeignKey(FunctionTopic, on_delete=models.PROTECT, null=True)
#    alternative_labels = models.JSONField(null=True)
#    comment = models.TextField(null=True)
#
#    def __str__(self):
#        return self.label or "Unlabelled FunctionType"


#############
# Relations #
#############


class LegacyRelation(VersionMixin, Relation):
    class Meta:
        abstract = True

    start = FuzzyDateParserField(
        max_length=255,
        blank=True,
        null=True,
        parser=parse_date_wrapper,
        verbose_name=_("start"),
    )
    end = FuzzyDateParserField(
        max_length=255,
        blank=True,
        null=True,
        parser=parse_date_wrapper,
        verbose_name=_("end"),
    )
    status = models.CharField(
        max_length=100, blank=True, null=True, editable=False, verbose_name=_("status")
    )
    references = models.TextField(blank=True, null=True, verbose_name=_("references"))
    notes = models.TextField(blank=True, null=True, verbose_name=_("notes"))
    objects = ViecrproModelManager()


class LegacyRelationType(VersionMixin, GenericModel):
    class Meta:
        abstract = True

    label = models.CharField(max_length=255, blank=True, null=True)
    label_reverse = models.CharField(max_length=255, blank=True, null=True)
    legacy_vocab_id = models.IntegerField(null=True, editable=False)

    def __str__(self):
        return f"{self.label} <-> {self.label_reverse}"


class InstitutionInstitutionRelationType(LegacyRelationType):
    class Meta:
        verbose_name = _("institution instition relation type")
        verbose_name_plural = _("institution institution relation types")

    parent = models.ForeignKey(
        "self",
        models.SET_NULL,
        blank=True,
        null=True,
        verbose_name=_("parent relation type"),
    )


class InstitutionInstitutionRelation(LegacyRelation):
    # 1684 ApisRelationsInstitutioninstitution
    class Meta:
        verbose_name = _("institution institution relation")
        verbose_name_plural = _("institution institution relations")

    subj_model = Institution
    obj_model = Institution

    type = models.ForeignKey(
        InstitutionInstitutionRelationType,
        models.DO_NOTHING,
        blank=True,
        null=True,
        verbose_name=_("type"),
    )


class InstitutionPlaceRelationType(LegacyRelationType):
    class Meta:
        verbose_name = _("institution place relation type")
        verbose_name_plural = _("institution place relation types")


class InstitutionPlaceRelation(LegacyRelation):
    # 903 ApisRelationsInstitutionplace
    class Meta:
        verbose_name = _("institution place relation")
        verbose_name_plural = _("institution place relations")

    subj_model = Institution
    obj_model = Place

    type = models.ForeignKey(
        InstitutionPlaceRelationType,
        models.DO_NOTHING,
        blank=True,
        null=True,
        verbose_name=_("type"),
    )


class PersonEventRelationType(LegacyRelationType):
    class Meta:
        verbose_name = _("person event relation type")
        verbose_name_plural = _("person event relation types")


class PersonEventRelation(LegacyRelation):
    # 80 ApisRelationsPersonevent
    class Meta:
        verbose_name = _("person event relation")
        verbose_name_plural = _("person even relations")

    subj_model = Person
    obj_model = Event

    type = models.ForeignKey(
        PersonEventRelationType,
        models.DO_NOTHING,
        blank=True,
        null=True,
        verbose_name=_("type"),
    )


class OverarchingFunctionalTerm(SimpleLabelModel):
    class Meta:
        verbose_name = _("overarching functional term")
        verbose_name_plural = _("overarching functional terms")

    field_of_activity = models.CharField(
        max_length=400, null=True, blank=True, verbose_name=_("field of activity")
    )
    label = models.CharField(
        max_length=255, null=True, blank=True, verbose_name=_("function generic term")
    )
    definition = models.TextField(blank=True, null=True, verbose_name=_("definition"))
    source = models.CharField(
        max_length=400, null=True, blank=True, verbose_name=_("source")
    )

    def __str__(self):
        return super().__str__() + " (FOB)"


class PersonInstitutionRelationType(LegacyRelationType):
    class Meta:
        verbose_name = _("person institution relation type")
        verbose_name_plural = _("person institution relation types")

    parent = models.ForeignKey(
        "self",
        models.SET_NULL,
        blank=True,
        null=True,
        verbose_name=_("parent relation type"),
    )
    synonyms_schema = {
        "title": "Texts",
        "type": "array",
        "format": "table",
        "items": {
            "type": "string",
            "options": {
                "inputAttributes": {
                    "required": True,
                    "placeholder": "Synonym",
                },
            },
        },
    }
    synonyms = JSONEditorField(
        schema=synonyms_schema,
        options=jsoneditorfield_options,
        null=True,
        verbose_name=_("synonyms"),
    )
    overarching_functional_term = models.ForeignKey(
        OverarchingFunctionalTerm,
        models.SET_NULL,
        blank=True,
        null=True,
        verbose_name=_("overarching functional term"),
    )


class PersonInstitutionRelation(LegacyRelation):
    # 80088 ApisRelationsPersoninstitution
    # ApisRelationsPersoninstitution.relation_type = Funktionstyp
    # ApisVocabulariesVocabsbaseclass.description = FunctionType.comment (falls das ausefüllt ist)
    class Meta:
        verbose_name = _("person institution relation")
        verbose_name_plural = _("person institution relations")

    subj_model = Person
    obj_model = Institution

    type = models.ForeignKey(
        PersonInstitutionRelationType,
        models.DO_NOTHING,
        blank=True,
        null=True,
        verbose_name=_("type"),
    )


class PersonPersonRelationType(LegacyRelationType):
    class Meta:
        verbose_name = _("person person relation type")
        verbose_name_plural = _("person person relation types")

    parent = models.ForeignKey(
        "self",
        models.SET_NULL,
        blank=True,
        null=True,
        verbose_name=_("parent relation type"),
    )


class PersonPersonRelation(LegacyRelation):
    # 21811 ApisRelationsPersonperson
    class Meta:
        verbose_name = _("person person relation")
        verbose_name_plural = _("person person relations")

    subj_model = Person
    obj_model = Person

    type = models.ForeignKey(
        PersonPersonRelationType,
        models.SET_NULL,
        blank=True,
        null=True,
        verbose_name=_("type"),
    )


class PersonPlaceRelationType(LegacyRelationType):
    class Meta:
        verbose_name = _("person place relation type")
        verbose_name_plural = _("person place relation types")


class PersonPlaceRelation(LegacyRelation):
    # 8150 ApisRelationsPersonplace
    class Meta:
        verbose_name = _("person place relation")
        verbose_name_plural = _("person place relations")

    subj_model = Person
    obj_model = Place

    type = models.ForeignKey(
        PersonPlaceRelationType,
        models.SET_NULL,
        blank=True,
        null=True,
        verbose_name=_("type"),
    )


class PlaceEventRelationType(LegacyRelationType):
    class Meta:
        verbose_name = _("place event relation type")
        verbose_name_plural = _("place event relation types")


class PlaceEventRelation(LegacyRelation):
    # 14 ApisRelationsPlaceevent
    class Meta:
        verbose_name = _("place event relation")
        verbose_name_plural = _("place event relations")

    subj_model = Place
    obj_model = Event

    type = models.ForeignKey(
        PlaceEventRelationType,
        models.SET_NULL,
        blank=True,
        null=True,
        verbose_name=_("type"),
    )


class PlacePlaceRelationType(LegacyRelationType):
    class Meta:
        verbose_name = _("place place relation type")
        verbose_name_plural = _("place place relation types")


class PlacePlaceRelation(LegacyRelation):
    # 3045 ApisRelationsPlaceplace
    class Meta:
        verbose_name = _("place place relation")
        verbose_name_plural = _("place place relations")

    subj_model = Place
    obj_model = Place

    type = models.ForeignKey(
        PlacePlaceRelationType,
        models.DO_NOTHING,
        blank=True,
        null=True,
        verbose_name=_("type"),
    )


# Relationen
#
# class PaymentTo(Relationen):
#    subj_model = Payment
#    obj_model = Person
#
# class PaymentFrom(Relationen):
#    subj_model = Payment
#    obj_model = Person


# decided to not use this after all
# class HasFunction(LegacyRelation):
#    subj_model = Person
#    obj_model = Institution
#
#    legacy_relation_vocab_label = None
#    legacy_relation_vocab_label_reverse = None
#    type = models.ForeignKey(FunctionType, on_delete=models.PROTECT)
