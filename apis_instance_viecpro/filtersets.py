from apis_core.entities.filtersets import EntityFilterSet


class PersonFilterSet(EntityFilterSet):
    class Meta(EntityFilterSet.Meta):
        exclude = ["merged_into", "grouped_into"]
