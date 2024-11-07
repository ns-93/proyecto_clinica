"""
ASGI config for django_clinica project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os

# Se importa la función 'get_asgi_application' de Django, que nos permite obtener la aplicación ASGI (Asynchronous Server Gateway Interface).
from django.core.asgi import get_asgi_application

# Se configura la variable de entorno 'DJANGO_SETTINGS_MODULE' con el valor 'django_clinica.settings'.
# Esta variable indica a Django cuál es el archivo de configuración (settings.py) que debe utilizar
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_clinica.settings')

# Se obtiene la aplicación ASGI utilizando la función 'get_asgi_application'. 
# Esta es la aplicación que se usará para manejar las solicitudes asíncronas en el servidor.
application = get_asgi_application()
