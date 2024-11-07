"""
WSGI config for django_clinica project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""
# Importación del módulo os para trabajar con variables de entorno y configuraciones
import os

# Importación de la función get_wsgi_application de Django, 
# que devuelve la aplicación WSGI que se utiliza para interactuar con servidores web.
from django.core.wsgi import get_wsgi_application

# Establecemos la variable de entorno DJANGO_SETTINGS_MODULE a la configuración de tu proyecto.
# Esto indica a Django que cargue la configuración desde el archivo 'django_clinica.settings'.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_clinica.settings')

# Se asigna la aplicación WSGI que Django usará para servir la aplicación web.
application = get_wsgi_application()
