from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'
    verbose_name = 'perfiles'


    #mediante la funcion ready que se encargara de cargar nuestra app y llamar al signals mediante un import
    def ready(self):
        import accounts.signals
