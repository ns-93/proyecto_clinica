
from django.urls import path
from .views import HomeView, PricingView, RegisterView, ProfileView, ServiciosView, ServicioCreateView, ErrorView, ServicioEditView, ServicioDeleteView, ServicioEnrollmentView, ServiciosListView, UpdateInfoclienteView, AgregarAsistenciaView, AsistenciaListView, ProfilePasswordChangeView, AddUserView, CustomLoginView, UserDetailsView, superuser_edit
from django.contrib.auth.decorators import login_required

# Definición de las rutas o URLs para la aplicación
urlpatterns = [
    # Página de inicio: Ruta principal de la web
    path('', HomeView.as_view(), name='home'),
    
    # Página de precios y ofertas: Muestra la información sobre precios y ofertas disponibles
    path('pricing/', PricingView.as_view(), name='pricing'),
    
    # Página de registro de usuarios y login: Ruta para el registro de nuevos usuarios
    path('register/', RegisterView.as_view(), name='register'),
    
    # Página de perfil y edición de perfil: Ruta para que los usuarios accedan a su perfil y lo editen
    # Se requiere que el usuario esté logueado para acceder a esta página
    path('profile/', login_required(ProfileView.as_view()), name='profile'),
    # Ruta para cambiar la contraseña del perfil
    path('profile/change-password/', login_required(ProfilePasswordChangeView.as_view()), name='profile_password_change'),
    # Ruta para agregar un nuevo usuario
    path('usuarios/agregar/', login_required(AddUserView.as_view()), name='add_usuarios'),
    
    # Página de servicios y lista de servicios: Muestra los servicios disponibles en la plataforma
    path('servicios/', ServiciosView.as_view(), name='servicios'),
    # Página para crear servicios: Los profesionales pueden crear nuevos servicios
    # Se requiere que el usuario esté logueado para acceder a esta página
    path('servicios/create/', login_required(ServicioCreateView.as_view()), name='servicios_create'),
    # Ruta para la edición de un servicio específico
    path('servicios/<int:pk>/edit/', login_required(ServicioEditView.as_view()), name='editar_servicios'),
    # Definimos la URL para la eliminación de un servicio específico.
    path('servicios/<int:pk>/delete/', login_required(ServicioDeleteView.as_view()), name='eliminar_servicios'),
    # Define una ruta URL para la inscripción de un servicio, con un parámetro dinámico 'servicio_id' de tipo entero
    path('inscribir-servicio/<int:servicio_id>/', login_required(ServicioEnrollmentView.as_view()), name='inscribir_servicio'),
    # Define la URL que apunta a la vista ServiciosListView, pasando un parámetro service_id para identificar el servicio específico, con el nombre de ruta 'servicios_list'.
    path('servicios/<int:servicios_id>/', login_required(ServiciosListView.as_view()), name='servicios_list'),
    # URL para actualizar la información del cliente
    path('servicios/update_infocliente/<int:infocliente_id>/', login_required(UpdateInfoclienteView.as_view()), name='update_info'),
    # URL para listar asistencias de un servicio
    path('servicios/<int:servicio_id>/asistencias/', login_required(AsistenciaListView.as_view()), name='lista_asistencia'),
    # URL para agregar asistencias a un servicio
    path('servicios/<int:servicio_id>/asistencias/agregar/', login_required(AgregarAsistenciaView.as_view()), name='agregar_asistencia'),
    
    # Página de error: Para mostrar un mensaje de error si un usuario sin permisos intenta acceder a una ruta restringida
    path('error/', login_required(ErrorView.as_view()), name='error'),
    
    # Página de login personalizada: Ruta para el login de usuarios
    path('login/', CustomLoginView.as_view(), name='custom_login'),
    
    # Página de detalles de usuario: Muestra los detalles de un usuario específico
    path('usuarios_detalles/<int:pk>/', login_required(UserDetailsView.as_view()), name='usuario_detalles'),
    
    # Página para editar el perfil de un usuario por un superusuario
    path('superuser_edit/<int:user_id>/', login_required(superuser_edit), name='superuser_edit'),
    
]
    

