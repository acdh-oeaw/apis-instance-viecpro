from django.contrib.contenttypes.models import ContentType
from django.views.generic.base import TemplateView

from apis_instance_viecpro.models import Ampel


class AmpelView(TemplateView):
    template_name = "apis_instance_viecpro/ampel.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        content_type = self.kwargs.get("content_type")
        content_type = ContentType.objects.get(pk=content_type)
        pk = self.kwargs.get("pk")
        ampel, _ = Ampel.objects.get_or_create(content_type=content_type, object_id=pk)
        ampel.status = self.kwargs.get("status")
        ampel.save()
        ctx["object"] = ampel
        return ctx
