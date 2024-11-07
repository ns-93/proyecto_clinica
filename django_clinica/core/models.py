from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import  post_save, post_delete
from django.dispatch import  receiver

# Create your models here.

#servicios aka definiremos el servicio que ofreceremos o alguna otra acitividad que se requiera

# Modelo de servicios con estados
# Modelo para gestionar servicios y su estado
class Servicios(models.Model):
    # Opciones de estado del servicio
    STATUS_CHOICES = (
        ('S', 'Solicitud de Servicio'), # Servicio solicitado por el cliente
        ('P', 'En progreso'),           # Servicio en proceso de realización
        ('F', 'Finalizado'),            # Servicio completado
    )


    name = models.CharField(max_length=100, verbose_name='Nombre del Servicio') # Nombre del servicio
    description = models.TextField(blank=True, null=True, verbose_name='Descripción') # Descripción opcional del servicio
    profesional = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'groups__name': 'profesionales'}, verbose_name='Profesional') # Profesional asignado, relacionado con un usuario del grupo "profesionales"
    # Número de procedimientos o sesiones asociadas al servicio
    n_procedimientos = models.PositiveIntegerField(default=0, verbose_name='Número de sesiones') 
    # Estado del servicio, utilizando las opciones definidas en STATUS_CHOICES
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='S', verbose_name='Estado')


    def __str__(self):
        return self.name 
# Representación del servicio como su nombre
    class Meta:
        verbose_name = 'servicio'
        verbose_name_plural = 'servicios'

#hasta aqui llega el punto de servicios


#solicitud de servicios aqui permitiremos que el cliente haga solicitud de algun servicio que creamos antes

#solicitud de servicio o registro de servicio
# Modelo para registrar solicitudes de servicios por parte de los clientes
class RegistroServicio(models.Model):
    # Servicio solicitado por el cliente
    servicio = models.ForeignKey( Servicios, on_delete=models.CASCADE, verbose_name= 'Servicio')
    # Cliente que solicita el servicio, limitado al grupo "clientes"
    cliente = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cliente_registrado' ,limit_choices_to={'groups__name':'clientes'},verbose_name='cliente')
    # Campo para indicar si el servicio solicitado está habilitado
    enabled = models.BooleanField(default=True, verbose_name='Habilitado')

# Muestra cliente y servicio en la representación
    def __str__(self):
        return f'{self.cliente.username} - {self.servicio}'
    
    class Meta:
        verbose_name= 'solicitud de servicio'
        verbose_name_plural= 'solicitudes de servicios'

#hasta aqui el registro o solicitudes de servicio        

#aqui realizaremos la asistencia para verificar que el cliente cumplio con las citas al procedimiento o servicio
#osea ejemplo el servicio son 10 asistencia pediante este prpoceso podremos verificar que el paciente asistio a esos 10 procedimientos

#asistencia
# Modelo para registrar la asistencia del cliente a las sesiones del servicio
class Asistencia(models.Model):
    # Servicio al que asiste el cliente
    servicio = models.ForeignKey( Servicios, on_delete=models.CASCADE, verbose_name= 'Servicio')
    # Cliente que asiste a la sesión, limitado al grupo "clientes"
    cliente = models.ForeignKey(User, on_delete=models.CASCADE, related_name='asistencias' ,limit_choices_to={'groups__name':'clientes'},verbose_name='cliente')
    # Fecha de la asistencia
    date= models.DateField(null=True, blank=True, verbose_name='Fecha')
    # Campo booleano para indicar si el cliente asistió o no
    present = models.BooleanField(default=False, blank=True, null=True, verbose_name='Asistido')

# Muestra el ID de la asistencia
    def __str__(self):
        return f'Asistencia {self.id}'

    class Meta:
        verbose_name= 'Asistencia'
        verbose_name_plural= 'Asisitencias'

    #hasta aqui la asistencia a procedimientos


#aqui realizaremo una clase que nos premitira agregar documentos y observaciones para nuetro cliente en su procedimiento solicitado
# Modelo para almacenar información adicional del cliente relacionada con el servicio
class infocliente(models.Model):
    # Servicio asociado a la información del cliente
    servicio = models.ForeignKey(Servicios, on_delete=models.CASCADE, verbose_name='Servicio')
    # Cliente para el que se registra la información, limitado al grupo "clientes"
    cliente = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'groups__name': 'clientes'}, verbose_name='Cliente')
    
    # Observación o nota que el profesional puede agregar
    observacion = models.TextField(null=True, blank=True, verbose_name='Observación')
    
    # Campo para que el profesional suba una Imagen relacionada con el servicio, como un documento visual adicional
    imagen = models.ImageField(upload_to='imagenes/', null=True, blank=True, verbose_name='Imagen')
    
    # Archivo odontograma para registros dentales específicos del cliente
    odontograma = models.FileField(upload_to='odontogramas/', null=True, blank=True, verbose_name='Odontograma')

# Muestra el servicio asociado en la representación
    def __str__(self):
        return str(self.servicio)
    
# Guarda la información en la base de datos
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Registro'
        verbose_name_plural = 'Registros'
#agregar otro campo para el odontograma y dejar el campo que esta para que pueda subir documento relacionados con el paciente
#hasta aqui llega esto

