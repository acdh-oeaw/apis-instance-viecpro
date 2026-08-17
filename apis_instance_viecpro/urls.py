from apis_acdhch_default_settings.urls import urlpatterns
from django.urls import include, path

urlpatterns += [path("", include("django_interval.urls"))]
