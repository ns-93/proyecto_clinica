
from django.urls import path
from .views import HomeView, PricingView, RegisterView, ProfileView, ServiciosView, ServicioCreateView, ErrorView
from django.contrib.auth.decorators import login_required


urlpatterns = [
        #pagina de inicio
    path('', HomeView.as_view(), name='home'),
    #pagina de precios y ofertas
    path('pricing/', PricingView.as_view(),name='pricing'),
    #pagina de registro de usuarios y login
    path('register/', RegisterView.as_view(), name='register'),
    #pagina de perfil y edicion de perfil
    path('profile/', login_required(ProfileView.as_view()), name='profile'),
    #pagina de servicios y lista de servicios
    path('servicios/', ServiciosView.as_view(), name='servicios'),
    #pagina para crear servicios
    path('servicios/create/', login_required(ServicioCreateView.as_view()), name='servicios_create'),
    #pagina de error para  usuario sin permisos que busque acceder mediante la ruta
    path('error/', login_required(ErrorView.as_view()), name='error'),
]
