
from django.urls import path
from .views import HomeView, PricingView, RegisterView, ProfileView, ServiciosView

urlpatterns = [
        #pagina de inicio
    path('', HomeView.as_view(), name='home'),
    #pagina de precios y ofertas
    path('pricing/', PricingView.as_view(),name='pricing'),
    #pagina de registro de usuarios y login
    path('register/', RegisterView.as_view(), name='register'),
    #pagina de perfil y edicion de perfil
    path('profile/', ProfileView.as_view(), name='profile'),
    #pagina de servicios y lista de servicios
    path('servicios/', ServiciosView.as_view(), name='servicios'),
]
