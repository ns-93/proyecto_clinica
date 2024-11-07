from django.contrib import admin
from .models import Profile

# Register your models here.
#perfiles detallados
# Configuración de la interfaz de administración para el modelo Profile
class ProfileAdmin(admin.ModelAdmin):
    # Define las columnas que se mostrarán en la lista de objetos Profile
    list_display = ('user', 'address', 'location', 'telephone', 'user_group')
    # Define los campos por los que se puede buscar en la interfaz de administración
    # Permite búsqueda por ubicación, nombre de usuario y nombre del grupo de usuarios
    search_fields = ('location', 'user__username', 'user__groups__name')
    # Agrega filtros en la barra lateral para filtrar por grupo de usuario y ubicación
    list_filter = ('user__groups', 'location')

    # Método personalizado para mostrar los grupos de usuario del perfil en una sola columna
    # Combina y muestra los nombres de los grupos a los que pertenece el usuario, separados por guiones
    def user_group(self, obj):
        return "-".join([t.name for t in obj.user.groups.all().order_by('name')])
    # Etiqueta que aparecerá en la interfaz de administración para la columna generada por user_group
    user_group.short_description = 'Grupo' 
# Registra el modelo Profile en el sitio de administración, usando la configuración personalizada ProfileAdmin
admin.site.register(Profile, ProfileAdmin)