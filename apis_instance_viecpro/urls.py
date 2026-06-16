from django.urls import include, path
from apis_acdhch_default_settings.urls import urlpatterns  # noqa: F401

urlpatterns += [path("", include("django_interval.urls"))]
