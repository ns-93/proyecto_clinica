from django.contrib import admin
from .models import Servicios, RegistroServicio, Asistencia, infocliente

# Register your models here.
#registramos la clase servicios admin y como se listara
# Configuración de la administración para el modelo Servicios
class ServiciosAdmin(admin.ModelAdmin):
    # Define las columnas que se mostrarán en la lista de objetos Servicios
    list_display= ('name', 'profesional', 'n_procedimientos',)
    # Añade un filtro lateral para buscar por el campo 'profesional'
    list_filter= ('profesional',)
# Registra el modelo Servicios en el panel de administración con la configuración personalizada
admin.site.register(Servicios, ServiciosAdmin)

#para el rel registro o solicitud de servicios
# Configuración de la administración para el modelo RegistroServicio
class RegistroServicioAdmin(admin.ModelAdmin):
    # Define las columnas que se mostrarán en la lista de objetos RegistroServicio
    list_display= ('servicio','cliente', 'enabled')
    # Añade filtros laterales para buscar por 'servicio', 'cliente' y 'enabled'(habilitado)
    list_filter = ('servicio', 'cliente', 'enabled')
# Registra el modelo RegistroServicio en el panel de administración con la configuración personalizada
admin.site.register(RegistroServicio, RegistroServicioAdmin)


#para las asistencias
# Configuración de la administración para el modelo Asistencia(registra la asistencia de los paciente a sus tratamientos)
class AsistenciaAdmin(admin.ModelAdmin):
    # Define las columnas que se mostrarán en la lista de objetos Asistencia
    list_display= ('servicio','cliente', 'date' ,'present')
    # Añade filtros laterales para buscar por 'servicio', 'cliente', 'date' y 'present'
    list_filter = ('servicio', 'cliente', 'date' , 'present')
# Registra el modelo Asistencia en el panel de administración con la configuración personalizada
admin.site.register(Asistencia, AsistenciaAdmin)

#para la info cliente
# Configuración de la administración para el modelo Infocliente

class InfoclienteAdmin(admin.ModelAdmin):
    # Define las columnas que se mostrarán en la lista de objetos Infocliente
    list_display = ('servicio', 'cliente', 'observacion', 'imagen', 'odontograma')
    # Añade una barra de búsqueda que permite buscar por nombre de usuario del cliente y nombre del servicio
    search_fields = ('cliente__username', 'servicio__nombre') 
    # Añade un filtro lateral para buscar por el campo 'servicio'
    list_filter = ('servicio',)
    # Define el orden de los objetos por el campo 'cliente'
    ordering = ('cliente',)
    # Define la estructura de los campos en la vista de edición de Infocliente en la administración
    fieldsets = (
        (None, {
            'fields': ('servicio', 'cliente', 'observacion')
        }),
        ('Archivos', {
            'fields': ('imagen', 'odontograma')
        }),
    )
# Registra el modelo Infocliente en el panel de administración con la configuración personalizada
admin.site.register(infocliente, InfoclienteAdmin)

#