import django_tables2 as tables
from apis_core.generic.tables import CustomTemplateColumn, GenericTable
from apis_core.relations.tables import RelationsListTable


class ReferenceColumn(CustomTemplateColumn):
    template_name = "columns/reference.html"


class EntityRelationsTable(RelationsListTable):
    start = tables.Column(order_by="start_date_sort")
    end = tables.Column(order_by="end_date_sort")
    ampel = tables.TemplateColumn(template_name="columns/relation_ampel.html")

    class Meta(RelationsListTable.Meta):
        sequence = RelationsListTable.Meta.sequence


class PersonTable(GenericTable):
    ampel_value = tables.TemplateColumn(template_name="columns/ampel.html")
