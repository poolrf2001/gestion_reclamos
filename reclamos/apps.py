from django.apps import AppConfig


class ReclamosConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'reclamos'
    def ready(self):
        import reclamos.signals
