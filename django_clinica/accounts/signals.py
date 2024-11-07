

from django.contrib.auth.models import Group
from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import Profile

#en este archivo configuramos la accionacion automatica de grupos de usuarios segun su rol

# Función que se ejecuta automáticamente después de guardar una instancia de Profile
# Añade al usuario asociado al perfil recién creado al grupo 'clientes'
@receiver(post_save, sender=Profile)
def add_user_to_clientes_group(sender, instance, created, **kwargs):
    # Solo ejecuta el bloque si el perfil fue creado (no actualizado)
    if created:
        try:
            # Intenta obtener el grupo 'clientes'
            group1= Group.objects.get(name='clientes')
        except Group.DoesNotExist:
            # Si el grupo 'clientes' no existe, lo crea junto con otros grupos predeterminados
            group1= Group.objects.create(name='clientes')
            group2= Group.objects.create(name='profesionales')
            group3= Group.objects.create(name='ejecutivos')
            group4= Group.objects.create(name='administradores')
        instance.user.groups.add(group1)


        