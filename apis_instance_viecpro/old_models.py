# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class ApisAmpelAmpelsettings(models.Model):
    active = models.IntegerField()
    content_type = models.ForeignKey("DjangoContentType", models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "apis_ampel_ampelsettings"


class ApisAmpelAmpeltemp(models.Model):
    status = models.CharField(max_length=300)
    note = models.TextField(blank=True, null=True)
    temp_entity = models.OneToOneField(
        "ApisMetainfoTempentityclass", models.DO_NOTHING, primary_key=True
    )

    class Meta:
        managed = False
        db_table = "apis_ampel_ampeltemp"


class ApisBibsonomyReference(models.Model):
    bibs_url = models.CharField(max_length=200)
    pages_start = models.PositiveIntegerField(blank=True, null=True)
    pages_end = models.PositiveIntegerField(blank=True, null=True)
    bibtex = models.TextField(blank=True, null=True)
    object_id = models.PositiveIntegerField()
    attribute = models.CharField(max_length=255, blank=True, null=True)
    last_update = models.DateTimeField()
    content_type = models.ForeignKey("DjangoContentType", models.DO_NOTHING)
    folio = models.CharField(max_length=255, blank=True, null=True)
    notes = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "apis_bibsonomy_reference"


class ApisEntitiesEvent(models.Model):
    tempentityclass_ptr = models.OneToOneField(
        "ApisMetainfoTempentityclass", models.DO_NOTHING, primary_key=True
    )
    kind = models.ForeignKey(
        "ApisVocabulariesEventtype", models.DO_NOTHING, blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "apis_entities_event"


class ApisEntitiesInstitution(models.Model):
    tempentityclass_ptr = models.OneToOneField(
        "ApisMetainfoTempentityclass", models.DO_NOTHING, primary_key=True
    )
    kind = models.ForeignKey(
        "ApisVocabulariesInstitutiontype", models.DO_NOTHING, blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "apis_entities_institution"


class ApisEntitiesPerson(models.Model):
    tempentityclass_ptr = models.OneToOneField(
        "ApisMetainfoTempentityclass", models.DO_NOTHING, primary_key=True
    )
    first_name = models.CharField(max_length=255, blank=True, null=True)
    gender = models.CharField(max_length=15, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "apis_entities_person"


class ApisEntitiesPersonProfession(models.Model):
    person = models.ForeignKey(ApisEntitiesPerson, models.DO_NOTHING)
    professiontype = models.ForeignKey(
        "ApisVocabulariesProfessiontype", models.DO_NOTHING
    )

    class Meta:
        managed = False
        db_table = "apis_entities_person_profession"
        unique_together = (("person", "professiontype"),)


class ApisEntitiesPersonTitle(models.Model):
    person = models.ForeignKey(ApisEntitiesPerson, models.DO_NOTHING)
    title = models.ForeignKey("ApisVocabulariesTitle", models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "apis_entities_person_title"
        unique_together = (("person", "title"),)


class ApisEntitiesPlace(models.Model):
    tempentityclass_ptr = models.OneToOneField(
        "ApisMetainfoTempentityclass", models.DO_NOTHING, primary_key=True
    )
    lat = models.FloatField(blank=True, null=True)
    lng = models.FloatField(blank=True, null=True)
    kind = models.ForeignKey(
        "ApisVocabulariesPlacetype", models.DO_NOTHING, blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "apis_entities_place"


class ApisEntitiesWork(models.Model):
    tempentityclass_ptr = models.OneToOneField(
        "ApisMetainfoTempentityclass", models.DO_NOTHING, primary_key=True
    )
    kind = models.ForeignKey(
        "ApisVocabulariesWorktype", models.DO_NOTHING, blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "apis_entities_work"


class ApisImportProjectDatasource(models.Model):
    name = models.CharField(max_length=255)
    server_directory = models.CharField(max_length=255)
    page_count = models.IntegerField(blank=True, null=True)
    citation = models.TextField(blank=True, null=True)
    year = models.CharField(max_length=10)
    owner = models.ForeignKey("AuthUser", models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "apis_import_project_datasource"


class ApisImportProjectDatasourcepage(models.Model):
    page_index = models.IntegerField()
    page_token = models.CharField(max_length=20, blank=True, null=True)
    datasource = models.ForeignKey(
        ApisImportProjectDatasource, models.DO_NOTHING, db_column="DataSource_id"
    )  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = "apis_import_project_datasourcepage"


class ApisImportProjectDatasourceprojectstate(models.Model):
    datasource = models.ForeignKey(
        ApisImportProjectDatasource, models.DO_NOTHING, blank=True, null=True
    )
    last_page = models.ForeignKey(
        ApisImportProjectDatasourcepage, models.DO_NOTHING, blank=True, null=True
    )
    project = models.ForeignKey(
        "ApisImportProjectImportproject", models.DO_NOTHING, blank=True, null=True
    )
    user = models.ForeignKey("AuthUser", models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "apis_import_project_datasourceprojectstate"


class ApisImportProjectGenericcollectionentry(models.Model):
    content_type = models.ForeignKey("DjangoContentType", models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "apis_import_project_genericcollectionentry"


class ApisImportProjectImportproject(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    collection = models.ForeignKey(
        "ApisMetainfoCollection", models.DO_NOTHING, blank=True, null=True
    )
    owner = models.ForeignKey("AuthUser", models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "apis_import_project_importproject"


class ApisImportProjectImportprojectDatasources(models.Model):
    importproject = models.ForeignKey(ApisImportProjectImportproject, models.DO_NOTHING)
    datasource = models.ForeignKey(ApisImportProjectDatasource, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "apis_import_project_importproject_DataSources"
        unique_together = (("importproject", "datasource"),)


class ApisImportProjectImportprojectEditors(models.Model):
    importproject = models.ForeignKey(ApisImportProjectImportproject, models.DO_NOTHING)
    user = models.ForeignKey("AuthUser", models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "apis_import_project_importproject_Editors"
        unique_together = (("importproject", "user"),)


class ApisImportProjectPagecollection(models.Model):
    class Meta:
        managed = False
        db_table = "apis_import_project_pagecollection"


class ApisImportProjectPagecollectionCreatedIn(models.Model):
    pagecollection = models.ForeignKey(
        ApisImportProjectPagecollection, models.DO_NOTHING
    )
    genericcollectionentry = models.ForeignKey(
        ApisImportProjectGenericcollectionentry, models.DO_NOTHING
    )

    class Meta:
        managed = False
        db_table = "apis_import_project_pagecollection_created_in"
        unique_together = (("pagecollection", "genericcollectionentry"),)


class ApisImportProjectPagecollectionEditedIn(models.Model):
    pagecollection = models.ForeignKey(
        ApisImportProjectPagecollection, models.DO_NOTHING
    )
    genericcollectionentry = models.ForeignKey(
        ApisImportProjectGenericcollectionentry, models.DO_NOTHING
    )

    class Meta:
        managed = False
        db_table = "apis_import_project_pagecollection_edited_in"
        unique_together = (("pagecollection", "genericcollectionentry"),)


class ApisImportProjectPagedata(models.Model):
    collection = models.OneToOneField(
        ApisImportProjectPagecollection, models.DO_NOTHING, blank=True, null=True
    )
    function = models.ForeignKey(
        "ApisVocabulariesPersoninstitutionrelation",
        models.DO_NOTHING,
        blank=True,
        null=True,
    )
    institution = models.ForeignKey(
        ApisEntitiesInstitution, models.DO_NOTHING, blank=True, null=True
    )
    page = models.ForeignKey(ApisImportProjectDatasourcepage, models.DO_NOTHING)
    project = models.ForeignKey(ApisImportProjectImportproject, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "apis_import_project_pagedata"


class ApisImportProjectProjectcollectionentry(models.Model):
    json = models.TextField()
    entry = models.ForeignKey(
        ApisImportProjectGenericcollectionentry, models.DO_NOTHING
    )
    project = models.ForeignKey(
        ApisImportProjectImportproject, models.DO_NOTHING, blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "apis_import_project_projectcollectionentry"


class ApisImportProjectProjectstate(models.Model):
    last_datasource = models.ForeignKey(
        ApisImportProjectDatasource, models.DO_NOTHING, blank=True, null=True
    )
    project = models.ForeignKey(ApisImportProjectImportproject, models.DO_NOTHING)
    user = models.ForeignKey("AuthUser", models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "apis_import_project_projectstate"


class ApisLabelsLabel(models.Model):
    label = models.CharField(max_length=255)
    isocode_639_3 = models.CharField(
        db_column="isoCode_639_3", max_length=3, blank=True, null=True
    )  # Field name made lowercase.
    label_type = models.ForeignKey(
        "ApisVocabulariesLabeltype", models.DO_NOTHING, blank=True, null=True
    )
    temp_entity = models.ForeignKey("ApisMetainfoTempentityclass", models.DO_NOTHING)
    end_date = models.DateField(blank=True, null=True)
    end_date_written = models.CharField(max_length=255, blank=True, null=True)
    end_end_date = models.DateField(blank=True, null=True)
    end_start_date = models.DateField(blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    start_date_written = models.CharField(max_length=255, blank=True, null=True)
    start_end_date = models.DateField(blank=True, null=True)
    start_start_date = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "apis_labels_label"


class ApisMetainfoCollection(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    collection_type = models.ForeignKey(
        "ApisVocabulariesCollectiontype", models.DO_NOTHING, blank=True, null=True
    )
    parent_class = models.ForeignKey("self", models.DO_NOTHING, blank=True, null=True)
    published = models.IntegerField()

    class Meta:
        managed = False
        db_table = "apis_metainfo_collection"


class ApisMetainfoCollectionGroupsAllowed(models.Model):
    collection = models.ForeignKey(ApisMetainfoCollection, models.DO_NOTHING)
    group = models.ForeignKey("AuthGroup", models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "apis_metainfo_collection_groups_allowed"
        unique_together = (("collection", "group"),)


class ApisMetainfoSource(models.Model):
    orig_filename = models.CharField(max_length=255)
    indexed = models.IntegerField()
    pubinfo = models.CharField(max_length=400)
    author = models.CharField(max_length=255)
    orig_id = models.PositiveIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "apis_metainfo_source"


class ApisMetainfoTempentityclass(models.Model):
    name = models.CharField(max_length=255)
    review = models.IntegerField()
    start_date = models.DateField(blank=True, null=True)
    start_start_date = models.DateField(blank=True, null=True)
    start_end_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    end_start_date = models.DateField(blank=True, null=True)
    end_end_date = models.DateField(blank=True, null=True)
    start_date_written = models.CharField(max_length=255, blank=True, null=True)
    end_date_written = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=100)
    references = models.TextField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    source = models.ForeignKey(
        ApisMetainfoSource, models.DO_NOTHING, blank=True, null=True
    )
    published = models.IntegerField()

    class Meta:
        managed = False
        db_table = "apis_metainfo_tempentityclass"


class ApisMetainfoTempentityclassCollection(models.Model):
    tempentityclass = models.ForeignKey(ApisMetainfoTempentityclass, models.DO_NOTHING)
    collection = models.ForeignKey(ApisMetainfoCollection, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "apis_metainfo_tempentityclass_collection"
        unique_together = (("tempentityclass", "collection"),)


class ApisMetainfoTempentityclassText(models.Model):
    tempentityclass = models.ForeignKey(ApisMetainfoTempentityclass, models.DO_NOTHING)
    text = models.ForeignKey("ApisMetainfoText", models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "apis_metainfo_tempentityclass_text"
        unique_together = (("tempentityclass", "text"),)


class ApisMetainfoText(models.Model):
    text = models.TextField()
    kind = models.ForeignKey(
        "ApisVocabulariesTexttype", models.DO_NOTHING, blank=True, null=True
    )
    source = models.ForeignKey(
        ApisMetainfoSource, models.DO_NOTHING, blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "apis_metainfo_text"


class ApisMetainfoUri(models.Model):
    uri = models.CharField(unique=True, max_length=255, blank=True, null=True)
    domain = models.CharField(max_length=255)
    rdf_link = models.CharField(max_length=200)
    loaded = models.IntegerField()
    loaded_time = models.DateTimeField(blank=True, null=True)
    entity = models.ForeignKey(
        ApisMetainfoTempentityclass, models.DO_NOTHING, blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "apis_metainfo_uri"


class ApisMetainfoUricandidate(models.Model):
    uri = models.CharField(max_length=200)
    confidence = models.FloatField(blank=True, null=True)
    responsible = models.CharField(max_length=255)
    entity = models.ForeignKey(
        ApisMetainfoTempentityclass, models.DO_NOTHING, blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "apis_metainfo_uricandidate"


class ApisRelationsEventevent(models.Model):
    tempentityclass_ptr = models.OneToOneField(
        ApisMetainfoTempentityclass, models.DO_NOTHING, primary_key=True
    )
    related_eventa = models.ForeignKey(
        ApisEntitiesEvent,
        models.DO_NOTHING,
        db_column="related_eventA_id",
        blank=True,
        null=True,
    )  # Field name made lowercase.
    related_eventb = models.ForeignKey(
        ApisEntitiesEvent,
        models.DO_NOTHING,
        db_column="related_eventB_id",
        related_name="apisrelationseventevent_related_eventb_set",
        blank=True,
        null=True,
    )  # Field name made lowercase.
    relation_type = models.ForeignKey(
        "ApisVocabulariesEventeventrelation", models.DO_NOTHING, blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "apis_relations_eventevent"


class ApisRelationsEventwork(models.Model):
    tempentityclass_ptr = models.OneToOneField(
        ApisMetainfoTempentityclass, models.DO_NOTHING, primary_key=True
    )
    related_event = models.ForeignKey(
        ApisEntitiesEvent, models.DO_NOTHING, blank=True, null=True
    )
    related_work = models.ForeignKey(
        ApisEntitiesWork, models.DO_NOTHING, blank=True, null=True
    )
    relation_type = models.ForeignKey(
        "ApisVocabulariesEventworkrelation", models.DO_NOTHING, blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "apis_relations_eventwork"


class ApisRelationsInstitutionevent(models.Model):
    tempentityclass_ptr = models.OneToOneField(
        ApisMetainfoTempentityclass, models.DO_NOTHING, primary_key=True
    )
    related_event = models.ForeignKey(
        ApisEntitiesEvent, models.DO_NOTHING, blank=True, null=True
    )
    related_institution = models.ForeignKey(
        ApisEntitiesInstitution, models.DO_NOTHING, blank=True, null=True
    )
    relation_type = models.ForeignKey(
        "ApisVocabulariesInstitutioneventrelation",
        models.DO_NOTHING,
        blank=True,
        null=True,
    )

    class Meta:
        managed = False
        db_table = "apis_relations_institutionevent"


class ApisRelationsInstitutioninstitution(models.Model):
    tempentityclass_ptr = models.OneToOneField(
        ApisMetainfoTempentityclass, models.DO_NOTHING, primary_key=True
    )
    related_institutiona = models.ForeignKey(
        ApisEntitiesInstitution,
        models.DO_NOTHING,
        db_column="related_institutionA_id",
        blank=True,
        null=True,
    )  # Field name made lowercase.
    related_institutionb = models.ForeignKey(
        ApisEntitiesInstitution,
        models.DO_NOTHING,
        db_column="related_institutionB_id",
        related_name="apisrelationsinstitutioninstitution_related_institutionb_set",
        blank=True,
        null=True,
    )  # Field name made lowercase.
    relation_type = models.ForeignKey(
        "ApisVocabulariesInstitutioninstitutionrelation",
        models.DO_NOTHING,
        blank=True,
        null=True,
    )

    class Meta:
        managed = False
        db_table = "apis_relations_institutioninstitution"


class ApisRelationsInstitutionplace(models.Model):
    tempentityclass_ptr = models.OneToOneField(
        ApisMetainfoTempentityclass, models.DO_NOTHING, primary_key=True
    )
    related_institution = models.ForeignKey(
        ApisEntitiesInstitution, models.DO_NOTHING, blank=True, null=True
    )
    related_place = models.ForeignKey(
        ApisEntitiesPlace, models.DO_NOTHING, blank=True, null=True
    )
    relation_type = models.ForeignKey(
        "ApisVocabulariesInstitutionplacerelation",
        models.DO_NOTHING,
        blank=True,
        null=True,
    )

    class Meta:
        managed = False
        db_table = "apis_relations_institutionplace"


class ApisRelationsInstitutionwork(models.Model):
    tempentityclass_ptr = models.OneToOneField(
        ApisMetainfoTempentityclass, models.DO_NOTHING, primary_key=True
    )
    related_institution = models.ForeignKey(
        ApisEntitiesInstitution, models.DO_NOTHING, blank=True, null=True
    )
    related_work = models.ForeignKey(
        ApisEntitiesWork, models.DO_NOTHING, blank=True, null=True
    )
    relation_type = models.ForeignKey(
        "ApisVocabulariesInstitutionworkrelation",
        models.DO_NOTHING,
        blank=True,
        null=True,
    )

    class Meta:
        managed = False
        db_table = "apis_relations_institutionwork"


class ApisRelationsPersonevent(models.Model):
    tempentityclass_ptr = models.OneToOneField(
        ApisMetainfoTempentityclass, models.DO_NOTHING, primary_key=True
    )
    related_event = models.ForeignKey(
        ApisEntitiesEvent, models.DO_NOTHING, blank=True, null=True
    )
    related_person = models.ForeignKey(
        ApisEntitiesPerson, models.DO_NOTHING, blank=True, null=True
    )
    relation_type = models.ForeignKey(
        "ApisVocabulariesPersoneventrelation", models.DO_NOTHING, blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "apis_relations_personevent"


class ApisRelationsPersoninstitution(models.Model):
    tempentityclass_ptr = models.OneToOneField(
        ApisMetainfoTempentityclass, models.DO_NOTHING, primary_key=True
    )
    related_institution = models.ForeignKey(
        ApisEntitiesInstitution, models.DO_NOTHING, blank=True, null=True
    )
    related_person = models.ForeignKey(
        ApisEntitiesPerson, models.DO_NOTHING, blank=True, null=True
    )
    relation_type = models.ForeignKey(
        "ApisVocabulariesPersoninstitutionrelation",
        models.DO_NOTHING,
        blank=True,
        null=True,
    )

    class Meta:
        managed = False
        db_table = "apis_relations_personinstitution"


class ApisRelationsPersonperson(models.Model):
    tempentityclass_ptr = models.OneToOneField(
        ApisMetainfoTempentityclass, models.DO_NOTHING, primary_key=True
    )
    related_persona = models.ForeignKey(
        ApisEntitiesPerson,
        models.DO_NOTHING,
        db_column="related_personA_id",
        blank=True,
        null=True,
    )  # Field name made lowercase.
    related_personb = models.ForeignKey(
        ApisEntitiesPerson,
        models.DO_NOTHING,
        db_column="related_personB_id",
        related_name="apisrelationspersonperson_related_personb_set",
        blank=True,
        null=True,
    )  # Field name made lowercase.
    relation_type = models.ForeignKey(
        "ApisVocabulariesPersonpersonrelation", models.DO_NOTHING, blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "apis_relations_personperson"


class ApisRelationsPersonplace(models.Model):
    tempentityclass_ptr = models.OneToOneField(
        ApisMetainfoTempentityclass, models.DO_NOTHING, primary_key=True
    )
    related_person = models.ForeignKey(
        ApisEntitiesPerson, models.DO_NOTHING, blank=True, null=True
    )
    related_place = models.ForeignKey(
        ApisEntitiesPlace, models.DO_NOTHING, blank=True, null=True
    )
    relation_type = models.ForeignKey(
        "ApisVocabulariesPersonplacerelation", models.DO_NOTHING, blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "apis_relations_personplace"


class ApisRelationsPersonwork(models.Model):
    tempentityclass_ptr = models.OneToOneField(
        ApisMetainfoTempentityclass, models.DO_NOTHING, primary_key=True
    )
    related_person = models.ForeignKey(
        ApisEntitiesPerson, models.DO_NOTHING, blank=True, null=True
    )
    related_work = models.ForeignKey(
        ApisEntitiesWork, models.DO_NOTHING, blank=True, null=True
    )
    relation_type = models.ForeignKey(
        "ApisVocabulariesPersonworkrelation", models.DO_NOTHING, blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "apis_relations_personwork"


class ApisRelationsPlaceevent(models.Model):
    tempentityclass_ptr = models.OneToOneField(
        ApisMetainfoTempentityclass, models.DO_NOTHING, primary_key=True
    )
    related_event = models.ForeignKey(
        ApisEntitiesEvent, models.DO_NOTHING, blank=True, null=True
    )
    related_place = models.ForeignKey(
        ApisEntitiesPlace, models.DO_NOTHING, blank=True, null=True
    )
    relation_type = models.ForeignKey(
        "ApisVocabulariesPlaceeventrelation", models.DO_NOTHING, blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "apis_relations_placeevent"


class ApisRelationsPlaceplace(models.Model):
    tempentityclass_ptr = models.OneToOneField(
        ApisMetainfoTempentityclass, models.DO_NOTHING, primary_key=True
    )
    related_placea = models.ForeignKey(
        ApisEntitiesPlace,
        models.DO_NOTHING,
        db_column="related_placeA_id",
        blank=True,
        null=True,
    )  # Field name made lowercase.
    related_placeb = models.ForeignKey(
        ApisEntitiesPlace,
        models.DO_NOTHING,
        db_column="related_placeB_id",
        related_name="apisrelationsplaceplace_related_placeb_set",
        blank=True,
        null=True,
    )  # Field name made lowercase.
    relation_type = models.ForeignKey(
        "ApisVocabulariesPlaceplacerelation", models.DO_NOTHING, blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "apis_relations_placeplace"


class ApisRelationsPlacework(models.Model):
    tempentityclass_ptr = models.OneToOneField(
        ApisMetainfoTempentityclass, models.DO_NOTHING, primary_key=True
    )
    related_place = models.ForeignKey(
        ApisEntitiesPlace, models.DO_NOTHING, blank=True, null=True
    )
    related_work = models.ForeignKey(
        ApisEntitiesWork, models.DO_NOTHING, blank=True, null=True
    )
    relation_type = models.ForeignKey(
        "ApisVocabulariesPlaceworkrelation", models.DO_NOTHING, blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "apis_relations_placework"


class ApisRelationsWorkwork(models.Model):
    tempentityclass_ptr = models.OneToOneField(
        ApisMetainfoTempentityclass, models.DO_NOTHING, primary_key=True
    )
    related_worka = models.ForeignKey(
        ApisEntitiesWork,
        models.DO_NOTHING,
        db_column="related_workA_id",
        blank=True,
        null=True,
    )  # Field name made lowercase.
    related_workb = models.ForeignKey(
        ApisEntitiesWork,
        models.DO_NOTHING,
        db_column="related_workB_id",
        related_name="apisrelationsworkwork_related_workb_set",
        blank=True,
        null=True,
    )  # Field name made lowercase.
    relation_type = models.ForeignKey(
        "ApisVocabulariesWorkworkrelation", models.DO_NOTHING, blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "apis_relations_workwork"


class ApisVocabulariesCollectiontype(models.Model):
    vocabsbaseclass_ptr = models.OneToOneField(
        "ApisVocabulariesVocabsbaseclass", models.DO_NOTHING, primary_key=True
    )

    class Meta:
        managed = False
        db_table = "apis_vocabularies_collectiontype"


class ApisVocabulariesEventeventrelation(models.Model):
    relationbaseclass_ptr = models.OneToOneField(
        "ApisVocabulariesRelationbaseclass", models.DO_NOTHING, primary_key=True
    )

    class Meta:
        managed = False
        db_table = "apis_vocabularies_eventeventrelation"


class ApisVocabulariesEventtype(models.Model):
    vocabsbaseclass_ptr = models.OneToOneField(
        "ApisVocabulariesVocabsbaseclass", models.DO_NOTHING, primary_key=True
    )

    class Meta:
        managed = False
        db_table = "apis_vocabularies_eventtype"


class ApisVocabulariesEventworkrelation(models.Model):
    relationbaseclass_ptr = models.OneToOneField(
        "ApisVocabulariesRelationbaseclass", models.DO_NOTHING, primary_key=True
    )

    class Meta:
        managed = False
        db_table = "apis_vocabularies_eventworkrelation"


class ApisVocabulariesInstitutioneventrelation(models.Model):
    relationbaseclass_ptr = models.OneToOneField(
        "ApisVocabulariesRelationbaseclass", models.DO_NOTHING, primary_key=True
    )

    class Meta:
        managed = False
        db_table = "apis_vocabularies_institutioneventrelation"


class ApisVocabulariesInstitutioninstitutionrelation(models.Model):
    relationbaseclass_ptr = models.OneToOneField(
        "ApisVocabulariesRelationbaseclass", models.DO_NOTHING, primary_key=True
    )

    class Meta:
        managed = False
        db_table = "apis_vocabularies_institutioninstitutionrelation"


class ApisVocabulariesInstitutionplacerelation(models.Model):
    relationbaseclass_ptr = models.OneToOneField(
        "ApisVocabulariesRelationbaseclass", models.DO_NOTHING, primary_key=True
    )

    class Meta:
        managed = False
        db_table = "apis_vocabularies_institutionplacerelation"


class ApisVocabulariesInstitutiontype(models.Model):
    vocabsbaseclass_ptr = models.OneToOneField(
        "ApisVocabulariesVocabsbaseclass", models.DO_NOTHING, primary_key=True
    )

    class Meta:
        managed = False
        db_table = "apis_vocabularies_institutiontype"


class ApisVocabulariesInstitutionworkrelation(models.Model):
    relationbaseclass_ptr = models.OneToOneField(
        "ApisVocabulariesRelationbaseclass", models.DO_NOTHING, primary_key=True
    )

    class Meta:
        managed = False
        db_table = "apis_vocabularies_institutionworkrelation"


class ApisVocabulariesLabeltype(models.Model):
    vocabsbaseclass_ptr = models.OneToOneField(
        "ApisVocabulariesVocabsbaseclass", models.DO_NOTHING, primary_key=True
    )

    class Meta:
        managed = False
        db_table = "apis_vocabularies_labeltype"


class ApisVocabulariesPersoneventrelation(models.Model):
    relationbaseclass_ptr = models.OneToOneField(
        "ApisVocabulariesRelationbaseclass", models.DO_NOTHING, primary_key=True
    )

    class Meta:
        managed = False
        db_table = "apis_vocabularies_personeventrelation"


class ApisVocabulariesPersoninstitutionrelation(models.Model):
    relationbaseclass_ptr = models.OneToOneField(
        "ApisVocabulariesRelationbaseclass", models.DO_NOTHING, primary_key=True
    )

    class Meta:
        managed = False
        db_table = "apis_vocabularies_personinstitutionrelation"


class ApisVocabulariesPersonpersonrelation(models.Model):
    relationbaseclass_ptr = models.OneToOneField(
        "ApisVocabulariesRelationbaseclass", models.DO_NOTHING, primary_key=True
    )

    class Meta:
        managed = False
        db_table = "apis_vocabularies_personpersonrelation"


class ApisVocabulariesPersonplacerelation(models.Model):
    relationbaseclass_ptr = models.OneToOneField(
        "ApisVocabulariesRelationbaseclass", models.DO_NOTHING, primary_key=True
    )

    class Meta:
        managed = False
        db_table = "apis_vocabularies_personplacerelation"


class ApisVocabulariesPersonworkrelation(models.Model):
    relationbaseclass_ptr = models.OneToOneField(
        "ApisVocabulariesRelationbaseclass", models.DO_NOTHING, primary_key=True
    )

    class Meta:
        managed = False
        db_table = "apis_vocabularies_personworkrelation"


class ApisVocabulariesPlaceeventrelation(models.Model):
    relationbaseclass_ptr = models.OneToOneField(
        "ApisVocabulariesRelationbaseclass", models.DO_NOTHING, primary_key=True
    )

    class Meta:
        managed = False
        db_table = "apis_vocabularies_placeeventrelation"


class ApisVocabulariesPlaceplacerelation(models.Model):
    relationbaseclass_ptr = models.OneToOneField(
        "ApisVocabulariesRelationbaseclass", models.DO_NOTHING, primary_key=True
    )

    class Meta:
        managed = False
        db_table = "apis_vocabularies_placeplacerelation"


class ApisVocabulariesPlacetype(models.Model):
    vocabsbaseclass_ptr = models.OneToOneField(
        "ApisVocabulariesVocabsbaseclass", models.DO_NOTHING, primary_key=True
    )

    class Meta:
        managed = False
        db_table = "apis_vocabularies_placetype"


class ApisVocabulariesPlaceworkrelation(models.Model):
    relationbaseclass_ptr = models.OneToOneField(
        "ApisVocabulariesRelationbaseclass", models.DO_NOTHING, primary_key=True
    )

    class Meta:
        managed = False
        db_table = "apis_vocabularies_placeworkrelation"


class ApisVocabulariesProfessiontype(models.Model):
    vocabsbaseclass_ptr = models.OneToOneField(
        "ApisVocabulariesVocabsbaseclass", models.DO_NOTHING, primary_key=True
    )

    class Meta:
        managed = False
        db_table = "apis_vocabularies_professiontype"


class ApisVocabulariesRelationbaseclass(models.Model):
    vocabsbaseclass_ptr = models.OneToOneField(
        "ApisVocabulariesVocabsbaseclass", models.DO_NOTHING, primary_key=True
    )
    name_reverse = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = "apis_vocabularies_relationbaseclass"


class ApisVocabulariesTexttype(models.Model):
    vocabsbaseclass_ptr = models.OneToOneField(
        "ApisVocabulariesVocabsbaseclass", models.DO_NOTHING, primary_key=True
    )
    entity = models.CharField(max_length=255)
    lang = models.CharField(max_length=3, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "apis_vocabularies_texttype"


class ApisVocabulariesTexttypeCollections(models.Model):
    texttype = models.ForeignKey(ApisVocabulariesTexttype, models.DO_NOTHING)
    collection = models.ForeignKey(ApisMetainfoCollection, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "apis_vocabularies_texttype_collections"
        unique_together = (("texttype", "collection"),)


class ApisVocabulariesTitle(models.Model):
    vocabsbaseclass_ptr = models.OneToOneField(
        "ApisVocabulariesVocabsbaseclass", models.DO_NOTHING, primary_key=True
    )
    abbreviation = models.CharField(max_length=10)

    class Meta:
        managed = False
        db_table = "apis_vocabularies_title"


class ApisVocabulariesVocabnames(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = "apis_vocabularies_vocabnames"


class ApisVocabulariesVocabsbaseclass(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(max_length=4)
    parent_class = models.ForeignKey("self", models.DO_NOTHING, blank=True, null=True)
    useradded = models.ForeignKey(
        "AuthUser", models.DO_NOTHING, db_column="userAdded_id", blank=True, null=True
    )  # Field name made lowercase.
    vocab_name = models.ForeignKey(
        ApisVocabulariesVocabnames, models.DO_NOTHING, blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "apis_vocabularies_vocabsbaseclass"


class ApisVocabulariesVocabsuri(models.Model):
    uri = models.CharField(max_length=200)
    domain = models.CharField(max_length=255)
    rdf_link = models.CharField(max_length=200)
    loaded = models.IntegerField()
    loaded_time = models.DateTimeField(blank=True, null=True)
    vocab = models.ForeignKey(
        ApisVocabulariesVocabsbaseclass, models.DO_NOTHING, blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "apis_vocabularies_vocabsuri"


class ApisVocabulariesWorktype(models.Model):
    vocabsbaseclass_ptr = models.OneToOneField(
        ApisVocabulariesVocabsbaseclass, models.DO_NOTHING, primary_key=True
    )

    class Meta:
        managed = False
        db_table = "apis_vocabularies_worktype"


class ApisVocabulariesWorkworkrelation(models.Model):
    relationbaseclass_ptr = models.OneToOneField(
        ApisVocabulariesRelationbaseclass, models.DO_NOTHING, primary_key=True
    )

    class Meta:
        managed = False
        db_table = "apis_vocabularies_workworkrelation"


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = "auth_group"


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey("AuthPermission", models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "auth_group_permissions"
        unique_together = (("group", "permission"),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey("DjangoContentType", models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = "auth_permission"
        unique_together = (("content_type", "codename"),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = "auth_user"


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "auth_user_groups"
        unique_together = (("user", "group"),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "auth_user_user_permissions"
        unique_together = (("user", "permission"),)


class AuthtokenToken(models.Model):
    key = models.CharField(primary_key=True, max_length=40)
    created = models.DateTimeField()
    user = models.OneToOneField(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "authtoken_token"


class BrowsingBrowsconf(models.Model):
    model_name = models.CharField(max_length=255)
    label = models.CharField(max_length=255)
    field_path = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = "browsing_browsconf"


class ChartsChartconfig(models.Model):
    model_name = models.CharField(max_length=255)
    label = models.CharField(max_length=255)
    field_path = models.CharField(max_length=255)
    help_text = models.CharField(max_length=255)
    legend_x = models.CharField(max_length=255)
    legend_y = models.CharField(max_length=255)
    app_name = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = "charts_chartconfig"


class ChartsChartconfigChartTypes(models.Model):
    chartconfig = models.ForeignKey(ChartsChartconfig, models.DO_NOTHING)
    charttype = models.ForeignKey("ChartsCharttype", models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "charts_chartconfig_chart_types"
        unique_together = (("chartconfig", "charttype"),)


class ChartsCharttype(models.Model):
    name = models.CharField(max_length=255)
    icon = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = "charts_charttype"


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey(
        "DjangoContentType", models.DO_NOTHING, blank=True, null=True
    )
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "django_admin_log"


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = "django_content_type"
        unique_together = (("app_label", "model"),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = "django_migrations"


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = "django_session"


class DublettenToolDublettenlog(models.Model):
    msg = models.TextField()
    action = models.CharField(max_length=255)
    timestamp = models.DateTimeField()
    user = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "dubletten_tool_dublettenlog"


class DublettenToolGroup(models.Model):
    name = models.CharField(max_length=600)
    status = models.CharField(max_length=300)
    field_gender = models.CharField(
        db_column="_gender", max_length=255, blank=True, null=True
    )  # Field renamed because it started with '_'.
    marked = models.IntegerField()
    note = models.TextField(blank=True, null=True)
    vorfin = models.OneToOneField(
        ApisEntitiesPerson, models.DO_NOTHING, blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "dubletten_tool_group"


class DublettenToolGroupMembers(models.Model):
    group = models.ForeignKey(DublettenToolGroup, models.DO_NOTHING)
    personproxy = models.ForeignKey("DublettenToolPersonproxy", models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "dubletten_tool_group_members"
        unique_together = (("group", "personproxy"),)


class DublettenToolPersonproxy(models.Model):
    status = models.CharField(max_length=300)
    marked = models.IntegerField()
    note = models.TextField(blank=True, null=True)
    field_names = models.TextField(
        db_column="_names", db_collation="utf8mb4_bin", blank=True, null=True
    )  # Field renamed because it started with '_'.
    field_first_names = models.TextField(
        db_column="_first_names", db_collation="utf8mb4_bin", blank=True, null=True
    )  # Field renamed because it started with '_'.
    person = models.OneToOneField(ApisEntitiesPerson, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "dubletten_tool_personproxy"


class DublettenToolStatusbuttongroup(models.Model):
    value = models.IntegerField()
    kind = models.ForeignKey("DublettenToolStatusbuttongrouptype", models.DO_NOTHING)
    related_instance = models.ForeignKey(DublettenToolGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "dubletten_tool_statusbuttongroup"


class DublettenToolStatusbuttongrouptype(models.Model):
    name = models.CharField(max_length=600)
    short = models.CharField(max_length=4)

    class Meta:
        managed = False
        db_table = "dubletten_tool_statusbuttongrouptype"


class DublettenToolStatusbuttonproxy(models.Model):
    value = models.IntegerField()
    kind = models.ForeignKey("DublettenToolStatusbuttonproxytype", models.DO_NOTHING)
    related_instance = models.ForeignKey(DublettenToolPersonproxy, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "dubletten_tool_statusbuttonproxy"


class DublettenToolStatusbuttonproxytype(models.Model):
    name = models.CharField(max_length=600)

    class Meta:
        managed = False
        db_table = "dubletten_tool_statusbuttonproxytype"


class DublettenToolSuggestions(models.Model):
    data = models.TextField(db_collation="utf8mb4_bin", blank=True, null=True)

    class Meta:
        managed = False
        db_table = "dubletten_tool_suggestions"


class GuardianGroupobjectpermission(models.Model):
    object_pk = models.CharField(max_length=255)
    content_type = models.ForeignKey(DjangoContentType, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "guardian_groupobjectpermission"
        unique_together = (("group", "permission", "object_pk"),)


class GuardianUserobjectpermission(models.Model):
    object_pk = models.CharField(max_length=255)
    content_type = models.ForeignKey(DjangoContentType, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "guardian_userobjectpermission"
        unique_together = (("user", "permission", "object_pk"),)


class HighlighterActivelearningproject(models.Model):
    name = models.CharField(max_length=255)
    sampling_strategy = models.CharField(max_length=4)
    rebuild = models.IntegerField()
    log_dir = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = "highlighter_activelearningproject"


class HighlighterAnnotation(models.Model):
    start = models.PositiveIntegerField()
    end = models.PositiveIntegerField()
    orig_string = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=4, blank=True, null=True)
    annotation_project = models.ForeignKey(
        "HighlighterAnnotationproject", models.DO_NOTHING, blank=True, null=True
    )
    parent = models.ForeignKey("self", models.DO_NOTHING, blank=True, null=True)
    text = models.ForeignKey(ApisMetainfoText, models.DO_NOTHING)
    user_added = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "highlighter_annotation"


class HighlighterAnnotationEntityCandidate(models.Model):
    annotation = models.ForeignKey(HighlighterAnnotation, models.DO_NOTHING)
    uricandidate = models.ForeignKey(ApisMetainfoUricandidate, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "highlighter_annotation_entity_candidate"
        unique_together = (("annotation", "uricandidate"),)


class HighlighterAnnotationEntityLink(models.Model):
    gm2m_src = models.ForeignKey(HighlighterAnnotation, models.DO_NOTHING)
    gm2m_ct = models.ForeignKey(DjangoContentType, models.DO_NOTHING)
    gm2m_pk = models.CharField(max_length=16)

    class Meta:
        managed = False
        db_table = "highlighter_annotation_entity_link"
        unique_together = (("gm2m_src", "gm2m_ct", "gm2m_pk"),)


class HighlighterAnnotationproject(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    published = models.IntegerField()

    class Meta:
        managed = False
        db_table = "highlighter_annotationproject"


class HighlighterMenuentry(models.Model):
    kind = models.CharField(max_length=4)
    name = models.CharField(max_length=255, blank=True, null=True)
    api = models.ForeignKey(
        "HighlighterVocabularyapi", models.DO_NOTHING, blank=True, null=True
    )
    parent = models.ForeignKey("self", models.DO_NOTHING, blank=True, null=True)
    project = models.ForeignKey(
        "HighlighterProject", models.DO_NOTHING, blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "highlighter_menuentry"


class HighlighterProject(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    base_url = models.CharField(max_length=200, blank=True, null=True)
    store_text = models.IntegerField()
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = "highlighter_project"


class HighlighterTexthigh(models.Model):
    title = models.CharField(max_length=255, blank=True, null=True)
    text_type = models.CharField(max_length=3)
    uri = models.CharField(max_length=200, blank=True, null=True)
    text = models.TextField(blank=True, null=True)
    text_id = models.PositiveIntegerField(blank=True, null=True)
    text_class = models.CharField(max_length=255, blank=True, null=True)
    project = models.ForeignKey(
        HighlighterProject, models.DO_NOTHING, blank=True, null=True
    )

    class Meta:
        managed = False
        db_table = "highlighter_texthigh"


class HighlighterVocabularyapi(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    api_endpoint = models.CharField(max_length=255, blank=True, null=True)
    method = models.CharField(max_length=2)

    class Meta:
        managed = False
        db_table = "highlighter_vocabularyapi"


class InfosAbouttheproject(models.Model):
    title = models.CharField(max_length=300)
    subtitle = models.CharField(max_length=300)
    description = models.TextField()
    author = models.CharField(max_length=250)
    github = models.CharField(max_length=250)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = "infos_abouttheproject"


class InfosProjectinst(models.Model):
    name = models.CharField(max_length=300)
    abbr = models.CharField(max_length=300)
    description = models.TextField()
    website = models.CharField(max_length=300)
    logo_url = models.CharField(max_length=300)
    norm_url = models.CharField(max_length=300)

    class Meta:
        managed = False
        db_table = "infos_projectinst"


class InfosTeammember(models.Model):
    name = models.CharField(max_length=300)
    description = models.TextField()
    website = models.CharField(max_length=300)
    role = models.CharField(max_length=300)
    norm_url = models.CharField(max_length=300)

    class Meta:
        managed = False
        db_table = "infos_teammember"


class ReversionRevision(models.Model):
    date_created = models.DateTimeField()
    comment = models.TextField()
    user = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = "reversion_revision"


class ReversionVersion(models.Model):
    object_id = models.CharField(max_length=191)
    format = models.CharField(max_length=255)
    serialized_data = models.TextField()
    object_repr = models.TextField()
    content_type = models.ForeignKey(DjangoContentType, models.DO_NOTHING)
    revision = models.ForeignKey(ReversionRevision, models.DO_NOTHING)
    db = models.CharField(max_length=191)

    class Meta:
        managed = False
        db_table = "reversion_version"
        unique_together = (("db", "content_type", "object_id", "revision"),)
