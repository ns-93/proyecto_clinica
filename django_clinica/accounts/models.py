from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

# Create your models here.
# Creacion perfiles de usuarios
# Creación de modelos para la aplicación
# Definición del modelo Profile para perfiles de usuarios

class Profile(models.Model):
    # Relación uno a uno con el modelo de usuario de Django, eliminando el perfil si se elimina el usuario
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile', verbose_name='Usuario')
    # Campo de imagen para el perfil de usuario; almacena la imagen en la carpeta 'users/' y usa una imagen por defecto si no se carga ninguna
    image = models.ImageField(default='users/usuario_defecto.jpg', upload_to='users/', verbose_name='Imagen de perfil')
    # Campos de texto para la dirección del usuario, localidad y telefono; es opcional
    address = models.CharField(max_length=150, null=True, blank=True, verbose_name='Direccion')
    location = models.CharField(max_length=100, null=True, blank=True, verbose_name='Localidad')
    telephone = models.CharField(max_length=20, null=True, blank=True, verbose_name='telefono')

    # Configuración de metadatos del modelo
    class Meta:
        
        verbose_name= 'perfil' # Nombre en singular para mostrar en el panel de administración
        verbose_name_plural= 'perfiles' # Nombre en plural para mostrar en el panel de administración
        ordering = ['-id'] # Ordena los perfiles de forma descendente por el ID, mostrando los más recientes primero
    
    # Representación en texto de cada instancia del modelo, retornando el nombre de usuario
    def __str__(self):
        return self.user.username
    
# Función para crear un perfil automáticamente al crear un usuario
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

# Función para guardar el perfil de usuario al guardar el usuario
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

# Conecta las señales post_save al modelo User para crear y guardar perfiles automáticamente
post_save.connect(create_user_profile, sender=User)
post_save.connect(save_user_profile, sender=User)
      
