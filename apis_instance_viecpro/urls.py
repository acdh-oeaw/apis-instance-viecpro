from apis_acdhch_default_settings.urls import urlpatterns
from django.urls import include, path

from apis_instance_viecpro.views import AmpelView

urlpatterns += [path("", include("django_interval.urls"))]
urlpatterns += [path("", include("django_grouper.urls"))]
urlpatterns += [
    path(
        "ampel/<int:content_type>/<int:pk>/<status>", AmpelView.as_view(), name="ampel"
    )
]
