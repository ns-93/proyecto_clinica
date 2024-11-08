from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.views.generic import TemplateView, CreateView, UpdateView, DeleteView
from django.contrib.auth.models import Group
from .forms import RegisterForm, UserForm, ProfileForm, ServiciosForm 
from django.views import View
from django.contrib.auth.models import User
from django.utils.decorators import method_decorator
from .models import Servicios, RegistroServicio, Infocliente
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin
from django.conf import settings
import os
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
            return redirect('home') # Redirige a la página de inicio
        
        data = {
            'form': user_creation_form
        }
        return render(request, 'registration/register.html', data)
    

# VISTA DEL PERFIL DEL USUARIO
@add_group_name_to_context
class ProfileView(TemplateView):
    template_name = 'profile/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        # Agrega los formularios de usuario y perfil al contexto
        context['user_form'] = UserForm(instance=user)  # Formulario del usuario
        context['profile_form'] = ProfileForm(instance=user.profile)  # Formulario del perfil

        # Se ajusta para manejar diferentes grupos de usuarios
        if user.groups.filter(name='profesionales').exists():
            # Obtener todos los servicios asignados al profesional
            assigned_services = Servicios.objects.filter(profesional=user).order_by('-id')
            inscription_services = assigned_services.filter(status='S')  # Servicios solicitados
            progress_services = assigned_services.filter(status='P')  # Servicios en progreso
            finalized_services = assigned_services.filter(status='F')  # Servicios finalizados
            context['inscription_services'] = inscription_services
            context['progress_services'] = progress_services
            context['finalized_services'] = finalized_services

        elif user.groups.filter(name='clientes').exists():
            # Obtener todos los servicios donde el cliente está inscrito
            registrations = RegistroServicio.objects.filter(cliente=user)
            enrolled_services = []
            inscription_services = []
            progress_services = []
            finalized_services = []

            for registration in registrations:
                service = registration.servicio
                enrolled_services.append(service)

                if service.status == 'S':
                    inscription_services.append(service)  # Servicios solicitados
                elif service.status == 'P':
                    progress_services.append(service)  # Servicios en progreso
                elif service.status == 'F':
                    finalized_services.append(service)  # Servicios finalizados

            context['enrolled_services'] = enrolled_services
            context['inscription_services'] = inscription_services
            context['progress_services'] = progress_services
            context['finalized_services'] = finalized_services

        elif user.groups.filter(name='administradores').exists() or user.groups.filter(name='ejecutivos').exists():
            # Obtener todos los servicios disponibles para los administradores y ejecutivos
            all_services = Servicios.objects.all()
            inscription_services = all_services.filter(status='S')  # Servicios solicitados
            progress_services = all_services.filter(status='P')  # Servicios en progreso
            finalized_services = all_services.filter(status='F')  # Servicios finalizados
            context['inscription_services'] = inscription_services
            context['progress_services'] = progress_services
            context['finalized_services'] = finalized_services
        
        return context

    def post(self, request, *args, **kwargs):
        user = self.request.user
        user_form = UserForm(request.POST, instance=user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=user.profile)

        # Procesa los formularios de perfil y usuario
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()  # Guarda el formulario de usuario
            profile_form.save()  # Guarda el formulario de perfil
            return redirect('profile')  # Redirige al perfil del usuario

        # Si los datos no son válidos, vuelve a mostrar el formulario con los errores
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
            if cliente:
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

                messages.success(request, 'Se a solicitado correctamente este servicio Gracias')
        else:
            # Si no está autenticado o no pertenece al grupo adecuado, mostramos un mensaje de error
            messages.error(request, 'No se pudo completar la Solicitud. Debes ser un cliente para Solicitar este servicio.')

        # Redirige al usuario a la lista de servicios
        return redirect('servicios')  # Redirige a la vista de servicios

#hasta aqui el enrolamiento o anotacion de un servicio



# MOSTRAR LISTA DE CLIENTES Y SERVICIOS A LOS PROFESIONALES
# Vista para mostrar la lista de registros de servicio y clientes asociados.
@add_group_name_to_context
class ServiciosListView(TemplateView):
    template_name = 'servicios_list.html'

    def get_context_data(self, **kwargs):
        # Se obtiene el contexto base desde la clase TemplateView
        context = super().get_context_data(**kwargs)
        
        # Se obtiene el ID del servicio desde los parámetros de la URL
        service_id = self.kwargs['service_id']
        
        # Buscamos el servicio en la base de datos usando el ID
        servicio = get_object_or_404(Servicios, id=service_id)
        
        # Filtramos los registros de servicio asociados al servicio específico
        registros_servicio = RegistroServicio.objects.filter(servicio=servicio)

        # Lista para almacenar los datos de cada cliente asociado al servicio
        client_data = []
        for registro in registros_servicio:
            # Buscamos al cliente relacionado con cada registro
            cliente = get_object_or_404(User, id=registro.cliente_id)
            
            # Se almacenan los datos de cada cliente en un diccionario
            client_data.append({
                'registro_id': registro.id,
                'nombre': cliente.get_full_name(),
                'observacion': registro.observacion if registro.observacion else '',   # Observación relacionada al cliente
                'archivo': registro.archivo.url if registro.archivo else None,  # URL del archivo si existe
                'odontograma': registro.odontograma.url if registro.odontograma else None,  # URL del odontograma si existe
            })

        # Se agrega la información del servicio y los datos de los clientes al contexto
        context['servicio'] = servicio
        context['client_data'] = client_data  # Cambiado a 'client_data' para coincidir con la plantilla
        
        # Se devuelve el contexto para que sea utilizado en la plantilla
        return context

#hasta aqui la lista de servicios y clientes

# Vista basada en clases para actualizar la información de un cliente.
@add_group_name_to_context
class UpdateInfoclienteView(UpdateView):

    model = Infocliente  # Modelo de datos que representa la información del cliente.
    fields = ['observacion', 'archivo', 'odontograma']  # Campos del modelo que se editarán en el formulario.
    template_name = 'update_infocliente.html'  # Plantilla HTML para el formulario de actualización.

    def get_success_url(self):
        """
        Obtiene la URL de redirección después de una actualización exitosa.

        Redirige a la vista de detalle del servicio, pasando el ID del servicio como argumento.
        """
        return reverse_lazy('servicio_detail', kwargs={'servicio_id': self.object.servicio.id})

    def form_valid(self, form):
        """
        Maneja la validación del formulario.

        Llama al método form_valid de la clase base y luego redirige a la URL de éxito.
        """
        response = super().form_valid(form)
        return redirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        """
        Obtiene el contexto para la plantilla.

        Agrega el nombre del servicio y el nombre completo del cliente al contexto para mostrarlos en la plantilla.
        """
        context = super().get_context_data(**kwargs)
        infocliente = self.get_object()
        context['servicio_name'] = infocliente.servicio.name  # Nombre del servicio relacionado.
        context['cliente_name'] = infocliente.cliente.nombre_completo  # Nombre completo del cliente.
        return context

    def get_object(self, queryset=None):
        """
        Obtiene el objeto Infocliente a actualizar.

        Busca el objeto Infocliente correspondiente al ID proporcionado en los argumentos de la URL.
        """
        infocliente_id = self.kwargs['infocliente_id']
        return get_object_or_404(Infocliente, id=infocliente_id)
    

