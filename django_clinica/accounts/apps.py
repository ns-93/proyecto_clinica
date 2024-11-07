from django.apps import AppConfig

# Define la configuración de la aplicación 'accounts'
class AccountsConfig(AppConfig):
    # Establece el tipo de campo de clave primaria predeterminado para los modelos en esta app
    default_auto_field = 'django.db.models.BigAutoField'
    # Nombre de la aplicación; debe coincidir con el nombre de la carpeta de la app
    name = 'accounts'
    # Nombre legible para mostrar en el panel de administración de Django
    verbose_name = 'perfiles'


    #mediante la funcion ready que se encargara de cargar nuestra app y llamar al signals mediante un import
    # Método ready que se ejecuta cuando Django carga la aplicación
    # Este método se utiliza aquí para importar el módulo 'signals' de la app
    # Esto asegura que las señales definidas en 'accounts/signals.py' se carguen correctamente
    def ready(self):
        import accounts.signals

