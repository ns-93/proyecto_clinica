import os

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.contrib.auth.models import Group, User
from django.contrib.auth.views import PasswordChangeView, LoginView
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import get_template
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import TemplateView, CreateView, UpdateView, DeleteView, ListView, DetailView

from .forms import RegisterForm, UserForm, ProfileForm, ServiciosForm, UserCreationForm, ReservaForm
from .models import Servicios, RegistroServicio, Infocliente, Asistencia, Mouth, Reserva
from accounts.models import Profile
from . import forms
from .models import Question, Answer
from .models import About
from .forms import AboutForm
# Create your views here.

# FUNCION PARA CONVERTIR EL PLURAL DE UN GRUPO A SU SINGULAR
def plural_to_singular(plural):
    # Diccionario que mapea los nombres de grupos en plural a su forma singular
    plural_singular = {
        "clientes": "cliente",
        "profesionales": "profesional",
        "ejecutivos": "ejecutivo",
        "administradores": "administrador",
    }
    # Devuelve la forma singular del grupo, o "error" si no se encuentra en el diccionario
    return plural_singular.get(plural, "error")

# OBTENER COLOR Y GRUPO DE UN USUARIO
def get_group_and_color(user):
    # Obtiene el primer grupo del usuario
    group = user.groups.first()
    group_id = None
    group_name = None
    group_name_singular = None
    color = None

    # Asigna un color de fondo dependiendo del grupo al que pertenece el usuario
    if group:
        if group.name == 'clientes':
            color = 'bg-primary'
        elif group.name == 'profesionales':
            color = 'bg-success'
        elif group.name == 'ejecutivos':
            color = 'bg-danger'
        elif group.name == 'administradores':
            color = 'bg-info'

        # Asigna el ID y el nombre del grupo
        group_id = group.id
        group_name = group.name
        group_name_singular = plural_to_singular(group.name)

    return group_id, group_name, group_name_singular, color

# DECORADOR PERSONALIZADO PARA AGREGAR EL NOMBRE DEL GRUPO AL CONTEXTO DE LA VISTA
def add_group_name_to_context(view_class):
    original_dispatch = view_class.dispatch

    def dispatch(self, request, *args, **kwargs):
        # Obtiene el grupo y color del usuario
        user = self.request.user
        group_id, group_name, group_name_singular, color = get_group_and_color(user)
        # Agrega la información del grupo al contexto
        context = {
            'group_name': group_name,
            'group_name_singular': group_name_singular,
            'color': color
        }

        self.extra_context = context
        return original_dispatch(self, request, *args, **kwargs)

    view_class.dispatch = dispatch
    return view_class


# VISTA DE LA PÁGINA PRINCIPAL
@add_group_name_to_context
class HomeView(TemplateView):
    template_name= 'home.html'


# VISTA DE LA PÁGINA DE PRECIOS Y OFERTAS
@add_group_name_to_context
class PricingView(TemplateView):
    template_name= 'pricing.html'


# VISTA DE REGISTRO DE USUARIOS
class RegisterView(View):

    def get(self, request):
        # Crea un formulario de registro vacío
        data = {
            'form': RegisterForm()
        }
        return render(request, 'registration/register.html', data)

    def post(self, request): 
        # Procesa el formulario de registro
        user_creation_form = RegisterForm(data=request.POST) 
        if user_creation_form.is_valid():
            user_creation_form.save()  # Guarda el usuario
            user = authenticate(username=user_creation_form.cleaned_data['username'], password=user_creation_form.cleaned_data['password1'])
            login(request, user) # Inicia sesión al usuario
            
            # Actualiza el campo created_by_admin del modelo Profile
            user.profile.created_by_admin = False
            user.profile.save()

            return redirect('home') # Redirige a la página de inicio
        
        data = {
            'form': user_creation_form
        }
        return render(request, 'registration/register.html', data)
    

# VISTA DE PERFIL DE USUARIO
@add_group_name_to_context
class ProfileView(TemplateView):
    """Vista para mostrar y gestionar el perfil del usuario"""
    template_name = 'profile/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        # Agrega los formularios de usuario y perfil al contexto
        context['user_form'] = UserForm(instance=user)
        context['profile_form'] = ProfileForm(instance=user.profile)

        if user.groups.filter(name='profesionales').exists():
            # Obtener todos los servicios asignados al profesional
            assigned_services = Servicios.objects.filter(profesional=user).order_by('-id')
            context['inscription_services'] = assigned_services.filter(status='S')
            context['progress_services'] = assigned_services.filter(status='P')
            context['finalized_services'] = assigned_services.filter(status='F')
            # Obtener todas las reservas del profesional
            context['reservas'] = Reserva.objects.filter(profesional=user)

        elif user.groups.filter(name='clientes').exists():
            # Obtener todos los servicios donde el cliente está inscrito
            registros = RegistroServicio.objects.filter(cliente=user).select_related('servicio')

            # Inicializar listas para cada tipo de servicio
            servicios_totales = []
            servicios_solicitud = []
            servicios_progreso = []
            servicios_finalizados = []

            # Clasificar servicios por estado
            for registro in registros:
                servicio = registro.servicio
                servicios_totales.append(servicio)

                if servicio.status == 'S':
                    servicios_solicitud.append(servicio)
                elif servicio.status == 'P':
                    servicios_progreso.append(servicio)
                elif servicio.status == 'F':
                    servicios_finalizados.append(servicio)

            # Agregar datos al contexto
            context.update({
                'servicios_totales': servicios_totales,
                'servicios_solicitud': servicios_solicitud,
                'servicios_progreso': servicios_progreso,
                'servicios_finalizados': servicios_finalizados,
                'cliente_id': user.id,
                'reservas': Reserva.objects.filter(cliente=user)  # Agregar reservas del cliente
            })

        elif user.groups.filter(name='ejecutivos').exists():
            # Obtener todos los servicios
            todos_servicios = Servicios.objects.all()
            
            # Filtrar por estado
            context['servicios_progreso'] = todos_servicios.filter(status='P')
            context['servicios_solicitud'] = todos_servicios.filter(status='S')
            context['servicios_finalizados'] = todos_servicios.filter(status='F')
            
            # Agregar conteo de registros
            for servicio in todos_servicios:
                servicio.registro_count = servicio.registroservicio_set.count()

        elif user.groups.filter(name='administradores').exists():
            # Obtengo todos los usuarios que no pertenecen al grupo administradores
            admin_group = Group.objects.get(name='administradores')
            """all_users = User.objects.exclude(groups__in=[admin_group])"""
            
            all_users = User.objects.all()
            # Obtengo todos los grupos
            all_groups = Group.objects.all()

            # Obtengo cada perfil de usuario
            user_profiles = []
            for user in all_users:
                profile = user.profile
                user_groups = user.groups.all()
                processed_groups = [plural_to_singular(group.name) for group in user_groups]
                user_profiles.append({
                    'user': user,
                    'groups': processed_groups,
                    'profile': profile
                })

            context['user_profiles'] = user_profiles

            # Obtener todos los servicios existentes
            all_services = Servicios.objects.all()
            context['servicios_solicitud'] = all_services.filter(status='S')
            context['servicios_progreso'] = all_services.filter(status='P')
            context['servicios_finalizados'] = all_services.filter(status='F')

        return context

    def post(self, request, *args, **kwargs):
        user = self.request.user
        user_form = UserForm(request.POST, instance=user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('profile')

        context = self.get_context_data()
        context['user_form'] = user_form
        context['profile_form'] = profile_form
        return render(request, 'profile/profile.html', context)



# MOSTRAR TODOS LOS servicios
# VISTA DE TODOS LOS SERVICIOS DISPONIBLES
@add_group_name_to_context
class ServiciosView(TemplateView):
    template_name = 'servicios.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        servicios = Servicios.objects.all().order_by('-id') # Obtiene todos los servicios
        cliente = self.request.user if self.request.user.is_authenticated else None

        for item in servicios:
            if (cliente):
                # importar RegistroServicio y Verifica si el cliente ya está registrado en el servicio
                registration = RegistroServicio.objects.filter(servicio=item, cliente=cliente).first()
                item.is_enrolled = registration is not None
            else:
                item.is_enrolled = False
            # Cuenta cuántos usuarios están registrados en el servicio
            enrollment_count = RegistroServicio.objects.filter(servicio=item).count()
            item.enrollment_count = enrollment_count

        context['servicios'] = servicios
        return context


# VISTA DE ERROR PARA USUARIOS QUE INTENTAN ACCEDER A UNA RUTA NO PERMITIDA
# pagina de error para usuario que intenten acceder mediante la ruta a servicios no permitidos
@add_group_name_to_context
class ErrorView(TemplateView):
    template_name = 'error.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        error_image_path = os.path.join(settings.MEDIA_URL, 'error.png') # Ruta de la imagen de error
        context['error_image_path'] = error_image_path
        return context


# VISTA PARA CREAR UN NUEVO SERVICIO
#crear un nuevo servicio
@add_group_name_to_context
class ServicioCreateView(UserPassesTestMixin, CreateView):
    model = Servicios 
    form_class = ServiciosForm  
    template_name = 'create_servicios.html'  
    success_url = reverse_lazy('servicios')    # Redirige a la página de servicios después de crear un servicio

    def test_func(self):
        # Permite solo a los administradores y ejecutivos crear un servicio
        return self.request.user.groups.filter(name__in=['administradores', 'ejecutivos']).exists()

    def handle_no_permission(self):
        return redirect('error') # Redirige a la página de error si no tiene permisos

    def form_valid(self, form):
        messages.success(self.request, 'El registro del servicio se ha guardado correctamente.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Ha ocurrido un error al guardar el registro del servicio.')
        return self.render_to_response(self.get_context_data(form=form))
    
#hasta aqui la creacion de un nuevo servico


# EDICIÓN DE UN SERVICIO CREADO
@add_group_name_to_context
class ServicioEditView(UserPassesTestMixin, UpdateView):
    # Define el modelo a utilizar para esta vista, en este caso, Servicio
    model = Servicios
    # Indica el formulario que se usará para editar un servicio
    form_class = ServiciosForm
    # Plantilla HTML donde se mostrará el formulario de edición
    template_name = 'edit_servicios.html'
    # URL a la que se redirige al usuario después de una edición exitosa
    success_url = reverse_lazy('servicios')

    # Método para verificar si el usuario tiene permiso para acceder a la vista
    def test_func(self):
        # Permite el acceso solo si el usuario pertenece al grupo 'administrativos'
        return self.request.user.groups.filter(name__in=['administradores', 'ejecutivos']).exists()

    # Método para manejar la falta de permisos del usuario
    def handle_no_permission(self):
        # Redirige al usuario a una página de error si no tiene permisos
        return redirect('error')

    # Método para manejar el caso en el que el formulario es válido
    def form_valid(self, form):
        # Guarda el formulario y muestra un mensaje de éxito
        form.save()
        messages.success(self.request, 'El servicio se ha actualizado correctamente')
        # Redirige a la URL de éxito
        return redirect(self.success_url)

    # Método para manejar el caso en el que el formulario es inválido
    def form_invalid(self, form):
        # Muestra un mensaje de error si hay un problema al actualizar
        messages.error(self.request, 'Ha ocurrido un error al actualizar el servicio')
        # Renderiza la respuesta con el contexto actual del formulario
        return self.render_to_response(self.get_context_data(form=form))
    
#hasta qui la edicion del servicio ya creado

@add_group_name_to_context
class ServicioDeleteView(UserPassesTestMixin, DeleteView):
    # Especifica el modelo de datos que se eliminará (en este caso, Servicio)
    model = Servicios
    # Define la plantilla HTML que se mostrará para confirmar la eliminación
    template_name = 'delete_servicio.html'
    # URL a la que se redirigirá el usuario si la eliminación se realiza con éxito
    success_url = reverse_lazy('servicios')

    # Define el criterio para que un usuario pueda acceder a esta vista.
    # Solo los usuarios del grupo "administrativos" pueden acceder
    def test_func(self):
        return self.request.user.groups.filter(name__in=['administradores', 'ejecutivos']).exists()

    # Maneja el caso en que el usuario no tiene permiso, redirigiéndolo a una página de error
    def handle_no_permission(self):
        return redirect('error')

    # Método que se ejecuta cuando la eliminación es válida
    def form_valid(self, form):
        # Envía un mensaje de éxito al usuario informando que el registro fue eliminado
        messages.success(self.request, 'El registro se ha eliminado correctamente')
        # Llama al método original form_valid() para continuar el proceso de eliminación
        return super().form_valid(form)

#hasta aqui la eliminacion de un servicio ya creado

#solicitud de un servicio o ingreso a un servicio creado
# Vista para gestionar la inscripción de un cliente en un servicio
@add_group_name_to_context
class ServicioEnrollmentView(View):
    # Método GET para manejar la inscripción de un cliente en un servicio
    def get(self, request, servicio_id):
        # Buscar el servicio usando el ID proporcionado, si no lo encontramos, lanza un 404
        servicio = get_object_or_404(Servicios, id=servicio_id)

        # Verificamos si el usuario está autenticado y pertenece al grupo 'clientes'
        if request.user.is_authenticated and request.user.groups.filter(name='clientes').exists():
            cliente = request.user  # Obtenemos al cliente (usuario actual)

            # Verifica si ya existe una inscripción para el cliente en este servicio
            existing_registration = RegistroServicio.objects.filter(servicio=servicio, cliente=cliente).first()

            if existing_registration:
                messages.warning(request, 'Ya has solicitado este servicio.')
            else:
                # Crear un registro de inscripción para el cliente y el servicio
                registro = RegistroServicio(servicio=servicio, cliente=cliente)
                registro.save()  # Guardamos el registro en la base de datos

                messages.success(request, 'Se ha solicitado correctamente este servicio. Gracias.')
        else:
            # Si no está autenticado o no pertenece al grupo adecuado, mostramos un mensaje de error
            messages.error(request, 'No se pudo completar la solicitud. Debes ser un cliente para solicitar este servicio.')

        # Redirige al usuario a la lista de servicios
        return redirect('servicios')  # Redirige a la vista de servicios

#hasta aqui el enrolamiento o anotacion de un servicio



# MOSTRAR LISTA DE CLIENTES Y SERVICIOS A LOS PROFESIONALES
# Vista para mostrar la lista de registros de servicio y clientes asociados.
@add_group_name_to_context
class ServiciosListView(TemplateView):
    template_name = 'servicios_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        servicios_id = self.kwargs['servicios_id']
        servicio = get_object_or_404(Servicios, id=servicios_id)
        registros_servicio = RegistroServicio.objects.filter(servicio=servicio)

        client_data = []
        for registro in registros_servicio:
            cliente = get_object_or_404(User, id=registro.cliente_id)
            infocliente = Infocliente.objects.filter(servicio=servicio, cliente=cliente).first()
            client_data.append({
                'registro_id': infocliente.id if infocliente else None,
                'nombre': cliente.get_full_name(),
                'observacion': infocliente.observacion if infocliente and infocliente.observacion else '',
                'archivo': infocliente.archivo.url if infocliente and infocliente.archivo else None,
                'odontograma': infocliente.odontograma.url if infocliente and infocliente.odontograma else None,
            })

        context['servicio'] = servicio
        context['client_data'] = client_data
        return context
#hasta aqui la lista de servicios y clientes

# Vista basada en clases para actualizar la información de un cliente.
@add_group_name_to_context
class UpdateInfoclienteView(UpdateView):
    model = Infocliente
    fields = ['observacion', 'archivo', 'odontograma']
    template_name = 'update_infocliente.html'

    def get_success_url(self):
        return reverse('servicios_list', kwargs={'servicios_id': self.object.servicio.id})

    def form_valid(self, form):
        response = super().form_valid(form)
        return redirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        infocliente = self.get_object()
        context['servicio_name'] = infocliente.servicio.name
        context['cliente_name'] = infocliente.cliente.get_full_name()
        return context

    def get_object(self, queryset=None):
        infocliente_id = self.kwargs['infocliente_id']
        return get_object_or_404(Infocliente, id=infocliente_id)
    
#hasta aqui la actualizacion de la informacion del cliente

#lista de asistencia de un servicio
@add_group_name_to_context
class AsistenciaListView(ListView):
    """Vista para listar las asistencias a las citas de un servicio"""
    model = Asistencia
    template_name = 'asistencia_list.html'
    context_object_name = 'asistencias'

    def get_queryset(self):
        """Define el queryset base para la vista"""
        servicio_id = self.kwargs['servicio_id']
        return Asistencia.objects.filter(
            servicio_id=servicio_id,
            date__isnull=False
        ).select_related('servicio', 'cliente').order_by('date')

    def get_context_data(self, **kwargs):
        """Obtiene el contexto con los datos de asistencias"""
        context = super().get_context_data(**kwargs)
        
        # Obtener servicio y sus clientes
        servicio = get_object_or_404(Servicios, id=self.kwargs['servicio_id'])
        registros_servicio = RegistroServicio.objects.filter(
            servicio=servicio
        ).select_related('cliente')

        # Obtener todas las fechas de asistencia
        fechas_asistencia = Asistencia.objects.filter(
            servicio=servicio,
            date__isnull=False
        ).values_list('date', flat=True).distinct().order_by('date')

        # Obtener todas las asistencias en un solo query
        asistencias = Asistencia.objects.filter(
            servicio=servicio,
            date__isnull=False
        ).select_related('cliente')

        # Crear diccionario de asistencias para acceso rápido
        asistencias_dict = {
            (a.cliente_id, a.date): a.present 
            for a in asistencias
        }

        # Preparar datos para la tabla
        asistencia_data = []
        for fecha in fechas_asistencia:
            datos_fecha = {
                'fecha': fecha,
                'asistencia_data': []
            }

            for registro in registros_servicio:
                estado = asistencias_dict.get((registro.cliente.id, fecha))
                datos_fecha['asistencia_data'].append({
                    'cliente': {
                        'cliente__id': registro.cliente.id,
                        'cliente__first_name': registro.cliente.first_name,
                        'cliente__last_name': registro.cliente.last_name
                    },
                    'estado_asistencia': estado,
                    'presente': estado is True,
                    'ausente': estado is False,
                    'sin_registro': estado is None
                })

            asistencia_data.append(datos_fecha)

        # Actualizar contexto
        sesiones_completadas = len(fechas_asistencia)
        context.update({
            'servicio': servicio,
            'clientes': registros_servicio.values(
                'cliente__id',
                'cliente__first_name',
                'cliente__last_name'
            ),
            'asistencia_data': asistencia_data,
            'sesiones_restantes': max(0, servicio.n_procedimientos - sesiones_completadas),
            'total_sesiones': servicio.n_procedimientos,
            'sesiones_completadas': sesiones_completadas
        })
        
        return context

#agregar asistencia a un servicio o procedimiento
@add_group_name_to_context
class AgregarAsistenciaView(TemplateView):
    template_name = 'agregar_asistencia.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        servicio_id = kwargs['servicio_id']
        servicio = get_object_or_404(Servicios, id=servicio_id)
        registros = RegistroServicio.objects.filter(servicio=servicio)
        
        context['servicio'] = servicio
        context['registros'] = registros
        return context

    def post(self, request, servicio_id):
        fecha = request.POST.get('date')
        if not fecha:
            messages.error(request, 'La fecha es requerida.')
            return redirect('agregar_asistencia', servicio_id=servicio_id)

        servicio = get_object_or_404(Servicios, id=servicio_id)
        registros = RegistroServicio.objects.filter(servicio=servicio)

        # Verificar si ya existe asistencia para esa fecha
        if Asistencia.objects.filter(servicio=servicio, date=fecha).exists():
            messages.error(request, 'Ya existe un registro de asistencia para esta fecha.')
            return redirect('agregar_asistencia', servicio_id=servicio_id)
        
        # Crear registros de asistencia
        for registro in registros:
            # Verificar si el checkbox existe en el POST
            checkbox_name = f'asistencia_{registro.cliente.id}'
            presente = checkbox_name in request.POST
            
            # Crear nueva asistencia si no existe
            asistencia, created = Asistencia.objects.get_or_create(
                cliente=registro.cliente,
                servicio=servicio,
                date=fecha,
                defaults={'present': presente}
            )

            if not created:
                asistencia.present = presente
                asistencia.save()

        messages.success(request, 'Asistencias registradas correctamente.')
        return redirect('lista_asistencia', servicio_id=servicio_id)
    
    
#hasta aqui la asistencia de un servicio

# CAMBIAR LA CONTRASEÑA DEL USUARIO
@add_group_name_to_context
class ProfilePasswordChangeView(PasswordChangeView):
    template_name = 'profile/change_password.html'
    success_url = reverse_lazy('profile')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['password_changed'] = self.request.session.get('password_changed', False)
        return context

    def form_valid(self, form):
        # Actualizar el campo created_by_admin del modelo Profile
        profile = Profile.objects.get(user=self.request.user)
        profile.created_by_admin = False
        profile.save()

        messages.success(self.request, 'Cambio de contraseña exitoso')
        update_session_auth_hash(self.request, form.user)
        self.request.session['password_changed'] = True
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(
            self.request,
            'Hubo un error al momento de intentar cambiar la contraseña: {}.'.format(
                form.errors.as_text()
            )
        )
        return super().form_invalid(form)
    
#hasta aqui el cambio de contraseña

# AGREGAR UN NUEVO USUARIO
@add_group_name_to_context
class AddUserView(UserPassesTestMixin, LoginRequiredMixin, CreateView):
    model = User
    form_class = UserCreationForm
    template_name = 'add_usuarios.html'
    success_url = reverse_lazy('profile')

    def test_func(self):
        return self.request.user.is_superuser

    def handle_no_permission(self):
        return redirect('error')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        groups = Group.objects.all()
        singular_groups = [plural_to_singular(group.name).capitalize() for group in groups]
        context['groups'] = zip(groups, singular_groups)
        return context

    def form_valid(self, form):
        # Obtener el grupo que seleccionó
        group_id = self.request.POST['group']
        group = get_object_or_404(Group, id=group_id)

        # Crear usuario sin guardarlo aún
        user = form.save(commit=False)

        # Colocamos una contraseña por defecto no aleatoria
        user.set_password('contraseña')

        # Convertir a un usuario al staff
        if group_id != '1':
            user.is_staff = True

        # Guardamos el usuario
        user.save()

        # Agregamos el usuario al grupo seleccionado
        user.groups.clear()
        user.groups.add(group)

        messages.success(self.request, 'Usuario creado exitosamente')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Hubo un error al intentar crear el usuario: {}.'.format(form.errors.as_text()))
        return super().form_invalid(form)
    
    
#hasta aqui la creacion de un nuevo usuario


#login personalizado
@add_group_name_to_context
class CustomLoginView(LoginView):
    def form_valid(self, form):
        response = super().form_valid(form)

        # Acceder al perfil del usuario
        profile = self.request.user.profile

        # Verificamos el valor del campo created_by_admin asegurandonos que el usuario fue creado por el administrador
        if profile.created_by_admin:
            messages.info(self.request, 'Su Contraseña fue creada por defecto remplezace su contraseña')
            response['Location'] = reverse_lazy('profile_password_change')
            response.status_code = 302

        return response

    def get_success_url(self):
        return super().get_success_url()

#hasta aqui el login personalizado

#vizualiacion de la informacion de un usuario
@add_group_name_to_context
# VISTA DE DETALLES DEL USUARIO
@add_group_name_to_context
class UserDetailsView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'usuarios_detalles.html'
    context_object_name = 'user_profile'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.get_object()
        group_id, group_name, group_name_singular, color = get_group_and_color(user)

        # Obtengo todos los grupos
        groups = Group.objects.all()
        singular_names = [plural_to_singular(group.name).capitalize() for group in groups]
        groups_ids = [group.id for group in groups]
        singular_groups = zip(singular_names, groups_ids)
        context['group_id_user'] = group_id
        context['group_name_user'] = group_name
        context['group_name_singular_user'] = group_name_singular
        context['color_user'] = color
        context['singular_groups'] = singular_groups

        if user.groups.first().name == 'profesionales':
            # Obtener todos los servicios asignados al profesional
            assigned_services = Servicios.objects.filter(profesional=user).order_by('-id')
            inscription_services = assigned_services.filter(status='S')
            progress_services = assigned_services.filter(status='P')
            finalized_services = assigned_services.filter(status='F')
            context['inscription_services'] = inscription_services
            context['progress_services'] = progress_services
            context['finalized_services'] = finalized_services

        elif user.groups.first().name == 'clientes':
            # Obtener todos los servicios donde el cliente está inscrito
            cliente_id = user.id
            registros = RegistroServicio.objects.filter(cliente=user)
            servicios_totales = []
            servicios_solicitud = []
            servicios_progreso = []
            servicios_finalizados = []

            for registro in registros:
                servicio = registro.servicio
                servicios_totales.append(servicio)

                if servicio.status == 'S':
                    servicios_solicitud.append(servicio)
                elif servicio.status == 'P':
                    servicios_progreso.append(servicio)
                elif servicio.status == 'F':
                    servicios_finalizados.append(servicio)

            context['cliente_id'] = cliente_id
            context['servicios_totales'] = servicios_totales
            context['servicios_solicitud'] = servicios_solicitud
            context['servicios_progreso'] = servicios_progreso
            context['servicios_finalizados'] = servicios_finalizados

        elif user.groups.first().name == 'ejecutivos':
            # Obtener todos los servicios existentes
            all_services = Servicios.objects.all()
            inscription_services = all_services.filter(status='S')
            progress_services = all_services.filter(status='P')
            finalized_services = all_services.filter(status='F')
            context['inscription_services'] = inscription_services
            context['progress_services'] = progress_services
            context['finalized_services'] = finalized_services

        return context
    
#hasta aqui la visualizacion de la informacion de un usuario

#actualizacion de la informacion de un usuario
# Vista para que un superusuario edite la información de un usuario
def superuser_edit(request, user_id):
    # Verificar si el usuario actual es un superusuario
    if not request.user.is_superuser:
        return redirect('error')

    # Obtener el usuario a editar
    user = User.objects.get(pk=user_id)
    
    if request.method == 'POST':
        # Crear formularios con los datos enviados en la solicitud POST
        user_form = UserForm(request.POST, instance=user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=user.profile)
        group = request.POST.get('group')

        # Verificar si los formularios son válidos
        if user_form.is_valid() and profile_form.is_valid():
            try:
                # Guardar los formularios
                user_form.save()
                profile_form.save()
                # Actualizar los grupos del usuario
                user.groups.clear()
                user.groups.add(group)
                # Redirigir a la página de detalles del usuario
                return redirect('usuario_detalles', pk=user.id)
            except forms.ValidationError as e:
                profile_form.add_error('rut', e)

    else:
        # Crear formularios con los datos actuales del usuario
        user_form = UserForm(instance=user)
        profile_form = ProfileForm(instance=user.profile)

    # Contexto para renderizar la plantilla
    context = {
        'user_form': user_form,
        'profile_form': profile_form
    }
    return render(request, 'usuarios_detalles.html', context)

#hasta aqui la actualizacion de la informacion de un usuario


#odontograma
def new_odontogram(request):
    odontogram = Mouth.objects.create()
    # append odontogram to profile
    if request.method == 'POST':
        return redirect('tooth', pk_mouth=odontogram.id)
    return render(request, 'odontogram/odontogram.html', {
        'odontogram': odontogram,
        }
    )


def tooth_view(request, pk_mouth, nb_tooth):
    nb_tooth
    odontogram = Mouth.objects.get(pk=pk_mouth)
    # Selection of field
    if nb_tooth == 't_11':
        tooth_form = forms.T11Form(instance=odontogram)
    elif nb_tooth == 't_12':
        tooth_form = forms.T12Form(instance=odontogram)
    elif nb_tooth == 't_13':
        tooth_form = forms.T13Form(instance=odontogram)
    elif nb_tooth == 't_14':
        tooth_form = forms.T14Form(instance=odontogram)
    elif nb_tooth == 't_15':
        tooth_form = forms.T15Form(instance=odontogram)
    elif nb_tooth == 't_16':
        tooth_form = forms.T16Form(instance=odontogram)
    elif nb_tooth == 't_17':
        tooth_form = forms.T17Form(instance=odontogram)
    elif nb_tooth == 't_18':
        tooth_form = forms.T18Form(instance=odontogram)
    elif nb_tooth == 't_21':
        tooth_form = forms.T21Form(instance=odontogram)
    elif nb_tooth == 't_22':
        tooth_form = forms.T22Form(instance=odontogram)
    elif nb_tooth == 't_23':
        tooth_form = forms.T23Form(instance=odontogram)
    elif nb_tooth == 't_24':
        tooth_form = forms.T24Form(instance=odontogram)
    elif nb_tooth == 't_25':
        tooth_form = forms.T25Form(instance=odontogram)
    elif nb_tooth == 't_26':
        tooth_form = forms.T26Form(instance=odontogram)
    elif nb_tooth == 't_27':
        tooth_form = forms.T27Form(instance=odontogram)
    elif nb_tooth == 't_28':
        tooth_form = forms.T28Form(instance=odontogram)
    elif nb_tooth == 't_31':
        tooth_form = forms.T31Form(instance=odontogram)
    elif nb_tooth == 't_32':
        tooth_form = forms.T32Form(instance=odontogram)
    elif nb_tooth == 't_33':
        tooth_form = forms.T33Form(instance=odontogram)
    elif nb_tooth == 't_34':
        tooth_form = forms.T34Form(instance=odontogram)
    elif nb_tooth == 't_35':
        tooth_form = forms.T35Form(instance=odontogram)
    elif nb_tooth == 't_36':
        tooth_form = forms.T36Form(instance=odontogram)
    elif nb_tooth == 't_37':
        tooth_form = forms.T37Form(instance=odontogram)
    elif nb_tooth == 't_38':
        tooth_form = forms.T38Form(instance=odontogram)
    elif nb_tooth == 't_41':
        tooth_form = forms.T41Form(instance=odontogram)
    elif nb_tooth == 't_42':
        tooth_form = forms.T42Form(instance=odontogram)
    elif nb_tooth == 't_43':
        tooth_form = forms.T43Form(instance=odontogram)
    elif nb_tooth == 't_44':
        tooth_form = forms.T44Form(instance=odontogram)
    elif nb_tooth == 't_45':
        tooth_form = forms.T45Form(instance=odontogram)
    elif nb_tooth == 't_46':
        tooth_form = forms.T46Form(instance=odontogram)
    elif nb_tooth == 't_47':
        tooth_form = forms.T47Form(instance=odontogram)
    elif nb_tooth == 't_48':
        tooth_form = forms.T48Form(instance=odontogram)
    elif nb_tooth == 't_51':
        tooth_form = forms.T51Form(instance=odontogram)
    elif nb_tooth == 't_52':
        tooth_form = forms.T52Form(instance=odontogram)
    elif nb_tooth == 't_53':
        tooth_form = forms.T53Form(instance=odontogram)
    elif nb_tooth == 't_54':
        tooth_form = forms.T54Form(instance=odontogram)
    elif nb_tooth == 't_55':
        tooth_form = forms.T55Form(instance=odontogram)
    elif nb_tooth == 't_61':
        tooth_form = forms.T61Form(instance=odontogram)
    elif nb_tooth == 't_62':
        tooth_form = forms.T62Form(instance=odontogram)
    elif nb_tooth == 't_63':
        tooth_form = forms.T63Form(instance=odontogram)
    elif nb_tooth == 't_64':
        tooth_form = forms.T64Form(instance=odontogram)
    elif nb_tooth == 't_65':
        tooth_form = forms.T65Form(instance=odontogram)
    elif nb_tooth == 't_71':
        tooth_form = forms.T71Form(instance=odontogram)
    elif nb_tooth == 't_72':
        tooth_form = forms.T72Form(instance=odontogram)
    elif nb_tooth == 't_73':
        tooth_form = forms.T73Form(instance=odontogram)
    elif nb_tooth == 't_74':
        tooth_form = forms.T74Form(instance=odontogram)
    elif nb_tooth == 't_75':
        tooth_form = forms.T75Form(instance=odontogram)
    elif nb_tooth == 't_81':
        tooth_form = forms.T81Form(instance=odontogram)
    elif nb_tooth == 't_82':
        tooth_form = forms.T82Form(instance=odontogram)
    elif nb_tooth == 't_83':
        tooth_form = forms.T83Form(instance=odontogram)
    elif nb_tooth == 't_84':
        tooth_form = forms.T84Form(instance=odontogram)
    else:
        tooth_form = forms.T85Form(instance=odontogram)
    if request.method == 'POST':
        # Selection of field
        if nb_tooth == 't_11':
            tooth_form = forms.T11Form(
                request.POST, instance=odontogram)
        elif nb_tooth == 't_12':
            tooth_form = forms.T12Form(
                request.POST, instance=odontogram)
        elif nb_tooth == 't_13':
            tooth_form = forms.T13Form(
                request.POST, instance=odontogram)
        elif nb_tooth == 't_14':
            tooth_form = forms.T14Form(
                request.POST, instance=odontogram)
        elif nb_tooth == 't_15':
            tooth_form = forms.T15Form(
                request.POST, instance=odontogram)
        elif nb_tooth == 't_16':
            tooth_form = forms.T16Form(
                request.POST, instance=odontogram)
        elif nb_tooth == 't_17':
            tooth_form = forms.T17Form(
                request.POST, instance=odontogram)
        elif nb_tooth == 't_18':
            tooth_form = forms.T18Form(
                request.POST, instance=odontogram)
        elif nb_tooth == 't_21':
            tooth_form = forms.T21Form(
                request.POST, instance=odontogram)
        elif nb_tooth == 't_22':
            tooth_form = forms.T22Form(
                request.POST, instance=odontogram)
        elif nb_tooth == 't_23':
            tooth_form = forms.T23Form(
                request.POST, instance=odontogram)
        elif nb_tooth == 't_24':
            tooth_form = forms.T24Form(
                request.POST, instance=odontogram)
        elif nb_tooth == 't_25':
            tooth_form = forms.T25Form(
                request.POST, instance=odontogram)
        elif nb_tooth == 't_26':
            tooth_form = forms.T26Form(
                request.POST, instance=odontogram)
        elif nb_tooth == 't_27':
            tooth_form = forms.T27Form(
                request.POST, instance=odontogram)
        elif nb_tooth == 't_28':
            tooth_form = forms.T28Form(
                request.POST, instance=odontogram)
        elif nb_tooth == 't_31':
            tooth_form = forms.T31Form(
                request.POST, instance=odontogram)
        elif nb_tooth == 't_32':
            tooth_form = forms.T32Form(
                request.POST, instance=odontogram)
        elif nb_tooth == 't_33':
            tooth_form = forms.T33Form(
                request.POST, instance=odontogram)
        elif nb_tooth == 't_34':
            tooth_form = forms.T34Form(
                request.POST, instance=odontogram)
        elif nb_tooth == 't_35':
            tooth_form = forms.T35Form(
                request.POST, instance=odontogram)
        elif nb_tooth == 't_36':
            tooth_form = forms.T36Form(
                request.POST, instance=odontogram)
        elif nb_tooth == 't_37':
            tooth_form = forms.T37Form(
                request.POST, instance=odontogram)
        elif nb_tooth == 't_38':
            tooth_form = forms.T38Form(
                request.POST, instance=odontogram)
        elif nb_tooth == 't_41':
            tooth_form = forms.T41Form(
                request.POST, instance=odontogram)
        elif nb_tooth == 't_42':
            tooth_form = forms.T42Form(
                request.POST, instance=odontogram)
        elif nb_tooth == 't_43':
            tooth_form = forms.T43Form(
                request.POST, instance=odontogram)
        elif nb_tooth == 't_44':
            tooth_form = forms.T44Form(
                request.POST, instance=odontogram)
        elif nb_tooth == 't_45':
            tooth_form = forms.T45Form(
                request.POST, instance=odontogram)
        elif nb_tooth == 't_46':
            tooth_form = forms.T46Form(
                request.POST, instance=odontogram)
        elif nb_tooth == 't_47':
            tooth_form = forms.T47Form(
                request.POST, instance=odontogram)
        elif nb_tooth == 't_48':
            tooth_form = forms.T48Form(
                request.POST, instance=odontogram)
        elif nb_tooth == 't_51':
            tooth_form = forms.T51Form(
                request.POST, instance=odontogram)
        elif nb_tooth == 't_52':
            tooth_form = forms.T52Form(
                request.POST, instance=odontogram)
        elif nb_tooth == 't_53':
            tooth_form = forms.T53Form(
                request.POST, instance=odontogram)
        elif nb_tooth == 't_54':
            tooth_form = forms.T54Form(
                request.POST, instance=odontogram)
        elif nb_tooth == 't_55':
            tooth_form = forms.T55Form(
                request.POST, instance=odontogram)
        elif nb_tooth == 't_61':
            tooth_form = forms.T61Form(
                request.POST, instance=odontogram)
        elif nb_tooth == 't_62':
            tooth_form = forms.T62Form(
                request.POST, instance=odontogram)
        elif nb_tooth == 't_63':
            tooth_form = forms.T63Form(
                request.POST, instance=odontogram)
        elif nb_tooth == 't_64':
            tooth_form = forms.T64Form(
                request.POST, instance=odontogram)
        elif nb_tooth == 't_65':
            tooth_form = forms.T65Form(
                request.POST, instance=odontogram)
        elif nb_tooth == 't_71':
            tooth_form = forms.T71Form(
                request.POST, instance=odontogram)
        elif nb_tooth == 't_72':
            tooth_form = forms.T72Form(
                request.POST, instance=odontogram)
        elif nb_tooth == 't_73':
            tooth_form = forms.T73Form(
                request.POST, instance=odontogram)
        elif nb_tooth == 't_74':
            tooth_form = forms.T74Form(
                request.POST, instance=odontogram)
        elif nb_tooth == 't_75':
            tooth_form = forms.T75Form(
                request.POST, instance=odontogram)
        elif nb_tooth == 't_81':
            tooth_form = forms.T81Form(
                request.POST, instance=odontogram)
        elif nb_tooth == 't_82':
            tooth_form = forms.T82Form(
                request.POST, instance=odontogram)
        elif nb_tooth == 't_83':
            tooth_form = forms.T83Form(
                request.POST, instance=odontogram)
        elif nb_tooth == 't_84':
            tooth_form = forms.T84Form(
                request.POST, instance=odontogram)
        else:
            tooth_form = forms.T85Form(
                request.POST, instance=odontogram)
        if tooth_form.is_valid():
            # append to profile
            tooth_form.save()
            messages.success(request,'Estado del diente actualizado!')
            return redirect('odontogram_in_codes', pk_mouth=pk_mouth)
    return render(request, 'odontogram/tooth.html', {
        'tooth_form': tooth_form,
        'pk_mouth': pk_mouth,
        'nb_tooth': nb_tooth,
        }
    )


def update_odonto(request, pk_mouth):
    odontogram = Mouth.objects.get(pk=pk_mouth)
    if request.method == 'POST':
        return redirect('tooth', pk_mouth=pk_mouth)
    return render(request, 'odontogram/odontogram.html', {
        'odontogram': odontogram,
        'pk_mouth': pk_mouth,
        }
    )


def view_odonto(request, pk_mouth):
    odontogram = Mouth.objects.get(pk=pk_mouth)
    treatments = [
        'sano', 'c1', 'c2', 'c3', 'c4', 'c5',
        'r1', 'r2', 'r3', 'r4', 'r5',
        'e', 'N', 'PL', 'p', 'z', 'd', 'g',
    ]
    if request.method == 'POST':
        return redirect('record:tooth', pk_mouth=pk_mouth)
    return render(request, 'odontogram/odontogram_codes.html', {
        'odontogram': odontogram,
        'pk_mouth': pk_mouth,
        'treatments': treatments,
        }
    )

@add_group_name_to_context
class ReservaCreateView(UserPassesTestMixin, CreateView):
    model = Reserva
    form_class = ReservaForm
    template_name = 'create_reserva.html'
    success_url = reverse_lazy('reservas_profesionales')

    def test_func(self):
        return self.request.user.groups.filter(name='profesionales').exists()

    def handle_no_permission(self):
        return redirect('error')

    def form_valid(self, form):
        reserva = form.save(commit=False)
        reserva.profesional = self.request.user
        reserva.save()
        messages.success(self.request, 'La reserva se ha creado correctamente.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Ha ocurrido un error al crear la reserva.')
        return self.render_to_response(self.get_context_data(form=form))


@add_group_name_to_context
class ReservaListView(LoginRequiredMixin, ListView):
    model = Reserva
    template_name = 'reservas.html'
    context_object_name = 'reservas'

    def get_queryset(self):
        if self.request.user.groups.filter(name='profesionales').exists():
            return Reserva.objects.filter(profesional=self.request.user)
        elif self.request.user.groups.filter(name='clientes').exists():
            return Reserva.objects.filter(cliente=self.request.user)
        return Reserva.objects.none()

@add_group_name_to_context
class ReservaListView(LoginRequiredMixin, ListView):
    model = Reserva
    template_name = 'reservas_disponibles.html'
    context_object_name = 'reservas'

    def get_queryset(self):
        return Reserva.objects.filter(cliente__isnull=True)

# Vista para que el cliente reserve una hora
@add_group_name_to_context
class ReservarHoraView(LoginRequiredMixin, View):
    def get(self, request, reserva_id):
        reserva = get_object_or_404(Reserva, id=reserva_id)
        if request.user.groups.filter(name='clientes').exists() and not reserva.cliente:
            if not Reserva.objects.filter(cliente=request.user).exists():
                reserva.cliente = request.user
                reserva.save()
                messages.success(request, 'Hora reservada exitosamente.')
            else:
                messages.error(request, 'Ya tienes una reserva activa.')
        else:
            messages.error(request, 'No se pudo reservar la hora.')
        return redirect('profile')

@add_group_name_to_context
class ReservaDeleteClienteView(LoginRequiredMixin, UserPassesTestMixin, View):
    def get_object(self):
        return get_object_or_404(Reserva, id=self.kwargs['pk'])

    def get(self, request, *args, **kwargs):
        reserva = self.get_object()
        if self.request.user == reserva.cliente:
            reserva.cliente = None
            reserva.save()
            messages.success(self.request, 'La reserva se ha anulado correctamente.')
        else:
            messages.error(self.request, 'No tienes permiso para anular esta reserva.')
        return redirect('profile')

    def test_func(self):
        reserva = self.get_object()
        return self.request.user == reserva.cliente

    def handle_no_permission(self):
        return redirect('error')

@add_group_name_to_context
class ReservaUpdateView(UserPassesTestMixin, UpdateView):
    model = Reserva
    form_class = ReservaForm
    template_name = 'update_reserva.html'
    success_url = reverse_lazy('reservas_profesionales')

    def test_func(self):
        reserva = self.get_object()
        return self.request.user == reserva.profesional

    def handle_no_permission(self):
        return redirect('error')

    def form_valid(self, form):
        messages.success(self.request, 'La reserva se ha actualizado correctamente.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Ha ocurrido un error al actualizar la reserva.')
        return self.render_to_response(self.get_context_data(form=form))


@add_group_name_to_context
class ReservaDeleteView(UserPassesTestMixin, DeleteView):
    model = Reserva
    template_name = 'delete_reserva.html'
    success_url = reverse_lazy('reservas_profesionales')

    def test_func(self):
        reserva = self.get_object()
        return self.request.user == reserva.profesional

    def handle_no_permission(self):
        return redirect('error')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'La reserva se ha eliminado correctamente.')
        return super().delete(request, *args, **kwargs)


def reservas_profesionales(request):
    reservas = Reserva.objects.all()
    return render(request, 'reservas_profesionales.html', {'reservas': reservas})

#vista de preguntas frecuentes

class FaqView(View):
    def get(self, request):
        questions = Question.objects.all()
        group_name = None
        if request.user.is_authenticated:
            group = request.user.groups.first()
            if group:
                group_name = group.name
        return render(request, 'faq.html', {'questions': questions, 'group_name': group_name})

class PostQuestionView(LoginRequiredMixin, View):
    def post(self, request):
        question_text = request.POST.get('question')
        Question.objects.create(user=request.user, text=question_text)
        return redirect('faq')

class PostAnswerView(LoginRequiredMixin, View):
    def post(self, request, question_id):
        if request.user.groups.filter(name='ejecutivos').exists():
            answer_text = request.POST.get('answer')
            question = Question.objects.get(id=question_id)
            Answer.objects.create(question=question, text=answer_text)
            messages.success(request, 'Respuesta publicada exitosamente.')
        else:
            messages.error(request, 'No tienes permiso para publicar una respuesta.')
        return redirect('faq')

# Vista para mostrar la información de "Acerca de"
class AboutView(TemplateView):
    template_name = 'about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        about = About.objects.first()
        context['about'] = about
        if self.request.user.is_authenticated:
            group = self.request.user.groups.first()
            if group:
                context['group_name'] = group.name
        return context

# Vista para editar la información de "Acerca de"
@add_group_name_to_context
class EditAboutView(UserPassesTestMixin, UpdateView):
    model = About
    form_class = AboutForm
    template_name = 'edit_about.html'
    success_url = reverse_lazy('about')

    def test_func(self):
        return self.request.user.groups.filter(name='ejecutivos').exists()

    def handle_no_permission(self):
        return redirect('error')

    def form_valid(self, form):
        messages.success(self.request, 'La información de "Acerca de" se ha actualizado correctamente.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Ha ocurrido un error al actualizar la información de "Acerca de".')
        return self.render_to_response(self.get_context_data(form=form))

@add_group_name_to_context
class AddAboutView(UserPassesTestMixin, CreateView):
    model = About
    form_class = AboutForm
    template_name = 'add_about.html'
    success_url = reverse_lazy('about')

    def test_func(self):
        return self.request.user.groups.filter(name='ejecutivos').exists()

    def handle_no_permission(self):
        return redirect('error')

    def form_valid(self, form):
        messages.success(self.request, 'La información de "Acerca de" se ha agregado correctamente.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Ha ocurrido un error al agregar la información de "Acerca de".')
        return self.render_to_response(self.get_context_data(form=form))
