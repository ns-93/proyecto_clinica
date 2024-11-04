from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from accounts.models import Profile
from .models import Servicios
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit

class LoginForm(AuthenticationForm):
    pass

#formulario de registro
class RegisterForm(UserCreationForm):
    email = forms.EmailField(label='Correo electrónico')
    first_name = forms.CharField(label='Nombre')
    last_name = forms.CharField(label='Apellido')


    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']

    def clean_email(self):
        email_field = self.cleaned_data['email']

        if User.objects.filter(email=email_field).exists():
            raise forms.ValidationError('Este correo electrónico ya está registrado')
        return email_field

class UserForm(forms.ModelForm):
        class Meta:
            model = User
            fields = ['first_name', 'last_name']

#formulario de perfil
class ProfileForm(forms.ModelForm):
        class Meta:
            model = Profile
            fields = ['image', 'address', 'location', 'telephone']    

#formulario de servicios

class ServiciosForm(forms.ModelForm):
    profesional = forms.ModelChoiceField(queryset=User.objects.filter(groups__name='profesionales'), label='Profesional')
    status = forms.ChoiceField(choices=Servicios.STATUS_CHOICES, initial='S', label='Estado')
    description = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), label='Descripción')
    
    class Meta:
        model = Servicios
        fields = ['name', 'description', 'profesional', 'n_procedimientos', 'status']

    helper = FormHelper()
    helper.layout = Layout(
        Field('name'),
        Field('description'),
        Field('profesional'),
        Field('n_procedimientos'),
        Field('status'),
        Submit('submit', 'Submit')
    )     
