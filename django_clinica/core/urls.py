from django.urls import path
from django.contrib.auth import views as auth_views
from .views import HomeView, PricingView, RegisterView, ProfileView, ServiciosView, ServicioCreateView, ErrorView, ServicioEditView, ServicioDeleteView, ServicioEnrollmentView, ServiciosListView, UpdateInfoclienteView, AgregarAsistenciaView, AsistenciaListView, ProfilePasswordChangeView, AddUserView, CustomLoginView, UserDetailsView, superuser_edit, new_odontogram, tooth_view, update_odonto, view_odonto, ReservaCreateView, ReservaListView, ReservaUpdateView, ReservaDeleteView, ReservarHoraView, reservas_profesionales, ReservaDeleteClienteView, FaqView, PostQuestionView, PostAnswerView, AboutView, EditAboutView, AddAboutView, ConsultasView, CrearConsultaView, ConfirmarPagoView, VerificarConsultaView, ReservarConsultaView, webhook, CheckoutView, EditarConsultaView, EliminarConsultaView, payment_success, payment_failure, payment_pending, ConsultasPagadasView, ConsultasPendientesView
from .views import Crear_preferencia, CheckoutView,ServiciosDashboardView, VentasDashboardView
from django.contrib.auth.decorators import login_required
from .forms import CustomPasswordResetForm  # Importar CustomPasswordResetForm

from django.conf import settings
from django.conf.urls.static import static

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
    path('usuarios_detalles/<int:pk>/', 
        login_required(UserDetailsView.as_view()), 
        name='usuario_detalles'),
    
    # Página para editar el perfil de un usuario por un superusuario
    path('superuser_edit/<int:user_id>/', superuser_edit, name='superuser_edit'),
    
    
    # Página para solicitar odontograma
    path('new/', login_required(new_odontogram), name='new_odontogram'),
    path('tooth/<int:pk_mouth>/<str:nb_tooth>/', login_required(tooth_view), name='tooth'),
    path('update/<int:pk_mouth>/', login_required(update_odonto), name='update_odontogram'),
    path('view/<int:pk_mouth>/', login_required(view_odonto), name='odontogram_in_codes'),
    
    # Rutas para las vistas de reservas
    path('reservas/', login_required(ReservaListView.as_view()), name='reservas_disponibles'),
    path('reservas/nueva/', login_required(ReservaCreateView.as_view()), name='crear_reserva'),
    path('reservas/<int:pk>/editar/', login_required(ReservaUpdateView.as_view()), name='editar_reserva'),
    path('reservas/<int:pk>/eliminar/', login_required(ReservaDeleteView.as_view()), name='eliminar_reserva'),
    path('reservar_hora/<int:reserva_id>/', login_required(ReservarHoraView.as_view()), name='reservar_hora'),
    path('reservas/<int:pk>/eliminar_cliente/', login_required(ReservaDeleteClienteView.as_view()), name='eliminar_reserva_cliente'),
    path('reservas_profesionales/', login_required(reservas_profesionales), name='reservas_profesionales'),
    
    # Página de preguntas y respuestas
    path('faq/', FaqView.as_view(), name='faq'),
    path('faq/post_question/', PostQuestionView.as_view(), name='post_question'),
    path('faq/post_answer/<int:question_id>/', PostAnswerView.as_view(), name='post_answer'),
    
    # Página de información sobre nosotros
    path('about/', AboutView.as_view(), name='about'),
    path('about/edit/<int:pk>/', login_required(EditAboutView.as_view()), name='edit_about'),
    path('about/add/', login_required(AddAboutView.as_view()), name='add_about'),

    # Rutas para la recuperación de contraseña
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='registration/password_reset_form.html', form_class=CustomPasswordResetForm), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'), name='password_reset_complete'),

    # Rutas para consultas
    path('consultas/', ConsultasView.as_view(), name='consultas'),
    path('consultas/crear/', CrearConsultaView.as_view(), name='crear_consulta'),
    #path('consultas/confirmar_pago/<int:consulta_id>/', ConfirmarPagoView.as_view(), name='confirmar_pago'),

    path('consultas/confirmar_pago/<int:consulta_id>/', ConfirmarPagoView.as_view(), name='confirmar_pago'),

    path('consultas/verificar/', VerificarConsultaView.as_view(), name='verificar_consulta'),


    path('consultas/reservar/<int:pk>/', ReservarConsultaView.as_view(), name='reservar_consulta'),

    
    path('consultas/editar/<int:pk>/', login_required(EditarConsultaView.as_view()), name='editar_consulta'),
    path('consultas/eliminar/<int:pk>/', login_required(EliminarConsultaView.as_view()), name='eliminar_consulta'),
    
    path('consultas/pagadas/', ConsultasPagadasView.as_view(), name='consultas_pagadas'),
    path('consultas/pendientes/', ConsultasPendientesView.as_view(), name='consultas_pendientes'),

    # Ruta para el webhook de MercadoPago
    path('webhook/', webhook, name='webhook'),

    # Ruta para el Checkout Pro
    path('checkout/<str:preference_id>/', CheckoutView.as_view(), name='checkout'),


    path('crear-preferencia/<int:consulta_id>/', Crear_preferencia.as_view(), name='crear_preferencia'),
    
    path('payment/success/<int:consulta_id>/', payment_success, name='payment_success'),
    path('payment/failure/<int:consulta_id>/', payment_failure, name='payment_failure'),
    path('payment/pending/<int:consulta_id>/', payment_pending, name='payment_pending'),
    path('webhook/', webhook, name='webhook'),
    
    #dashboard
    # urls.py
    path('servicios/dashboard/', ServiciosDashboardView.as_view(), name='servicios_dashboard'),
    
    path('ventas/dashboard/', VentasDashboardView.as_view(), name='ventas_dashboard'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
