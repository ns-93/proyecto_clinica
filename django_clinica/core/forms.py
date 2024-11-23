from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from accounts.models import Profile
from .models import Servicios, Mouth, Reserva
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit
from django.utils import timezone


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
        fields = ['first_name', 'last_name', 'email']  # Eliminar 'rut' del formulario

# Formulario de perfil de usuario
class ProfileForm(forms.ModelForm):
    class Meta:
        # Utiliza el modelo Profile (perfil de usuario personalizado)
        # Define los campos de perfil que se pueden actualizar
        model = Profile
        fields = ['image', 'address', 'location', 'telephone', 'rut']  # Añadir 'rut' al formulario


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
    


#formulario de odontograma
MOUTH_CHOICES = (
    ('sano', 'sano'),
    ('c1', 'c1'),
    ('c2', 'c2'),
    ('c3', 'c3'),
    ('c4', 'c4'),
    ('c5', 'c5'),
    ('r1', 'r1'),
    ('r2', 'r2'),
    ('r3', 'r3'),
    ('r4', 'r4'),
    ('r5', 'r5'),
    ('e', 'e'),
    ('N', 'N'),
    ('PL', 'PL'),
    ('p', 'p'),
    ('z', 'z'),
    ('d', 'd'),
    ('g', 'g'),
)


class T11Form(forms.ModelForm):
    t_11 = forms.MultipleChoiceField(
        choices=MOUTH_CHOICES,
        required=False,
        widget=forms.CheckboxSelectMultiple,
        #label='',
    )

    class Meta:
        model = Mouth
        fields = ['t_11', ]


class T12Form(forms.ModelForm):
    t_12 = forms.MultipleChoiceField(
        choices=MOUTH_CHOICES,
        required=False,
        widget=forms.CheckboxSelectMultiple,
        #label='',
    )

    class Meta:
        model = Mouth
        fields = ['t_12', ]


class T13Form(forms.ModelForm):
    t_13 = forms.MultipleChoiceField(
        choices=MOUTH_CHOICES,
        required=False,
        widget=forms.CheckboxSelectMultiple,
        #label='',
    )

    class Meta:
        model = Mouth
        fields = ['t_13', ]


class T14Form(forms.ModelForm):
    t_14 = forms.MultipleChoiceField(
        choices=MOUTH_CHOICES,
        required=False,
        widget=forms.CheckboxSelectMultiple,
        #label='',
    )

    class Meta:
        model = Mouth
        fields = ['t_14', ]


class T15Form(forms.ModelForm):
    t_15 = forms.MultipleChoiceField(
        choices=MOUTH_CHOICES,
        required=False,
        widget=forms.CheckboxSelectMultiple,
        #label='',
    )

    class Meta:
        model = Mouth
        fields = ['t_15', ]


class T16Form(forms.ModelForm):
    t_16 = forms.MultipleChoiceField(
        choices=MOUTH_CHOICES,
        required=False,
        widget=forms.CheckboxSelectMultiple,
        #label='',
    )

    class Meta:
        model = Mouth
        fields = ['t_16', ]


class T17Form(forms.ModelForm):
    t_17 = forms.MultipleChoiceField(
        choices=MOUTH_CHOICES,
        required=False,
        widget=forms.CheckboxSelectMultiple,
        #label='',
    )

    class Meta:
        model = Mouth
        fields = ['t_17', ]


class T18Form(forms.ModelForm):
    t_18 = forms.MultipleChoiceField(
        choices=MOUTH_CHOICES,
        required=False,
        widget=forms.CheckboxSelectMultiple,
        #label='',
    )

    class Meta:
        model = Mouth
        fields = ['t_18', ]


class T21Form(forms.ModelForm):
    t_21 = forms.MultipleChoiceField(
        choices=MOUTH_CHOICES,
        required=False,
        widget=forms.CheckboxSelectMultiple,
        #label='',
    )

    class Meta:
        model = Mouth
        fields = ['t_21', ]


class T22Form(forms.ModelForm):
    t_22 = forms.MultipleChoiceField(
        choices=MOUTH_CHOICES,
        required=False,
        widget=forms.CheckboxSelectMultiple,
        #label='',
    )

    class Meta:
        model = Mouth
        fields = ['t_22', ]


class T23Form(forms.ModelForm):
    t_23 = forms.MultipleChoiceField(
        choices=MOUTH_CHOICES,
        required=False,
        widget=forms.CheckboxSelectMultiple,
        #label='',
    )

    class Meta:
        model = Mouth
        fields = ['t_23', ]


class T24Form(forms.ModelForm):
    t_24 = forms.MultipleChoiceField(
        choices=MOUTH_CHOICES,
        required=False,
        widget=forms.CheckboxSelectMultiple,
        #label='',
    )

    class Meta:
        model = Mouth
        fields = ['t_24', ]


class T25Form(forms.ModelForm):
    t_25 = forms.MultipleChoiceField(
        choices=MOUTH_CHOICES,
        required=False,
        widget=forms.CheckboxSelectMultiple,
        #label='',
    )

    class Meta:
        model = Mouth
        fields = ['t_25', ]


class T26Form(forms.ModelForm):
    t_26 = forms.MultipleChoiceField(
        choices=MOUTH_CHOICES,
        required=False,
        widget=forms.CheckboxSelectMultiple,
        #label='',
    )

    class Meta:
        model = Mouth
        fields = ['t_26', ]


class T27Form(forms.ModelForm):
    t_27 = forms.MultipleChoiceField(
        choices=MOUTH_CHOICES,
        required=False,
        widget=forms.CheckboxSelectMultiple,
        #label='',
    )

    class Meta:
        model = Mouth
        fields = ['t_27', ]


class T28Form(forms.ModelForm):
    t_28 = forms.MultipleChoiceField(
        choices=MOUTH_CHOICES,
        required=False,
        widget=forms.CheckboxSelectMultiple,
        #label='',
    )

    class Meta:
        model = Mouth
        fields = ['t_28', ]


class T31Form(forms.ModelForm):
    t_31 = forms.MultipleChoiceField(
        choices=MOUTH_CHOICES,
        required=False,
        widget=forms.CheckboxSelectMultiple,
        #label='',
    )

    class Meta:
        model = Mouth
        fields = ['t_31', ]


class T32Form(forms.ModelForm):
    t_32 = forms.MultipleChoiceField(
        choices=MOUTH_CHOICES,
        required=False,
        widget=forms.CheckboxSelectMultiple,
        #label='',
    )

    class Meta:
        model = Mouth
        fields = ['t_32', ]


class T33Form(forms.ModelForm):
    t_33 = forms.MultipleChoiceField(
        choices=MOUTH_CHOICES,
        required=False,
        widget=forms.CheckboxSelectMultiple,
        #label='',
    )

    class Meta:
        model = Mouth
        fields = ['t_33', ]


class T34Form(forms.ModelForm):
    t_34 = forms.MultipleChoiceField(
        choices=MOUTH_CHOICES,
        required=False,
        widget=forms.CheckboxSelectMultiple,
        #label='',
    )

    class Meta:
        model = Mouth
        fields = ['t_34', ]


class T35Form(forms.ModelForm):
    t_35 = forms.MultipleChoiceField(
        choices=MOUTH_CHOICES,
        required=False,
        widget=forms.CheckboxSelectMultiple,
        #label='',
    )

    class Meta:
        model = Mouth
        fields = ['t_35', ]


class T36Form(forms.ModelForm):
    t_36 = forms.MultipleChoiceField(
        choices=MOUTH_CHOICES,
        required=False,
        widget=forms.CheckboxSelectMultiple,
        #label='',
    )

    class Meta:
        model = Mouth
        fields = ['t_36', ]


class T37Form(forms.ModelForm):
    t_37 = forms.MultipleChoiceField(
        choices=MOUTH_CHOICES,
        required=False,
        widget=forms.CheckboxSelectMultiple,
        #label='',
    )

    class Meta:
        model = Mouth
        fields = ['t_37', ]


class T38Form(forms.ModelForm):
    t_38 = forms.MultipleChoiceField(
        choices=MOUTH_CHOICES,
        required=False,
        widget=forms.CheckboxSelectMultiple,
        #label='',
    )

    class Meta:
        model = Mouth
        fields = ['t_38', ]


class T41Form(forms.ModelForm):
    t_41 = forms.MultipleChoiceField(
        choices=MOUTH_CHOICES,
        required=False,
        widget=forms.CheckboxSelectMultiple,
        #label='',
    )

    class Meta:
        model = Mouth
        fields = ['t_41', ]


class T42Form(forms.ModelForm):
    t_42 = forms.MultipleChoiceField(
        choices=MOUTH_CHOICES,
        required=False,
        widget=forms.CheckboxSelectMultiple,
        #label='',
    )

    class Meta:
        model = Mouth
        fields = ['t_42', ]


class T43Form(forms.ModelForm):
    t_43 = forms.MultipleChoiceField(
        choices=MOUTH_CHOICES,
        required=False,
        widget=forms.CheckboxSelectMultiple,
        #label='',
    )

    class Meta:
        model = Mouth
        fields = ['t_43', ]


class T44Form(forms.ModelForm):
    t_44 = forms.MultipleChoiceField(
        choices=MOUTH_CHOICES,
        required=False,
        widget=forms.CheckboxSelectMultiple,
        #label='',
    )

    class Meta:
        model = Mouth
        fields = ['t_44', ]


class T45Form(forms.ModelForm):
    t_45 = forms.MultipleChoiceField(
        choices=MOUTH_CHOICES,
        required=False,
        widget=forms.CheckboxSelectMultiple,
        #label='',
    )

    class Meta:
        model = Mouth
        fields = ['t_45', ]


class T46Form(forms.ModelForm):
    t_46 = forms.MultipleChoiceField(
        choices=MOUTH_CHOICES,
        required=False,
        widget=forms.CheckboxSelectMultiple,
        #label='',
    )

    class Meta:
        model = Mouth
        fields = ['t_46', ]


class T47Form(forms.ModelForm):
    t_47 = forms.MultipleChoiceField(
        choices=MOUTH_CHOICES,
        required=False,
        widget=forms.CheckboxSelectMultiple,
        #label='',
    )

    class Meta:
        model = Mouth
        fields = ['t_47', ]


class T48Form(forms.ModelForm):
    t_48 = forms.MultipleChoiceField(
        choices=MOUTH_CHOICES,
        required=False,
        widget=forms.CheckboxSelectMultiple,
        #label='',
    )

    class Meta:
        model = Mouth
        fields = ['t_48', ]


class T51Form(forms.ModelForm):
    t_51 = forms.MultipleChoiceField(
        choices=MOUTH_CHOICES,
        required=False,
        widget=forms.CheckboxSelectMultiple,
        #label='',
    )

    class Meta:
        model = Mouth
        fields = ['t_51', ]


class T52Form(forms.ModelForm):
    t_52 = forms.MultipleChoiceField(
        choices=MOUTH_CHOICES,
        required=False,
        widget=forms.CheckboxSelectMultiple,
        #label='',
    )

    class Meta:
        model = Mouth
        fields = ['t_52', ]


class T53Form(forms.ModelForm):
    t_53 = forms.MultipleChoiceField(
        choices=MOUTH_CHOICES,
        required=False,
        widget=forms.CheckboxSelectMultiple,
        #label='',
    )

    class Meta:
        model = Mouth
        fields = ['t_53', ]


class T54Form(forms.ModelForm):
    t_54 = forms.MultipleChoiceField(
        choices=MOUTH_CHOICES,
        required=False,
        widget=forms.CheckboxSelectMultiple,
        #label='',
    )

    class Meta:
        model = Mouth
        fields = ['t_54', ]


class T55Form(forms.ModelForm):
    t_55 = forms.MultipleChoiceField(
        choices=MOUTH_CHOICES,
        required=False,
        widget=forms.CheckboxSelectMultiple,
        #label='',
    )

    class Meta:
        model = Mouth
        fields = ['t_55', ]


class T61Form(forms.ModelForm):
    t_61 = forms.MultipleChoiceField(
        choices=MOUTH_CHOICES,
        required=False,
        widget=forms.CheckboxSelectMultiple,
        #label='',
    )

    class Meta:
        model = Mouth
        fields = ['t_61', ]


class T62Form(forms.ModelForm):
    t_62 = forms.MultipleChoiceField(
        choices=MOUTH_CHOICES,
        required=False,
        widget=forms.CheckboxSelectMultiple,
        #label='',
    )

    class Meta:
        model = Mouth
        fields = ['t_62', ]


class T63Form(forms.ModelForm):
    t_63 = forms.MultipleChoiceField(
        choices=MOUTH_CHOICES,
        required=False,
        widget=forms.CheckboxSelectMultiple,
        #label='',
    )

    class Meta:
        model = Mouth
        fields = ['t_63', ]


class T64Form(forms.ModelForm):
    t_64 = forms.MultipleChoiceField(
        choices=MOUTH_CHOICES,
        required=False,
        widget=forms.CheckboxSelectMultiple,
        #label='',
    )

    class Meta:
        model = Mouth
        fields = ['t_64', ]


class T65Form(forms.ModelForm):
    t_65 = forms.MultipleChoiceField(
        choices=MOUTH_CHOICES,
        required=False,
        widget=forms.CheckboxSelectMultiple,
        #label='',
    )

    class Meta:
        model = Mouth
        fields = ['t_65', ]


class T71Form(forms.ModelForm):
    t_71 = forms.MultipleChoiceField(
        choices=MOUTH_CHOICES,
        required=False,
        widget=forms.CheckboxSelectMultiple,
        #label='',
    )

    class Meta:
        model = Mouth
        fields = ['t_71', ]


class T72Form(forms.ModelForm):
    t_72 = forms.MultipleChoiceField(
        choices=MOUTH_CHOICES,
        required=False,
        widget=forms.CheckboxSelectMultiple,
        #label='',
    )

    class Meta:
        model = Mouth
        fields = ['t_72', ]


class T73Form(forms.ModelForm):
    t_73 = forms.MultipleChoiceField(
        choices=MOUTH_CHOICES,
        required=False,
        widget=forms.CheckboxSelectMultiple,
        #label='',
    )

    class Meta:
        model = Mouth
        fields = ['t_73', ]


class T74Form(forms.ModelForm):
    t_74 = forms.MultipleChoiceField(
        choices=MOUTH_CHOICES,
        required=False,
        widget=forms.CheckboxSelectMultiple,
        #label='',
    )

    class Meta:
        model = Mouth
        fields = ['t_74', ]


class T75Form(forms.ModelForm):
    t_75 = forms.MultipleChoiceField(
        choices=MOUTH_CHOICES,
        required=False,
        widget=forms.CheckboxSelectMultiple,
        #label='',
    )

    class Meta:
        model = Mouth
        fields = ['t_75', ]


class T81Form(forms.ModelForm):
    t_81 = forms.MultipleChoiceField(
        choices=MOUTH_CHOICES,
        required=False,
        widget=forms.CheckboxSelectMultiple,
        #label='',
    )

    class Meta:
        model = Mouth
        fields = ['t_81', ]


class T82Form(forms.ModelForm):
    t_82 = forms.MultipleChoiceField(
        choices=MOUTH_CHOICES,
        required=False,
        widget=forms.CheckboxSelectMultiple,
        #label='',
    )

    class Meta:
        model = Mouth
        fields = ['t_82', ]


class T83Form(forms.ModelForm):
    t_83 = forms.MultipleChoiceField(
        choices=MOUTH_CHOICES,
        required=False,
        widget=forms.CheckboxSelectMultiple,
        #label='',
    )

    class Meta:
        model = Mouth
        fields = ['t_83', ]


class T84Form(forms.ModelForm):
    t_84 = forms.MultipleChoiceField(
        choices=MOUTH_CHOICES,
        required=False,
        widget=forms.CheckboxSelectMultiple,
        #label='',
    )

    class Meta:
        model = Mouth
        fields = ['t_84', ]


class T85Form(forms.ModelForm):
    t_85 = forms.MultipleChoiceField(
        choices=MOUTH_CHOICES,
        required=False,
        widget=forms.CheckboxSelectMultiple,
        #label='',
    )

    class Meta:
        model = Mouth
        fields = ['t_85', ]


class ReservaForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = ['fecha', 'hora']
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date'}),
            'hora': forms.TimeInput(attrs={'type': 'time'}),
        }

    def clean_fecha(self):
        fecha = self.cleaned_data.get('fecha')
        if fecha < timezone.now().date():
            raise forms.ValidationError('No se puede crear una reserva en una fecha pasada.')
        return fecha
