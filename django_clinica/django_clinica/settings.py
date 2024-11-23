"""
Django settings for django_clinica project.

Generated by 'django-admin startproject' using Django 5.1.2.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""
import os
from pathlib import Path

# Se define la variable BASE_DIR que contiene la ruta base del proyecto.
# Esto nos permite construir rutas relativas de manera más sencilla.
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-d+!ke&9(zy#zhtevt-$ryf)*ukx6ufkr!zjoug0e@yx_dv0)l$'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'accounts.apps.AccountsConfig',
    'core',
    'crispy_forms',
    'crispy_bootstrap5',
]

# Configuración de crispy-forms para usar el framework de diseño bootstrap5.
CRISPY_ALLOWED_TEMPLATE_PACKS = 'bootstrap5'

CRISPY_TEMPLATE_PACK = 'bootstrap5'

# Middleware de seguridad y autenticación para proteger la aplicación.
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Configuración de URL raíz
ROOT_URLCONF = 'django_clinica.urls'

# Configuración de plantillas
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media',
            ],
        },
    },
]

# Configuración de WSGI y ASGI
WSGI_APPLICATION = 'django_clinica.wsgi.application'

# Configuración de la base de datos
# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Validadores de contraseñas
# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

# Lista de validadores de contraseñas que se utilizan para verificar la seguridad de las contraseñas de los usuarios.
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

# Código de idioma, en este caso español de Chile.
LANGUAGE_CODE = 'es-cl'
# Zona horaria. Debes ajustarla según la ubicación del proyecto.
TIME_ZONE = 'UTC'
# Habilita la internacionalización para soportar múltiples idiomas.
USE_I18N = True
# Habilita el soporte para zonas horarias.
USE_TZ = True

# Configuración de archivos estáticos
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

# URL de los archivos estáticos, como CSS y JS.
STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Configuración de archivos multimedia
# Definimos la carpeta Media files para el manejo de imagenes
# URL y ruta del directorio para almacenar archivos subidos, como imágenes y documentos.
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, "media")  # Ruta completa para los archivos multimedia.

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]


# Configuración de redirección de login/logout
#login y logout
# URL a la que el usuario será redirigido después de iniciar sesión.
LOGIN_REDIRECT_URL = 'home'
# URL a la que el usuario será redirigido después de cerrar sesión.
LOGOUT_REDIRECT_URL = 'home'


AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',  # Backend predeterminado
    'accounts.backends.EmailOrUsernameBackend',   # Backend personalizado
]

# Configuración de correo electrónico
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.example.com'  # Cambia esto por tu servidor SMTP
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'tu_email@example.com'
EMAIL_HOST_PASSWORD = 'tu_contraseña'

