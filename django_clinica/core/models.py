from django.db import models
from django.contrib.auth.models import User

# Create your models here.

#servicios aka definiremos el servicio que ofreceremos o alguna otra acitividad que se requiera

class Servicios(models.Model):
    name= models.CharField(max_length=100, verbose_name='Nombre del Servicio')
    description= models.TextField(blank=True, null=True, verbose_name='Descripcion')
    profesional= models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'groups__name':'profesionales'},verbose_name='Profesional')
    n_procedimientos = models.PositiveIntegerField(default=0, verbose_name='Numero de sesiones')

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name= 'servicio'
        verbose_name_plural= 'servicios'

#hasta aqui llega el punto de servicios


#solicitud de servicios aqui permitiremos que el cliente haga solicitud de algun servicio que creamos antes

#solicitud de servicio o registro de servicio

class RegistroServicio(models.Model):
    servicio = models.ForeignKey( Servicios, on_delete=models.CASCADE, verbose_name= 'Servicio')
    cliente = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cliente_registrado' ,limit_choices_to={'groups__name':'clientes'},verbose_name='cliente')
    enabled = models.BooleanField(default=True, verbose_name='Habilitado')

    def __str__(self):
        return f'{self.cliente.username} - {self.servicio}'
    
    class Meta:
        verbose_name= 'solicitud de servicio'
        verbose_name_plural= 'solicitudes de servicios'

#hasta aqui el registro o solicitudes de servicio        

#aqui realizaremos la asistencia para verificar que el cliente cumplio con las citas al procedimiento o servicio
#osea ejemplo el servicio son 10 asistencia pediante este prpoceso podremos verificar que el paciente asistio a esos 10 procedimientos

#asistencia

class Asistencia(models.Model):
    servicio = models.ForeignKey( Servicios, on_delete=models.CASCADE, verbose_name= 'Servicio')
    cliente = models.ForeignKey(User, on_delete=models.CASCADE, related_name='asistencias' ,limit_choices_to={'groups__name':'clientes'},verbose_name='cliente')
    date= models.DateField(null=True, blank=True, verbose_name='Fecha')
    present = models.BooleanField(default=False, blank=True, null=True, verbose_name='Asistido')

    def __str__(self):
        return f'Asistencia {self.id}'
    
    class Meta:
        verbose_name= 'Asistencia'
        verbose_name_plural= 'Asisitencias'

    #hasta aqui la asistencia a procedimientos


#aqui realizaremo una clase que nos premitira agregar documentos y observaciones para nuetro cliente en su procedimiento solicitado

class infocliente(models.Model):
    servicio = models.ForeignKey(Servicios, on_delete=models.CASCADE, verbose_name='Servicio')
    cliente = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'groups__name': 'clientes'}, verbose_name='Cliente')
    
    # Campo para que el profesional ingrese una observación de texto
    observacion = models.TextField(null=True, blank=True, verbose_name='Observación')
    
    # Campo para que el profesional suba una imagen
    imagen = models.ImageField(upload_to='imagenes/', null=True, blank=True, verbose_name='Imagen')
    
    # Campo para subir el archivo de odontograma
    odontograma = models.FileField(upload_to='odontogramas/', null=True, blank=True, verbose_name='Odontograma')

    def __str__(self):
        return str(self.servicio)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Registro'
        verbose_name_plural = 'Registros'
#agregar otro campo para el odontograma y dejar el campo que esta para que pueda subir documento relacionados con el paciente
#hasta aqui llega esto
