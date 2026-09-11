# ruff: noqa: E402, F403, F405
import pathlib
import django
import logging
import functools
import json
from collections import defaultdict

django.setup()

from apis_instance_viecpro.models import (
    Person,
    Institution,
    Event,
    FunctionType,
    Place,
    Source,
    Ampel,
    InstitutionInstitutionRelation,
    InstitutionPlaceRelation,
    PersonEventRelation,
    PersonInstitutionRelation,
    PersonPersonRelation,
    PersonPlaceRelation,
    PlaceEventRelation,
    PlacePlaceRelation,
    HasFunction,
)
from apis_bibsonomy.models import Reference
from apis_instance_viecpro.old_models import *
from apis_core.collections.models import SkosCollection
from django.contrib.contenttypes.models import ContentType
from django.conf import settings
from django.core import serializers
from django.db import connections
from django.db import OperationalError


## Based on code from django-db-reconnect
logger = logging.getLogger(__name__)

DEFAULT_ERROR_CODES = [
    2006,  # MySQL server has gone away
    2013,  # Lost connection to MySQL server during query
]


def close_old_connections():
    for conn in connections.all():
        conn.close_if_unusable_or_obsolete()


def should_reconnect(error):
    error_codes = getattr(settings, "DB_RECONNECT_ERROR_CODES", DEFAULT_ERROR_CODES)
    error_code = error.args[0]

    if error_code in error_codes:
        logger.warning(
            "Database connection lost (code: %s). Attempting to reconnect.", error_code
        )
        return True
    return False


def ensure_db_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except OperationalError as e:
            if should_reconnect(e):
                close_old_connections()
                return func(*args, **kwargs)
            else:
                raise

    return wrapper


source_mapping = {}
metainfo_mapping = {}

functions = pathlib.Path("data/functions.lst").read_text().splitlines()


@ensure_db_connection
def fetch_objects_to_json(name, qs):
    file = f"/data/{name}.json"
    file = pathlib.Path(file)
    if not file.exists():
        data = serializers.serialize("json", qs)
        file.write_text(data)
    return json.loads(file.read_text())


@ensure_db_connection
def fetch_ampels():
    file = pathlib.Path("/data/ampels.json")
    if not file.exists():
        data = {}
        for a in ApisAmpelAmpeltemp.objects.using("old").all():
            data[a.pk] = {"status": a.status, "note": a.note, "tempentity_id": a.temp_entity_id}
        file.write_text(json.dumps(data))
    return json.loads(file.read_text())


@ensure_db_connection
def fetch_vocabs():
    vocabs_file = "/data/vocabs.json"
    data_file = pathlib.Path(vocabs_file)
    if not data_file.exists():
        data = serializers.serialize(
            "json", ApisVocabulariesVocabsbaseclass.objects.using("old").all()
        )
        data = json.loads(data)
        data = {item["pk"]: item["fields"] for item in data}
        data_file.write_text(json.dumps(data))
    return json.loads(data_file.read_text())


@ensure_db_connection
def fetch_person_texts(person_ids=list[int]):
    person_texts_file = "/data/person_texts.json"
    data_file = pathlib.Path(person_texts_file)
    data = defaultdict(dict)
    if not data_file.exists():
        print("fetching person texts ...")
        text_types_names = ["Diverses", "Ereignis-Datum", "Quellenzitat"]
        text_types = ApisVocabulariesTexttype.objects.using("old").prefetch_related(
            "vocabsbaseclass_ptr"
        )
        text_types = text_types.filter(vocabsbaseclass_ptr__name__in=text_types_names)

        texts = ApisMetainfoTempentityclassText.objects.using("old").prefetch_related(
            "tempentityclass", "text"
        )
        texts = texts.filter(
            text__kind__in=text_types, tempentityclass__id__in=person_ids
        )
        texts = texts.exclude(text__text="").exclude(text__text__isnull=True)
        for text in texts:
            match text.text.kind.vocabsbaseclass_ptr.name:
                case "Diverses":
                    att = "diverses"
                case "Ereignis-Datum":
                    att = "ereignisdatum"
                case "Quellenzitat":
                    att = "quellenzitat"
            data[text.tempentityclass.pk][att] = text.text.text
        data_file.write_text(json.dumps(data, indent=2))
    return json.loads(data_file.read_text())


@ensure_db_connection
def fetch_person_labels(person_ids=list[int]):
    person_labels_file = "/data/person_labels.json"
    data_file = pathlib.Path(person_labels_file)
    data = defaultdict(dict)
    if not data_file.exists():
        print("fetching person labels ...")
        for label in (
            ApisLabelsLabel.objects.using("old")
            .prefetch_related("temp_entity")
            .filter(temp_entity__pk__in=person_ids)
        ):
            data[label.temp_entity.pk][label.label_type.vocabsbaseclass_ptr.name] = label.label
        data_file.write_text(json.dumps(data, indent=2))
    return json.loads(data_file.read_text())


@ensure_db_connection
def fetch_person_relations():
    person_relations_file = "/data/person_relation_merged_in.json"
    data_file = pathlib.Path(person_relations_file)
    data = {}
    if not data_file.exists():
        print("fetching person 'merged from' relations ...")
        for rel in (
            ApisRelationsPersonperson.objects.using("old")
            .prefetch_related("relation_type")
            .filter(
                relation_type__relationbaseclass_ptr__vocabsbaseclass_ptr__name="data merged from"
            )
        ):
            data[rel.related_persona.pk] = rel.related_personb.pk
        data_file.write_text(json.dumps(data, indent=2))
    return json.loads(data_file.read_text())


def apismetainfotempentityclass():
    data_file = pathlib.Path("/data/tempentityclass.json")
    if not data_file.exists():
        data = serializers.serialize(
            "json", ApisMetainfoTempentityclass.objects.using("old").all()
        )
        data = {k.get("pk"): k.get("fields") for k in json.loads(data)}
        data_file.write_text(json.dumps(data, indent=2))
    return json.loads(data_file.read_text())


tempentityclasses = apismetainfotempentityclass()


def set_tempentityclass_data(old, new):
    new.pk = old["pk"]
    te = tempentityclasses.get(str(new.pk))
    new.review = te["review"]
    new.references = te["references"]
    new.notes = te["notes"]
    new.published = te["published"]
    if source := te["source"]:
        source_mapping[source] = new


def objects_skips(obj):
    obj.skip_entity_id_creation = True
    obj.skip_history_when_saving = True
    obj.skip_date_interval_populate = True


def wrap_save(obj):
    objects_skips(obj)
    obj.save()


def persons():
    persons = Person.objects.all()
    print(f"Deleting {len(persons)} persons")
    persons._raw_delete(persons.db)
    content_type = ContentType.objects.get_for_model(Person)

    person_ids = ApisEntitiesPerson.objects.using("old").all().values_list("pk", flat=True)
    texts = fetch_person_texts(person_ids)
    labels = fetch_person_labels(person_ids)
    fetch_person_relations()

    object_list = []
    qs = ApisEntitiesPerson.objects.using("old").all()
    for old in fetch_objects_to_json("persons", qs):
        new = Person()
        set_tempentityclass_data(old, new)

        new.forename = old["fields"]["first_name"] or ""
        new.gender = old["fields"]["gender"] or ""

        te = tempentityclasses.get(str(new.pk))
        new.surname = te["name"] or ""
        new.date_of_birth = te["start_date_written"]
        new.date_of_death = te["end_date_written"]

        for att, text in texts.get(new.id, {}).items():
            setattr(new, att, text)
        for name, label in labels.get(new.id, {}).items():
            if new.labels:
                new.labels[name] = label
            else:
                new.label = {name: label}

        if new.id in fetch_person_relations().keys():
            new.mergedinto = fetch_person_relations()[new.id]

        objects_skips(new)

        metainfo_mapping[new.pk] = content_type.pk
        object_list.append(new)
    persons = Person.objects.bulk_create(object_list, batch_size=1000)
    print(f"Created {len(persons)} persons")
    object_list.clear()


def institutions():
    institutions = Institution.objects.all()
    print(f"Deleting {len(institutions)} institutions")
    institutions._raw_delete(institutions.db)
    content_type = ContentType.objects.get_for_model(Institution)

    object_list = []
    qs = ApisEntitiesInstitution.objects.using("old").all()
    for old in fetch_objects_to_json("institutions", qs):
        new = Institution()
        set_tempentityclass_data(old, new)
        te = tempentityclasses.get(str(new.pk))
        new.label = te["name"]
        new.start = te["start_date_written"]
        new.end = te["end_date_written"]
        new.status = te["status"]

        if kind := old.get("kind"):
            new.type = fetch_vocabs()[kind]

        objects_skips(new)

        metainfo_mapping[new.pk] = content_type.pk
        object_list.append(new)
    institutions = Institution.objects.bulk_create(object_list, batch_size=1000)
    print(f"Created {len(institutions)} institutions")


def events():
    events = Event.objects.all()
    print(f"Deleting {len(events)} events")
    events._raw_delete(events.db)
    content_type = ContentType.objects.get_for_model(Event)

    object_list = []
    qs = ApisEntitiesEvent.objects.using("old").all()
    for old in fetch_objects_to_json("events", qs):
        new = Event()
        set_tempentityclass_data(old, new)
        te = tempentityclasses.get(str(new.pk))
        new.name = te["name"]
        new.start = te["start_date_written"]
        new.end = te["end_date_written"]
        new.status = te["status"]

        objects_skips(new)

        metainfo_mapping[new.pk] = content_type.pk
        object_list.append(new)
    events = Event.objects.bulk_create(object_list, batch_size=1000)
    print(f"Created {len(events)} events")


def places():
    places = Place.objects.all()
    print(f"Deleting {len(places)} places")
    places._raw_delete(places.db)
    content_type = ContentType.objects.get_for_model(Place)

    object_list = []
    qs = ApisEntitiesPlace.objects.using("old").all()
    for old in fetch_objects_to_json("places", qs):
        new = Place()
        set_tempentityclass_data(old, new)
        te = tempentityclasses.get(str(new.pk))
        new.label = te["name"]
        if kind := old.get("kind"):
            new.kind = fetch_vocabs()[kind]
        new.start = te["start_date_written"]
        new.end = te["end_date_written"]
        new.status = te["status"]

        objects_skips(new)

        metainfo_mapping[new.pk] = content_type.pk
        object_list.append(new)
    places = Place.objects.bulk_create(object_list, batch_size=1000)
    print(f"Created {len(places)} places")


def sources():
    sources = Source.objects.all()
    print(f"Deleting {len(sources)} sources")
    sources._raw_delete(sources.db)

    object_list = []
    qs = ApisMetainfoSource.objects.using("old").filter(pk__in=source_mapping.keys())
    for old in fetch_objects_to_json("sources", qs):
        new = Source()
        new.pk = old["pk"]
        new.orig_filename = old["fields"]["orig_filename"]
        new.indexed = old["fields"]["indexed"]
        new.pubinfo = old["fields"]["pubinfo"]
        new.author = old["fields"]["author"]
        new.orig_id = old["fields"]["orig_id"]

        new.object_id = source_mapping[old["pk"]].pk
        new.content_type = ContentType.objects.get_for_model(source_mapping[old["pk"]])

        objects_skips(new)
        object_list.append(new)
    sources = Source.objects.bulk_create(object_list, batch_size=1000)
    print(f"Created {len(sources)} sources")


@ensure_db_connection
def collections():
    for old in (
        ApisMetainfoTempentityclassCollection.objects.using("old")
        .prefetch_related("tempentityclass", "collection")
        .all()
    ):
        print(old)
        sc, _ = SkosCollection.objects.get_or_create(name=old.collection.name)
        if old.tempentityclass.pk in metainfo_mapping.keys():
            content_type_id = metainfo_mapping[old.tempentityclass.pk]
            instance = ContentType.objects.get(
                pk=content_type_id
            ).get_object_for_this_type(pk=old.tempentityclass.pk)
            sc.add(instance)


def ampel():
    ampels = Ampel.objects.all()
    print(f"Deleting {len(ampels)} ampels")
    ampels._raw_delete(ampels.db)

    object_list = []
    for id, old in fetch_ampels().items():
        new = Ampel()
        new.pk = id
        new.status = old["status"]
        new.note = old["note"]
        new.object_id = old["tempentity_id"]
        new.content_type_id = metainfo_mapping[old["tempentity_id"]]
        objects_skips(new)
        object_list.append(new)
    ampels = Ampel.objects.bulk_create(object_list, batch_size=1000)
    print(f"Created {len(ampels)} ampels")


def oldrelation2newrelation_attrs(old, new, subject_pk, object_pk):
    new.pk = old.pk
    new.subj_object_id = subject_pk
    new.subj_content_type_id = metainfo_mapping[subject_pk]
    new.obj_object_id = object_pk
    new.obj_content_type_id = metainfo_mapping[object_pk]
    pks = str(old.pk)
    new.label = tempentityclasses[pks]["name"]
    new.start = tempentityclasses[pks]["start_date_written"]
    new.end = tempentityclasses[pks]["end_date_written"]
    new.review = tempentityclasses[pks]["review"]
    new.status = tempentityclasses[pks]["status"]
    new.references = tempentityclasses[pks]["references"]
    new.notes = tempentityclasses[pks]["notes"]
    if hasattr(new, "legacy_relation_vocab_label"):
        new.legacy_relation_vocab_label = (
            old.relation_type.relationbaseclass_ptr.vocabsbaseclass_ptr.name
        )
    if hasattr(new, "legacy_relation_vocab_label_reverse"):
        new.legacy_relation_vocab_label_reverse = (
            old.relation_type.relationbaseclass_ptr.name_reverse
        )
    if old.tempentityclass_ptr.source:
        source_mapping[old.tempentityclass_ptr.source.pk] = new


def oldrelation2newrelation(qs, newtype, subject_pk_name, object_pk_name):
    content_type = ContentType.objects.get_for_model(newtype)
    object_list = []
    for old in qs:
        new = newtype()
        subject = getattr(old, subject_pk_name)
        object = getattr(old, object_pk_name)
        oldrelation2newrelation_attrs(old, new, subject.pk, object.pk)
        metainfo_mapping[new.pk] = content_type.pk
        object_list.append(new)
    for obj in object_list:
        wrap_save(obj)
    print(f"Created {len(object_list)} {newtype} relations")


#@ensure_db_connection
#def fetch_relation(name, qs, subject_pk_name, object_pk_name):
#    filename = f"/data/{name}.json"
#    file = pathlib.Path(filename)
#    if not file.exists():
#        objects = []
#        for old in qs:
#            te = tempentityclasses[old.pk]
#            obj = {}
#            obj["label"] = te["name"]
#            obj["start"] = te["start_date_written"]
#            obj["end"] = te["end_date_written"]
#            obj["review"] = te["review"]
#            obj["status"] = te["status"]
#            obj["references"] = te["references"]
#            obj["notes"] = te["notes"]
#            obj["subject_pk"] = getattr(old, subject_pk_name)
#            obj["object_pk"] = getattr(old, object_pk_name)
#            obj["legacy_relation_vocab_label"] = old.relation_type.relationbaseclass_ptr.vocabsbaseclass_ptr.name
#            obj["legacy_relation_vocab_label_reverse"] = old.relation_type.relationbaseclass_ptr.name_reverse
#            if old.tempentityclass_ptr.source:
#                obj["source_mapping"] = old.tempentityclass_ptr.source.pk
#            objects.append(obj)
#        file.write_text(json.dumps(objects, indent=2))
#    return json.loads(file.read_text())


@ensure_db_connection
def relations():
    qs = ApisRelationsInstitutioninstitution.objects.using("old").prefetch_related("relation_type")
    #ii_rel = fetch_relation("institutioninstitution", qs, "related_institutiona", "related_institutionb")
    #for rel in ii_rel:
    #    source_mapping_pk = rel.pop("source_mapping", None)
    #    new = InstitutionInstitutionRelation(*rel)
    #    if source_mapping_pk:
    #        source_mapping[source_mapping_pk] = new
    #    wrap_save(new)
    oldrelation2newrelation(
        qs,
        InstitutionInstitutionRelation,
        "related_institutiona",
        "related_institutionb",
    )

    qs = ApisRelationsInstitutionplace.objects.using("old").prefetch_related(
        "tempentityclass_ptr", "relation_type"
    )
    oldrelation2newrelation(
        qs, InstitutionPlaceRelation, "related_institution", "related_place"
    )

    qs = ApisRelationsPersonevent.objects.using("old").prefetch_related(
        "tempentityclass_ptr", "relation_type"
    )
    oldrelation2newrelation(qs, PersonEventRelation, "related_person", "related_event")

    qs = ApisRelationsPersonperson.objects.using("old").prefetch_related(
        "tempentityclass_ptr", "relation_type"
    )
    oldrelation2newrelation(
        qs, PersonPersonRelation, "related_persona", "related_personb"
    )

    qs = ApisRelationsPersonplace.objects.using("old").prefetch_related(
        "tempentityclass_ptr", "relation_type"
    )
    oldrelation2newrelation(qs, PersonPlaceRelation, "related_person", "related_place")

    qs = ApisRelationsPlaceevent.objects.using("old").prefetch_related(
        "tempentityclass_ptr", "relation_type"
    )
    oldrelation2newrelation(qs, PlaceEventRelation, "related_place", "related_event")

    qs = ApisRelationsPlaceplace.objects.using("old").prefetch_related(
        "tempentityclass_ptr", "relation_type"
    )
    oldrelation2newrelation(qs, PlacePlaceRelation, "related_placea", "related_placeb")

    # special handling: convert to HasFunction
    for old in ApisRelationsPersoninstitution.objects.using("old").prefetch_related(
        "tempentityclass_ptr", "relation_type"
    ):
        print(old)
        name = old.relation_type.relationbaseclass_ptr.vocabsbaseclass_ptr.name
        if name.strip() in [function.strip() for function in functions]:
            ft, _ = FunctionType.objects.get_or_create(label=name)
            new = HasFunction()
            new.type = ft
        else:
            new = PersonInstitutionRelation()
        oldrelation2newrelation_attrs(
            old, new, old.related_person.pk, old.related_institution.pk
        )
        wrap_save(new)
        content_type = ContentType.objects.get_for_model(new)
        metainfo_mapping[new.pk] = content_type.pk


@ensure_db_connection
def bibsonomy():
    references = Reference.objects.all()
    print(f"Deleting {len(references)} references")
    references._raw_delete(references.db)

    qs = ApisBibsonomyReference.objects.using("old").all()
    object_list = []
    for old in fetch_objects_to_json("bibsonomy", qs):
        content_type_id = old["fields"].pop("content_type")
        new = Reference(**old["fields"])
        new.content_type_id = content_type_id
        if old["fields"]["object_id"] in metainfo_mapping.keys():
            new.content_type_id = metainfo_mapping[old["fields"]["object_id"]]
        objects_skips(new)
        object_list.append(new)
    references = Reference.objects.bulk_create(object_list, batch_size=1000)
    print(f"Created {len(references)} references")


fetch_vocabs()
persons()
institutions()
events()
places()
relations()
collections()
ampel()
sources()
bibsonomy()
