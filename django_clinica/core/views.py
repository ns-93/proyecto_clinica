from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.views.generic import TemplateView, CreateView, UpdateView, DeleteView
from django.contrib.auth.models import Group
from .forms import RegisterForm, UserForm, ProfileForm, ServiciosForm  
from django.views import View
from django.utils.decorators import method_decorator
from .models import Servicios, RegistroServicio
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
        context['user_form']= UserForm(instance=user)
        context['profile_form']= ProfileForm(instance=user.profile)
        
        return context     
    
    def post(self, request, *arg, **kwargs):
        # Procesa los formularios de perfil y usuario
        user = self.request.user
        user_form = UserForm(request.POST, instance=user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=user.profile)

        #si los datos son validos
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()  # Guarda el formulario de usuario
            profile_form.save()  # Guarda el formulario de perfil

            return redirect('profile') # Redirige al perfil del usuario
        
        #si los datos no son validos
        context = self.get_context_data()
        context ['user_form'] = user_form
        context ['profile_form'] = profile_form
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

