from apis_core.generic.tables import CustomTemplateColumn
from apis_core.relations.tables import RelationsListTable


class ReferenceColumn(CustomTemplateColumn):
    template_name = "columns/reference.html"


class EntityRelationsTable(RelationsListTable):
    reference = ReferenceColumn()

    class Meta(RelationsListTable.Meta):
        sequence = RelationsListTable.Meta.sequence + ("reference",)
