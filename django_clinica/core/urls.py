
from django.urls import path
from .views import HomeView, PricingView, RegisterView

urlpatterns = [
    #pagina de inicio
    path('', HomeView.as_view(), name='home'),
    #pagina de precios y ofertas
    path('pricing/', PricingView.as_view(),name='pricing'),
    #pagina de registro de usuarios y login
    path('register/', RegisterView.as_view(), name='register'),
    


    
]
