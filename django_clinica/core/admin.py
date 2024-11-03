from django.contrib import admin
from .models import Servicios, RegistroServicio, Asistencia, infocliente

# Register your models here.
#refistramos la clase servicios admin y como se listara
class ServiciosAdmin(admin.ModelAdmin):
    list_display= ('name', 'profesional', 'n_procedimientos',)
    list_filter= ('profesional',)

admin.site.register(Servicios, ServiciosAdmin)

#para el rel registro o solicitud de servicios

class RegistroServicioAdmin(admin.ModelAdmin):
    list_display= ('servicio','cliente', 'enabled')
    list_filter = ('servicio', 'cliente', 'enabled')

admin.site.register(RegistroServicio, RegistroServicioAdmin)


#para las asistencias

class AsistenciaAdmin(admin.ModelAdmin):
    list_display= ('servicio','cliente', 'date' ,'present')
    list_filter = ('servicio', 'cliente', 'date' , 'present')

admin.site.register(Asistencia, AsistenciaAdmin)

#para la info cliente


class InfoclienteAdmin(admin.ModelAdmin):
    list_display = ('servicio', 'cliente', 'observacion', 'imagen', 'odontograma')
    search_fields = ('cliente__username', 'servicio__nombre')
    list_filter = ('servicio',)
    ordering = ('cliente',)

    fieldsets = (
        (None, {
            'fields': ('servicio', 'cliente', 'observacion')
        }),
        ('Archivos', {
            'fields': ('imagen', 'odontograma')
        }),
    )

admin.site.register(infocliente, InfoclienteAdmin)

#