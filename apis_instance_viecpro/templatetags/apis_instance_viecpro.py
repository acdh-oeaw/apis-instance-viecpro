from django import template
from django.contrib.contenttypes.models import ContentType
from django.db import models

from apis_instance_viecpro.models import Ampel

register = template.Library()


@register.inclusion_tag("apis_instance_viecpro/ampel.html")
def get_ampel_for_object(obj: models.Model):
    content_type = ContentType.objects.get_for_model(obj)
    ampel, _ = Ampel.objects.get_or_create(content_type=content_type, object_id=obj.pk)
    return {"object": ampel}
