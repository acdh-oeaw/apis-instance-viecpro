import os
from pathlib import Path
from apis_acdhch_default_settings.settings import *

INSTALLED_APPS[INSTALLED_APPS.index("apis_ontology")] = "apis_instance_viecpro"
INSTALLED_APPS += ["simple_history"]
INSTALLED_APPS += ["django.contrib.postgres"]

ROOT_URLCONF = "apis_instance_viecpro.urls"

LANGUAGE_CODE = "de"

STATIC_ROOT = "/data"
