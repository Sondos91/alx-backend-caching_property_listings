from django.apps import AppConfig


class PropertiesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'properties'
    verbose_name = 'Property Management'

    def ready(self):
        """
        Import signals when the app is ready to ensure they are registered.
        This method is called when Django starts up.
        """
        try:
            import properties.signals
        except ImportError:
            pass
