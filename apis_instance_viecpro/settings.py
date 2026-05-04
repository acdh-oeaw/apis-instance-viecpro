# 'INSTALLED_APPS' may be undefined, or defined from star imports: apis_acdhch_default_settings.settings
# ruff: noqa: F405
from apis_acdhch_default_settings.settings import *  # noqa: F403

INSTALLED_APPS[INSTALLED_APPS.index("apis_ontology")] = "apis_instance_viecpro"
INSTALLED_APPS += ["simple_history"]
INSTALLED_APPS += ["django.contrib.postgres"]

ROOT_URLCONF = "apis_instance_viecpro.urls"

LANGUAGE_CODE = "de"
