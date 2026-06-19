# 'INSTALLED_APPS' may be undefined, or defined from star imports: apis_acdhch_default_settings.settings
# ruff: noqa: F405
from apis_acdhch_default_settings.settings import *  # noqa: F403
import os

INSTALLED_APPS[INSTALLED_APPS.index("apis_ontology")] = "apis_instance_viecpro"
INSTALLED_APPS += ["simple_history"]
INSTALLED_APPS += ["django.contrib.postgres"]
INSTALLED_APPS += ["django_interval"]
INSTALLED_APPS += ["apis_bibsonomy"]

ROOT_URLCONF = "apis_instance_viecpro.urls"

LANGUAGE_CODE = "de"

if db_url := os.environ.get("OLD_DATABASE_URL", False):
    print("Connecting to OLD_DATABASE_URL")
    DATABASES["old"] = dj_database_url.parse(db_url)
