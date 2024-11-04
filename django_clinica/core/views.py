from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.views.generic import TemplateView
from django.contrib.auth.models import Group
from .forms import RegisterForm, UserForm, ProfileForm
from django.views import View
from django.utils.decorators import method_decorator
from .models import Servicios, RegistroServicio
# Create your views here.

# FUNCION PARA CONVERTIR EL PLURAL DE UN GRUPO A SU SINGULAR
def plural_to_singular(plural):
    # Diccionario de palabras
    plural_singular = {
        "clientes": "cliente",
        "profesionales": "profesional",
        "ejecutivos": "ejecutivo",
        "administradores": "administrador",
    }

    return plural_singular.get(plural, "error")

# OBTENER COLOR Y GRUPO DE UN USUARIO
def get_group_and_color(user):
    group = user.groups.first()
    group_id = None
    group_name = None
    group_name_singular = None
    color = None

    if group:
        if group.name == 'clientes':
            color = 'bg-primary'
        elif group.name == 'profesionales':
            color = 'bg-success'
        elif group.name == 'ejecutivos':
            color = 'bg-danger'
        elif group.name == 'administradores':
            color = 'bg-info'

        group_id = group.id
        group_name = group.name
        group_name_singular = plural_to_singular(group.name)

    return group_id, group_name, group_name_singular, color

# DECORADOR PERSONALIZADO
def add_group_name_to_context(view_class):
    original_dispatch = view_class.dispatch

    def dispatch(self, request, *args, **kwargs):
        user = self.request.user
        group_id, group_name, group_name_singular, color = get_group_and_color(user)

        context = {
            'group_name': group_name,
            'group_name_singular': group_name_singular,
            'color': color
        }

        self.extra_context = context
        return original_dispatch(self, request, *args, **kwargs)

    view_class.dispatch = dispatch
    return view_class

#
#class CustomTemplateView(TemplateView):
    group_name= None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        group_name = None
        if user.is_authenticated:
            group = Group.objects.filter(user=user).first()
            if group:
                group_name = group.name
        context['group_name'] = group_name
        return context




#pagina principal
@add_group_name_to_context
class HomeView(TemplateView):
    template_name= 'home.html'


#pagina de precios y ofertas
@add_group_name_to_context
class PricingView(TemplateView):
    template_name= 'pricing.html'


#registro de usuarios

class RegisterView(View):

    def get(self, request):
        data = {
            'form': RegisterForm()
        }
        return render(request, 'registration/register.html', data)

    def post(self, request):  # Cambiar Post a post
        user_creation_form = RegisterForm(data=request.POST)  # Cambiar Post a POST
        if user_creation_form.is_valid():
            user_creation_form.save()
            user = authenticate(username=user_creation_form.cleaned_data['username'], password=user_creation_form.cleaned_data['password1'])
            login(request, user)
            return redirect('home')
        
        data = {
            'form': user_creation_form
        }
        return render(request, 'registration/register.html', data)
    

#pagina de perfil
@add_group_name_to_context
class ProfileView(TemplateView):
    template_name = 'profile/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['user_form']= UserForm(instance=user)
        context['profile_form']= ProfileForm(instance=user.profile)
        
        return context     
    
    def post(self, request, *arg, **kwargs):
        user = self.request.user
        user_form = UserForm(request.POST, instance=user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=user.profile)

        #si los datos son validos
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()

            return redirect('profile')
        
        #si los datos no son validos
        context = self.get_context_data()
        context ['user_form'] = user_form
        context ['profile_form'] = profile_form
        return render(request, 'profile/profile.html', context)


# MOSTRAR TODOS LOS servicios

@add_group_name_to_context
class ServiciosView(TemplateView):
    template_name = 'servicios.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        servicios = Servicios.objects.all().order_by('-id')
        cliente = self.request.user if self.request.user.is_authenticated else None

        for item in servicios:
            if cliente:
                # importar RegistroServicio
                registration = RegistroServicio.objects.filter(servicio=item, cliente=cliente).first()
                item.is_enrolled = registration is not None
            else:
                item.is_enrolled = False

            enrollment_count = RegistroServicio.objects.filter(servicio=item).count()
            item.enrollment_count = enrollment_count

        context['servicios'] = servicios
        return context
    