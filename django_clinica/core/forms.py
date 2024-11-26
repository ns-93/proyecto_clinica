from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordResetForm
from accounts.models import Profile
from .models import Servicios, Mouth, Reserva, About, Consulta
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit
from django.utils import timezone
from django import forms
from django.core.validators import MinLengthValidator, MinValueValidator, RegexValidator
import re


# Formulario de inicio de sesión heredado de AuthenticationForm de Django
class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label='Nombre de usuario o Correo electrónico',
        max_length=254,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'usuario@ejemplo.com'
        })
    )
    password = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese su contraseña'
        })
    )

# Formulario de registro de usuario

class RegisterForm(UserCreationForm):
    email = forms.EmailField(
        label='Correo electrónico',
        widget=forms.EmailInput(attrs={'class': 'form-control'}),
        error_messages={
            'invalid': 'Ingrese un correo electrónico válido',
            'required': 'El correo electrónico es requerido'
        }
    )
    
    first_name = forms.CharField(
        label='Nombre',
        validators=[
            RegexValidator(
                regex=r'^[a-zA-ZñÑáéíóúÁÉÍÓÚ\s]+$',
                message='El nombre solo debe contener letras'
            )
        ],
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    
    last_name = forms.CharField(
        label='Apellido',
        validators=[
            RegexValidator(
                regex=r'^[a-zA-ZñÑáéíóúÁÉÍÓÚ\s]+$',
                message='El apellido solo debe contener letras'
            )
        ],
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    
    rut = forms.CharField(
        max_length=12,
        required=True,
        validators=[
            RegexValidator(
                regex=r'^\d{1,2}\.\d{3}\.\d{3}[-][0-9kK]{1}$',
                message='Formato de RUT inválido (Ej: 12.345.678-9)'
            )
        ],
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '12.345.678-9'
        })
    )

    class Meta:
        model = User
        fields = ['username', 'rut', 'email', 'first_name', 'last_name', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Este correo electrónico ya está registrado')
        return email

    def clean_rut(self):
        rut = self.cleaned_data.get('rut')
        if not self.validar_rut(rut):
            raise forms.ValidationError('RUT inválido')
        if User.objects.filter(profile__rut=rut).exists():
            raise forms.ValidationError('Este RUT ya está registrado')
        return rut

    def validar_rut(rut):
        """
        Ejemplos de RUT válidos:
        - 11.111.111-1
        - 22.222.222-2 
        - 33.333.333-3
        - 44.444.444-4
        - 55.555.555-5
        """
        try:
            rut = rut.replace(".", "").replace("-", "")
            if not re.match(r'^\d{7,8}[0-9Kk]{1}$', rut):
                return False
            
            # Algoritmo de validación
            valor = rut[:-1]
            dv = rut[-1].upper()
            suma = 0
            multiplo = 2
            
            for i in reversed(valor):
                suma += int(i) * multiplo
                multiplo = 2 if multiplo == 7 else multiplo + 1
            
            resultado = 11 - (suma % 11)
            dv_esperado = {10: 'K', 11: '0'}.get(resultado, str(resultado))
            
            return dv == dv_esperado
            
        except (TypeError, ValueError):
            return False


# Formulario de actualización de usuario
class UserForm(forms.ModelForm):
    first_name = forms.CharField(
        label='Nombre',
        validators=[
            RegexValidator(
                regex=r'^[a-zA-ZñÑáéíóúÁÉÍÓÚ\s]+$',
                message='El nombre solo debe contener letras'
            )
        ],
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    
    last_name = forms.CharField(
        label='Apellido',
        validators=[
            RegexValidator(
                regex=r'^[a-zA-ZñÑáéíóúÁÉÍÓÚ\s]+$',
                message='El apellido solo debe contener letras'
            )
        ],
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    
    email = forms.EmailField(
        label='Correo electrónico',
        widget=forms.EmailInput(attrs={'class': 'form-control'}),
        error_messages={
            'invalid': 'Por favor ingrese un email válido'
        }
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

# Formulario de perfil de usuario
class ProfileForm(forms.ModelForm):
    rut = forms.CharField(
        label='RUT',
        max_length=12,
        validators=[
            RegexValidator(
                regex=r'^\d{1,2}\.\d{3}\.\d{3}[-][0-9kK]{1}$',
                message='Formato de RUT inválido (Ej: 12.345.678-9)'
            )
        ],
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '12.345.678-9'
        })
    )

    telephone = forms.CharField(
        label='Teléfono',
        validators=[
            RegexValidator(
                regex=r'^\+?569\d{8}$',
                message='Ingrese un número válido (+56912345678)'
            )
        ],
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '+56912345678'
        })
    )

    address = forms.CharField(
        label='Dirección',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    location = forms.CharField(
        label='Ciudad',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    image = forms.ImageField(
        label='Imagen de perfil',
        required=False,
        widget=forms.FileInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Profile
        fields = ['image', 'address', 'location', 'telephone', 'rut']

    def clean_rut(self):
        rut = self.cleaned_data.get('rut')
        if not self.validar_rut(rut):
            raise forms.ValidationError('RUT inválido')
        
        # Verificar si el RUT ya existe, excluyendo el usuario actual
        if self.instance and self.instance.pk:
            exists = Profile.objects.exclude(pk=self.instance.pk).filter(rut=rut).exists()
        else:
            exists = Profile.objects.filter(rut=rut).exists()
            
        if exists:
            raise forms.ValidationError('Este RUT ya está registrado')
        return rut

    def validar_rut(self, rut):
        try:
            rut = rut.replace(".", "").replace("-", "")
            if not re.match(r'^\d{7,8}[0-9Kk]{1}$', rut):
                return False
            
            valor = rut[:-1]
            dv = rut[-1].upper()
            suma = 0
            multiplo = 2
            
            for i in reversed(valor):
                suma += int(i) * multiplo
                multiplo = 2 if multiplo == 7 else multiplo + 1
            
            resultado = 11 - (suma % 11)
            dv_esperado = {10: 'K', 11: '0'}.get(resultado, str(resultado))
            
            return dv == dv_esperado
            
        except (TypeError, ValueError):
            return False


# Formulario de servicios
class ServiciosForm(forms.ModelForm):
    name = forms.CharField(
        label='Nombre del Servicio',
        validators=[
            MinLengthValidator(3, 'El nombre debe tener al menos 3 caracteres')
        ],
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese el nombre del servicio'
        })
    )

    description = forms.CharField(
        label='Descripción',
        validators=[
            MinLengthValidator(10, 'La descripción debe tener al menos 10 caracteres')
        ],
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Describa el servicio'
        })
    )

    n_procedimientos = forms.IntegerField(
        label='Número de Procedimientos',
        validators=[
            MinValueValidator(1, 'Debe haber al menos 1 procedimiento')
        ],
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'min': '1'
        })
    )

    status = forms.ChoiceField(
        choices=Servicios.STATUS_CHOICES,
        initial='S',
        label='Estado',
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Servicios
        fields = ['name', 'description', 'profesional', 'n_procedimientos', 'status']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        if user and user.groups.filter(name='profesionales').exists():
            self.fields['profesional'].queryset = User.objects.filter(id=user.id)
            self.fields['profesional'].initial = user
        elif user and (user.groups.filter(name='administradores').exists() or 
                    user.groups.filter(name='ejecutivos').exists()):
            self.fields['profesional'].required = True

        self.helper = FormHelper()
        self.helper.form_id = 'servicios-form'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-8'
        self.helper.layout = Layout(
            Field('name'),
            Field('description'),
            Field('profesional'),
            Field('n_procedimientos'),
            Field('status'),
            Submit('submit', 'Guardar', css_class='btn btn-primary mt-3')
        )

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if len(name.strip()) < 3:
            raise forms.ValidationError('El nombre es demasiado corto')
        return name.strip()

    def clean_description(self):
        description = self.cleaned_data.get('description')
        if len(description.strip()) < 10:
            raise forms.ValidationError('La descripción es demasiado corta')
        return description.strip()

# FORMULARIO DE NUEVO USUARIO
class UserCreationForm(forms.ModelForm):
    username = forms.CharField(
        label='Nombre de usuario',
        min_length=4,
        validators=[
            RegexValidator(
                regex=r'^[a-zA-Z0-9_]+$',
                message='El nombre de usuario solo puede contener letras, números y guiones bajos'
            )
        ],
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    first_name = forms.CharField(
        label='Nombre',
        validators=[
            RegexValidator(
                regex=r'^[a-zA-ZñÑáéíóúÁÉÍÓÚ\s]+$',
                message='El nombre solo debe contener letras'
            )
        ],
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    last_name = forms.CharField(
        label='Apellido',
        validators=[
            RegexValidator(
                regex=r'^[a-zA-ZñÑáéíóúÁÉÍÓÚ\s]+$',
                message='El apellido solo debe contener letras'
            )
        ],
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    email = forms.EmailField(
        label='Correo electrónico',
        widget=forms.EmailInput(attrs={'class': 'form-control'}),
        error_messages={
            'invalid': 'Por favor ingrese un email válido'
        }
    )

    password1 = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        min_length=8,
        help_text='La contraseña debe tener al menos 8 caracteres'
    )

    password2 = forms.CharField(
        label='Confirmar contraseña',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'user-creation-form'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-8'
        self.helper.layout = Layout(
            Field('username'),
            Field('first_name'),
            Field('last_name'),
            Field('email'),
            Field('password1'),
            Field('password2'),
            Submit('submit', 'Crear Usuario', css_class='btn btn-primary mt-3')
        )

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Este correo electrónico ya está registrado')
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('Este nombre de usuario ya existe')
        return username

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Las contraseñas no coinciden')
        return password2


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


class T44Form(forms.ModelForm):  # Corregir aquí
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


class AboutForm(forms.ModelForm):
    class Meta:
        model = About
        fields = ['mission', 'vision', 'values', 'contact_info', 'email', 'address', 'phone', 'images']


class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(label='Correo electrónico', max_length=254)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({'class': 'form-control'})

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError('No existe una cuenta con este correo electrónico.')
        return email


class ConsultaForm(forms.ModelForm):
    class Meta:
        model = Consulta
        fields = ['profesional', 'fecha', 'hora', 'precio']
        widgets = {
            'profesional': forms.Select(
                attrs={'class': 'form-control'}
            ),
            'fecha': forms.DateInput(
                attrs={
                    'class': 'form-control',
                    'type': 'date'
                }
            ),
            'hora': forms.TimeInput(
                attrs={
                    'class': 'form-control',
                    'type': 'time'
                }
            ),
            'precio': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'min': '0',
                    'step': '1000',
                    'placeholder': 'Ingrese el precio'
                }
            )
        }

    def clean_precio(self):
        precio = self.cleaned_data.get('precio')
        if precio is not None and precio < 0:
            raise forms.ValidationError('El precio no puede ser negativo')
        return precio


class ReservaConsultaForm(forms.ModelForm):  # Corregir aquí
    class Meta:
        model = Consulta
        fields = ['profesional', 'fecha', 'hora', 'precio']
        widgets = {
            'profesional': forms.TextInput(attrs={'readonly': 'readonly'}),
            'fecha': forms.DateInput(attrs={'type': 'date', 'readonly': 'readonly'}),
            'hora': forms.TimeInput(attrs={'type': 'time', 'readonly': 'readonly'}),
            'precio': forms.NumberInput(attrs={'readonly': 'readonly'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['precio'].widget.attrs['step'] = 1


class PagoForm(forms.Form):
    token = forms.CharField(widget=forms.HiddenInput())
    payment_method_id = forms.CharField(widget=forms.HiddenInput())
    email = forms.EmailField()
    
    


class ConsultaForm(forms.ModelForm):
    nombre_completo = forms.CharField(
        label='Nombre Completo',
        validators=[
            RegexValidator(
                regex=r'^[a-zA-ZñÑáéíóúÁÉÍÓÚ\s]+$',
                message='El nombre solo debe contener letras'
            ),
            MinLengthValidator(5, 'El nombre debe tener al menos 5 caracteres')
        ]
    )
    
    rut = forms.CharField(
        label='RUT',
        max_length=12,
        validators=[
            RegexValidator(
                regex=r'^\d{1,2}\.\d{3}\.\d{3}[-][0-9kK]{1}$',
                message='Formato de RUT inválido (Ej: 12.345.678-9)'
            )
        ]
    )
    
    telefono = forms.CharField(
        label='Teléfono',
        validators=[
            RegexValidator(
                regex=r'^\+?569\d{8}$',
                message='Ingrese un número válido (+56912345678)'
            )
        ]
    )
    
    email = forms.EmailField(
        label='Email',
        error_messages={
            'invalid': 'Por favor ingrese un email válido'
        }
    )

    class Meta:
        model = Consulta
        fields = ['nombre_completo', 'rut', 'telefono', 'email', 'fecha', 'hora', 'profesional', 'precio']
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date'}),
            'hora': forms.TimeInput(attrs={'type': 'time'}),
            'precio': forms.NumberInput(attrs={'readonly': 'readonly'}),
        }

    def clean_rut(self):
        rut = self.cleaned_data.get('rut')
        if not self.validar_rut(rut):
            raise forms.ValidationError('RUT inválido')
        return rut

    def clean_telefono(self):
        telefono = self.cleaned_data.get('telefono')
        if not telefono.startswith('+569'):
            raise forms.ValidationError('El teléfono debe comenzar con +569')
        return telefono

    def validar_rut(self, rut):
        try:
            rut = rut.replace(".", "").replace("-", "")
            if not re.match(r'^\d{7,8}[0-9Kk]{1}$', rut):
                return False
            
            valor = rut[:-1]
            dv = rut[-1].upper()
            suma = 0
            multiplo = 2
            
            for i in reversed(valor):
                suma += int(i) * multiplo
                multiplo = 2 if multiplo == 7 else multiplo + 1
            
            resultado = 11 - (suma % 11)
            dv_esperado = {10: 'K', 11: '0'}.get(resultado, str(resultado))
            
            return dv == dv_esperado
            
        except (TypeError, ValueError):
            return False

class PagoForm(forms.Form):
    token = forms.CharField(widget=forms.HiddenInput())
    payment_method_id = forms.CharField(widget=forms.HiddenInput())
    email = forms.EmailField(
        error_messages={
            'required': 'El email es requerido',
            'invalid': 'Por favor ingrese un email válido'
        })