from django.apps import AppConfig


class ApisInstanceViecproConfig(AppConfig):
    default_auto_field = "django.db.models.AutoField"
    name = "apis_instance_viecpro"

    def ready(self):
        import apis_instance_viecpro.signals  # noqa: F401
