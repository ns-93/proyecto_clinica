from django.apps import AppConfig

# Define la configuración para la aplicación 'core'
class CoreConfig(AppConfig):
    # Especifica el tipo de campo automático que se usará como clave primaria en los modelos de esta app
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'
    verbose_name = 'django_clinica'
    # Nombre de la aplicación; debe coincidir con el nombre de la carpeta de la app

    def ready(self):
        import core.signals
