
from django.urls import path
from .views import HomeView, PricingView, RegisterView, ProfileView, ServiciosView, ServicioCreateView, ErrorView
from django.contrib.auth.decorators import login_required

# Definición de las rutas o URLs para la aplicación
urlpatterns = [
        # Página de inicio: Ruta principal de la web
    path('', HomeView.as_view(), name='home'),
    # Página de precios y ofertas: Muestra la información sobre precios y ofertas disponibles
    path('pricing/', PricingView.as_view(),name='pricing'),
    # Página de registro de usuarios y login: Ruta para el registro de nuevos usuarios
    path('register/', RegisterView.as_view(), name='register'),
    # Página de perfil y edición de perfil: Ruta para que los usuarios accedan a su perfil y lo editen
    # Se requiere que el usuario esté logueado para acceder a esta página
    path('profile/', login_required(ProfileView.as_view()), name='profile'),
    # Página de servicios y lista de servicios: Muestra los servicios disponibles en la plataforma
    path('servicios/', ServiciosView.as_view(), name='servicios'),
    # Página para crear servicios: Los profesionales pueden crear nuevos servicios
    # Se requiere que el usuario esté logueado para acceder a esta página
    path('servicios/create/', login_required(ServicioCreateView.as_view()), name='servicios_create'),
    # Página de error: Para mostrar un mensaje de error si un usuario sin permisos intenta acceder a una ruta restringida
    path('error/', login_required(ErrorView.as_view()), name='error'),
]
