"""
URL configuration for django_clinica project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from core import views  # Asegúrate de importar las vistas

# Definición de las rutas de URL del proyecto.
urlpatterns = [
    # Ruta para acceder al panel de administración de Django.
    # 'admin/' es la URL para acceder a la interfaz de administración.
    path('admin/', admin.site.urls),

    # Ruta para las URLs de la app 'core'.
    # Esto incluye todas las URLs definidas en el archivo 'core/urls.py'.
    path('', include('core.urls')),

    # Ruta para las URLs de autenticación proporcionadas por Django (login, logout, etc.).
    # Esto incluye las URLs estándar de Django para manejo de usuarios.
    path('accounts/', include('django.contrib.auth.urls')),
    
    # Ruta para la vista 'lista_especialidades'.
    path('lista_especialidades/', views.lista_especialidades, name='lista_especialidades'),
]

# Solo se ejecutará si el modo DEBUG está habilitado.
# Esto permite servir archivos multimedia (como imágenes) durante el desarrollo.
if settings.DEBUG:
    # Importamos la función para manejar archivos estáticos en el entorno de desarrollo.
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # A��adimos una ruta para servir archivos multimedia, 
    # basada en la configuración MEDIA_URL y MEDIA_ROOT en el archivo settings.py.