import re
from django.db.models.signals import post_save
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator, FileExtensionValidator
from django.core.exceptions import ValidationError
import os
from django.dispatch import receiver
from django.core.exceptions import ObjectDoesNotExist
import logging

logger = logging.getLogger(__name__)

# Create your models here.
# Creacion perfiles de usuarios
# Creación de modelos para la aplicación
# Definición del modelo Profile para perfiles de usuarios

class Profile(models.Model):
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE, 
        related_name='profile', 
        verbose_name='Usuario'
    )
    
    image = models.ImageField(
        default='users/usuario_defecto.jpg', 
        upload_to='users/', 
        verbose_name='Imagen de perfil',
        validators=[
            FileExtensionValidator(
                allowed_extensions=['jpg', 'jpeg', 'png'],
                message='Solo se permiten imágenes JPG o PNG'
            )
        ]
    )
    
    address = models.CharField(
        max_length=150, 
        null=True, 
        blank=True, 
        verbose_name='Dirección',
        validators=[
            RegexValidator(
                regex=r'^[a-zA-Z0-9\s,.-]+$',
                message='La dirección contiene caracteres no válidos'
            )
        ]
    )
    
    location = models.CharField(
        max_length=100, 
        null=True, 
        blank=True, 
        verbose_name='Localidad',
        validators=[
            RegexValidator(
                regex=r'^[a-zA-ZñÑáéíóúÁÉÍÓÚ\s]+$',
                message='La localidad solo debe contener letras'
            )
        ]
    )
    
    telephone = models.CharField(
        max_length=12, 
        null=True, 
        blank=True, 
        verbose_name='Teléfono',
        validators=[
            RegexValidator(
                regex=r'^\+?569\d{8}$',
                message='Ingrese un número válido (+56912345678)'
            )
        ]
    )
    
    rut = models.CharField(
        max_length=12, 
        null=True, 
        blank=True, 
        verbose_name='Rut',
        validators=[
            RegexValidator(
                regex=r'^\d{1,2}\.\d{3}\.\d{3}[-][0-9kK]{1}$',
                message='Formato de RUT inválido (Ej: 12.345.678-9)'
            )
        ]
    )
    
    created_by_admin = models.BooleanField(
        default=True, 
        blank=True, 
        null=True, 
        verbose_name='Creado por Admin'
    )

    def clean(self):
        if self.image:
            # Validar tamaño de imagen
            if self.image.size > 2*1024*1024:  # 2MB
                raise ValidationError({
                    'image': 'La imagen no debe superar los 2MB'
                })
        
        # Validar RUT
        if self.rut:
            if not self.validar_rut(self.rut):
                raise ValidationError({
                    'rut': 'RUT inválido'
                })
                
    def validar_rut(self, rut):
        try:
            # Limpiar el RUT de puntos y guión
            rut = rut.replace(".", "").replace("-", "")
            
            # Validar formato básico
            if not re.match(r'^\d{7,8}[0-9Kk]{1}$', rut):
                return False
            
            # Separar número y dígito verificador
            valor = rut[:-1]
            dv = rut[-1].upper()
            
            # Calcular dígito verificador
            suma = 0
            multiplo = 2
            
            for i in reversed(valor):
                suma += int(i) * multiplo
                multiplo = 2 if multiplo == 7 else multiplo + 1
            
            resultado = 11 - (suma % 11)
            dv_esperado = {10: 'K', 11: '0'}.get(resultado, str(resultado))
            
            return dv == dv_esperado
            
        except (TypeError, ValueError) as e:
            logger.error(f"Error validando RUT: {str(e)}")
            return False

    class Meta:
        verbose_name = 'perfil'
        verbose_name_plural = 'perfiles'
        ordering = ['-id']
    
    # Representación en texto de cada instancia del modelo, retornando el nombre de usuario
    def __str__(self):
        return self.user.username
    
# Función para crear un perfil automáticamente al crear un usuario
"""@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)"""

# Función para guardar el perfil de usuario al guardar el usuario
"""@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()"""

# Conecta las señales post_save al modelo User para crear y guardar perfiles automáticamente
"""post_save.connect(create_user_profile, sender=User)
post_save.connect(save_user_profile, sender=User)
"""


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    try:
        if created:
            logger.info(f"Creando perfil para usuario: {instance.username}")
            Profile.objects.create(
                user=instance,
                created_by_admin=True if instance.is_staff else False
            )
            logger.info(f"Perfil creado exitosamente para: {instance.username}")
    except Exception as e:
        logger.error(f"Error al crear perfil para {instance.username}: {str(e)}")
        raise

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    try:
        if hasattr(instance, 'profile'):
            logger.info(f"Actualizando perfil de usuario: {instance.username}")
            instance.profile.save()
            logger.info(f"Perfil actualizado exitosamente para: {instance.username}")
        else:
            logger.warning(f"Usuario {instance.username} no tiene perfil, creando uno nuevo")
            Profile.objects.create(
                user=instance,
                created_by_admin=True if instance.is_staff else False
            )
    except ObjectDoesNotExist:
        logger.error(f"Perfil no encontrado para {instance.username}")
        Profile.objects.create(
            user=instance,
            created_by_admin=True if instance.is_staff else False
        )
    except Exception as e:
        logger.error(f"Error al guardar perfil para {instance.username}: {str(e)}")
        raise
    
    