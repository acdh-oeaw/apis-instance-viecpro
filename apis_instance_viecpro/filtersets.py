import django_filters
from apis_core.entities.filtersets import EntityFilterSet as CoreEntityFilterSet
from django.contrib.contenttypes.models import ContentType
from django.db import models

from .models import Ampel


class AmpelFilter(django_filters.MultipleChoiceFilter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        choices = ["red", "green", "yellow"]
        self.extra["choices"] = list(zip(choices, choices))

    def filter(self, qs, value):
        if value:
            if "red" in value:
                value += [""]
            content_type = ContentType.objects.get_for_model(qs.model)
            qs = qs.annotate(
                ampel_value=models.Subquery(
                    Ampel.objects.filter(
                        content_type=content_type, object_id=models.OuterRef("pk")
                    ).values("status")
                )
            )
            return qs.filter(ampel_value__in=value)
        return qs


class EntityFilterSet(CoreEntityFilterSet):
    ampel = AmpelFilter(label="Ampel")


class PersonFilterSet(EntityFilterSet):
    class Meta(EntityFilterSet.Meta):
        exclude = ["merged_into", "grouped_into"]
