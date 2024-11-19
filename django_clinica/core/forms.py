from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from accounts.models import Profile
from .models import Servicios
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit


# Formulario de inicio de sesión heredado de AuthenticationForm de Django
"""class LoginForm(AuthenticationForm):
    pass"""

# Formularios personalizados para la aplicación de cuentas
class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Nombre de usuario o Correo electrónico', max_length=254)
    password = forms.CharField(label='Contraseña', widget=forms.PasswordInput)

# Formulario de registro de usuario
class RegisterForm(UserCreationForm):
    email = forms.EmailField(label='Correo electrónico')
    first_name = forms.CharField(label='Nombre')
    last_name = forms.CharField(label='Apellido')
    rut = forms.CharField(max_length=12, required=True)

# Configuración de metadatos para el formulario
    class Meta:
        # Especifica que este formulario se basa en el modelo User de Django
        # Define los campos que se mostrarán en el formulario de registro
        model = User
        fields = ['username','rut', 'email', 'first_name', 'last_name', 'password1', 'password2']

# Método de validación para el campo de correo electrónico
    def clean_email(self):
        email_field = self.cleaned_data['email']
        # Verifica si el correo electrónico ya está registrado
        if User.objects.filter(email=email_field).exists():
            raise forms.ValidationError('Este correo electrónico ya está registrado')
        return email_field    # Retorna el correo si no está registrado

# Formulario de actualización de usuario
class UserForm(forms.ModelForm):
        class Meta:
            model = User
            fields = ['first_name', 'last_name']  # Define los campos a mostrar en el formulario de actualización de usuario

# Formulario de perfil de usuario
class ProfileForm(forms.ModelForm):
        class Meta:
            # Utiliza el modelo Profile (perfil de usuario personalizado)
            # Define los campos de perfil que se pueden actualizar
            model = Profile
            fields = ['image', 'address', 'location', 'telephone', 'rut']    


# Formulario de servicios
class ServiciosForm(forms.ModelForm):
    # Campo de selección para elegir un profesional del grupo 'profesionales'
    profesional = forms.ModelChoiceField(queryset=User.objects.filter(groups__name='profesionales'), label='Profesional')
    # Campo de selección para el estado del servicio
    status = forms.ChoiceField(choices=Servicios.STATUS_CHOICES, initial='S', label='Estado')
    # Campo de texto para la descripción del servicio con un widget personalizado
    description = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), label='Descripción')
    
    # Configuración de metadatos para el formulario
    # Utiliza el modelo Servicios
    # Define los campos del formulario para crear o actualizar un servicio
    class Meta:
        model = Servicios
        fields = ['name', 'description', 'profesional', 'n_procedimientos', 'status']

# Configuración de diseño del formulario usando FormHelper (de django-crispy-forms)
    helper = FormHelper()
    helper.layout = Layout(
        Field('name'),
        Field('description'),
        Field('profesional'),
        Field('n_procedimientos'),
        Field('status'),
        Submit('submit', 'Submit') # Botón de envío para el formulario
    )     


# FORMULARIO DE NUEVO USUARIO
class UserCreationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

    # Configuración de diseño del formulario usando FormHelper (de django-crispy-forms)
    helper = FormHelper()
    helper.layout = Layout(
        Field('username'),
        Field('first_name'),
        Field('last_name'),
        Field('email'),
        Submit('submit', 'Crear Usuario')  # Botón de envío para el formulario
    )