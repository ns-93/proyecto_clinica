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
    # Relación con el modelo Servicios, indica el servicio que se solicita
    servicio = models.ForeignKey(Servicios, on_delete=models.CASCADE, verbose_name='Servicio')
    
    # Relación con el modelo User, limitado al grupo "clientes", indica qué cliente solicita el servicio
    cliente = models.ForeignKey(
        User,
        on_delete=models.CASCADE,  # Si el cliente se elimina, también se elimina la solicitud
        related_name='cliente_registrado',  # Relaciona la solicitud con el cliente
        limit_choices_to={'groups__name': 'clientes'},  # Limita los clientes a aquellos que están en el grupo "clientes"
        verbose_name='cliente'
    )
    
    # Campo booleano que indica si la solicitud de servicio está habilitada o no
    enabled = models.BooleanField(default=True, verbose_name='Habilitado')
    
    # Nuevo campo de observación para que el cliente o profesional pueda agregar notas adicionales a la solicitud
    observacion = models.TextField(null=True, blank=True, verbose_name='Observación')
    archivo = models.FileField(upload_to='archivos/', null=True, blank=True)
    odontograma = models.ImageField(upload_to='odontogramas/', null=True, blank=True)

    # Método para representar la solicitud en formato de texto, mostrando el nombre de usuario del cliente y el servicio
    def __str__(self):
        return f'{self.cliente.username} - {self.servicio}'

    # Configuración adicional para el modelo en el administrador de Django
    class Meta:
        # Nombre en singular para el modelo
        verbose_name = 'solicitud de servicio'
        # Nombre plural para el modelo
        verbose_name_plural = 'solicitudes de servicios'

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
class Infocliente(models.Model):
    # Servicio asociado a la información del cliente
    servicio = models.ForeignKey(Servicios, on_delete=models.CASCADE, verbose_name='Servicio')
    # Cliente para el que se registra la información, limitado al grupo "clientes"
    cliente = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'groups__name': 'clientes'}, verbose_name='Cliente')
    
    # Observación o nota que el profesional puede agregar
    observacion = models.TextField(null=True, blank=True, verbose_name='Observación')
    
    # Campo para que el profesional suba una Imagen relacionada con el servicio, como un documento visual adicional
    archivo = models.FileField(upload_to='archivos/', null=True, blank=True, verbose_name='Archivo')
    
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

