import django_tables2 as tables
from apis_core.generic.tables import CustomTemplateColumn
from apis_core.relations.tables import RelationsListTable


class ReferenceColumn(CustomTemplateColumn):
    template_name = "columns/reference.html"


class EntityRelationsTable(RelationsListTable):
    reference = ReferenceColumn()
    start = tables.Column(order_by="start_date_sort")
    end = tables.Column(order_by="end_date_sort")
    label = tables.Column(accessor="legacy_relation_vocab_label")
    notes = tables.Column()

    class Meta(RelationsListTable.Meta):
        sequence = RelationsListTable.Meta.sequence + ("reference",)
