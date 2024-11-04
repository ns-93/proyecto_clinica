from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

# Create your models here.
# Creacion perfiles de usuarios

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile', verbose_name='Usuario')
    image = models.ImageField(default='usuario_defecto.jpg', upload_to='users/', verbose_name='Imagen de perfil')
    address = models.CharField(max_length=150, null=True, blank=True, verbose_name='Direccion')
    location = models.CharField(max_length=100, null=True, blank=True, verbose_name='Localidad')
    telephone = models.CharField(max_length=20, null=True, blank=True, verbose_name='telefono')


    class Meta:
        verbose_name= 'perfil'
        verbose_name_plural= 'perfiles'
        ordering = ['-id'] #con este punto nos ordara los perfiles por el perfil mas reciente creado

    def __str__(self):
        return self.user.username
    

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

post_save.connect(create_user_profile, sender=User)
post_save.connect(save_user_profile, sender=User)
      
