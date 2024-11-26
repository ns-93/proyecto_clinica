from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import  post_save, post_delete
from django.dispatch import  receiver
from django.utils.timezone import now
# Create your models here.

#servicios aka definiremos el servicio que ofreceremos o alguna otra acitividad que se requiera

# Modelo de servicios con estados
# Modelo para gestionar servicios y su estado

class Servicios(models.Model):
    STATUS_CHOICES = [
        ('S', 'Solicitado'),
        ('A', 'Aprobado'),
        ('R', 'Rechazado'),
        ('C', 'Completado')
    ]

    name = models.CharField(
        max_length=100, 
        verbose_name='Nombre',
        validators=[
            MinLengthValidator(3, 'El nombre debe tener al menos 3 caracteres')
        ]
    )

    description = models.TextField(
        verbose_name='Descripción',
        blank=True,
        validators=[
            MinLengthValidator(10, 'La descripción debe tener al menos 10 caracteres')
        ]
    )

    profesional = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        limit_choices_to={'groups__name': 'profesionales'},
        verbose_name='Profesional',
        related_name='servicios_profesional'
    )

    cliente = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={'groups__name': 'clientes'},
        verbose_name='Cliente',
        null=True,
        blank=True,
        related_name='servicios_cliente'
    )

    n_procedimientos = models.PositiveIntegerField(
        default=0,
        verbose_name='Número de sesiones',
        validators=[
            MinValueValidator(1, 'Debe haber al menos 1 procedimiento')
        ]
    )

    status = models.CharField(
        max_length=1,
        choices=STATUS_CHOICES,
        default='S',
        verbose_name='Estado'
    )

    def clean(self):
        # Validar que el profesional pertenece al grupo correcto
        if not self.profesional.groups.filter(name='profesionales').exists():
            raise ValidationError({
                'profesional': 'El usuario seleccionado no es un profesional'
            })

        # Validar que el cliente pertenece al grupo correcto
        if self.cliente and not self.cliente.groups.filter(name='clientes').exists():
            raise ValidationError({
                'cliente': 'El usuario seleccionado no es un cliente'
            })

        # Validar estado según condiciones
        if self.status == 'C' and not self.cliente:
            raise ValidationError({
                'status': 'No se puede marcar como completado sin un cliente asignado'
            })

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

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
    servicio = models.ForeignKey(
        Servicios, 
        on_delete=models.CASCADE,
        verbose_name='Servicio'
    )
    
    # Cliente que asiste al servicio
    cliente = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        verbose_name='Cliente'
    )
    
    # Fecha de la asistencia
    date = models.DateField(
        null=True, 
        blank=True,
        verbose_name='Fecha de asistencia'
    )
    
    # Indica si el cliente asistió o no
    present = models.BooleanField(
        null=True, 
        blank=True,
        verbose_name='¿Asistió?'
    )

    def __str__(self):
        return f"{self.cliente.username} - {self.servicio.name} - {self.date or 'Sin fecha'}"

    class Meta:
        verbose_name = 'asistencia'
        verbose_name_plural = 'asistencias'
        # Ordenar por fecha de asistencia
        ordering = ['date']
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
        return f"{self.cliente.username} - {self.servicio.name}"
    
    # Guarda la información en la base de datos
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Registro'
        verbose_name_plural = 'Registros'
#agregar otro campo para el odontograma y dejar el campo que esta para que pueda subir documento relacionados con el paciente
#hasta aqui llega esto

#modelo de odontograma
""""El odontograma esta creado para que los dientes estuvieran organizados dentro de un modelo Geométricos: donde se utilizan formas geométricas como círculos o cuadrados para representar las cuatro caras del diente des una vista por cuadrantes"""

class Mouth(models.Model):
    
    date = models.DateTimeField(default=now, editable=False)
    t_11 = models.CharField(max_length=90, default='sano')
    t_12 = models.CharField(max_length=90, default='sano')
    t_13 = models.CharField(max_length=90, default='sano')
    t_14 = models.CharField(max_length=90, default='sano')
    t_15 = models.CharField(max_length=90, default='sano')
    t_16 = models.CharField(max_length=90, default='sano')
    t_17 = models.CharField(max_length=90, default='sano')
    t_18 = models.CharField(max_length=90, default='sano')
    t_21 = models.CharField(max_length=90, default='sano')
    t_22 = models.CharField(max_length=90, default='sano')
    t_23 = models.CharField(max_length=90, default='sano')
    t_24 = models.CharField(max_length=90, default='sano')
    t_25 = models.CharField(max_length=90, default='sano')
    t_26 = models.CharField(max_length=90, default='sano')
    t_27 = models.CharField(max_length=90, default='sano')
    t_28 = models.CharField(max_length=90, default='sano')
    t_31 = models.CharField(max_length=90, default='sano')
    t_32 = models.CharField(max_length=90, default='sano')
    t_33 = models.CharField(max_length=90, default='sano')
    t_34 = models.CharField(max_length=90, default='sano')
    t_35 = models.CharField(max_length=90, default='sano')
    t_36 = models.CharField(max_length=90, default='sano')
    t_37 = models.CharField(max_length=90, default='sano')
    t_38 = models.CharField(max_length=90, default='sano')
    t_41 = models.CharField(max_length=90, default='sano')
    t_42 = models.CharField(max_length=90, default='sano')
    t_43 = models.CharField(max_length=90, default='sano')
    t_44 = models.CharField(max_length=90, default='sano')
    t_45 = models.CharField(max_length=90, default='sano')
    t_46 = models.CharField(max_length=90, default='sano')
    t_47 = models.CharField(max_length=90, default='sano')
    t_48 = models.CharField(max_length=90, default='sano')
    t_51 = models.CharField(max_length=90, default='sano')
    t_52 = models.CharField(max_length=90, default='sano')
    t_53 = models.CharField(max_length=90, default='sano')
    t_54 = models.CharField(max_length=90, default='sano')
    t_55 = models.CharField(max_length=90, default='sano')
    t_61 = models.CharField(max_length=90, default='sano')
    t_62 = models.CharField(max_length=90, default='sano')
    t_63 = models.CharField(max_length=90, default='sano')
    t_64 = models.CharField(max_length=90, default='sano')
    t_65 = models.CharField(max_length=90, default='sano')
    t_71 = models.CharField(max_length=90, default='sano')
    t_72 = models.CharField(max_length=90, default='sano')
    t_73 = models.CharField(max_length=90, default='sano')
    t_74 = models.CharField(max_length=90, default='sano')
    t_75 = models.CharField(max_length=90, default='sano')
    t_81 = models.CharField(max_length=90, default='sano')
    t_82 = models.CharField(max_length=90, default='sano')
    t_83 = models.CharField(max_length=90, default='sano')
    t_84 = models.CharField(max_length=90, default='sano')
    t_85 = models.CharField(max_length=90, default='sano')

#hasa aqui llega el modelo de odontograma

class HorarioDisponible(models.Model):
    dia = models.DateField()
    hora = models.TimeField()
    disponible = models.BooleanField(default=True)

class Reserva(models.Model):
    profesional = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'groups__name': 'profesionales'}, verbose_name='Profesional', related_name='reservas_profesional')
    cliente = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'groups__name': 'clientes'}, verbose_name='Cliente', null=True, blank=True, related_name='reservas_cliente')
    fecha = models.DateField(verbose_name='Fecha de la Reserva')
    hora = models.TimeField(verbose_name='Hora de la Reserva')
    pagada = models.BooleanField(default=False, verbose_name='Pagada')

    def __str__(self):
        return f"{self.profesional.get_full_name()} - {self.fecha} {self.hora}"

    class Meta:
        verbose_name = 'reserva'
        verbose_name_plural = 'reservas'
        unique_together = ('profesional', 'fecha', 'hora')
        
#modelo de preguntas y respuestas

class Question(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class Answer(models.Model):
    question = models.OneToOneField(Question, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class About(models.Model):
    mission = models.TextField(verbose_name='Misión')
    vision = models.TextField(verbose_name='Visión')
    values = models.TextField(verbose_name='Valores')
    contact_info = models.TextField(verbose_name='Información de Contacto')
    email = models.EmailField(verbose_name='Email', null=True, blank=True)
    address = models.CharField(max_length=255, verbose_name='Dirección', null=True, blank=True)
    phone = models.CharField(max_length=20, verbose_name='Teléfono', null=True, blank=True)
    images = models.ImageField(upload_to='about_images/', null=True, blank=True, verbose_name='Imágenes')

    def __str__(self):
        return "Acerca de Dental Knights"

    class Meta:
        verbose_name = 'Acerca de'
        verbose_name_plural = 'Acerca de'



#modelo consultas
class Consulta(models.Model):
    ESTADO_CHOICES = [
        ('disponible', 'Disponible'),
        ('vendida', 'Vendida'),
        ('cancelada', 'Cancelada')
    ]
    
    ESTADO_PAGO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('completado', 'Completado'),
        ('fallido', 'Fallido')
    ]

    # Campos existentes
    nombre_completo = models.CharField(max_length=255)
    rut = models.CharField(max_length=12)
    telefono = models.CharField(max_length=12)
    email = models.EmailField()
    fecha = models.DateField(default=now)
    hora = models.TimeField(default=now)
    profesional = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        limit_choices_to={'groups__name': 'profesionales'}, 
        verbose_name='Profesional'
    )
    precio = models.DecimalField(max_digits=10, decimal_places=2, default=50000)
    
    # Campos de pago y estado
    pagada = models.BooleanField(default=False)
    preference_id = models.CharField(max_length=255, null=True, blank=True)
    payment_id = models.CharField(max_length=255, null=True, blank=True)
    estado_pago = models.CharField(
        max_length=20, 
        choices=ESTADO_PAGO_CHOICES,
        default='pendiente'
    )
    
    # Nuevos campos
    estado = models.CharField(
        max_length=20, 
        choices=ESTADO_CHOICES,
        default='disponible'
    )
    comprador = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL,
        null=True, 
        blank=True,
        related_name='consultas_compradas'
    )
    fecha_compra = models.DateTimeField(null=True, blank=True)
    
    def marcar_como_vendida(self, user):
        self.estado = 'vendida'
        self.comprador = user
        self.fecha_compra = timezone.now()
        self.save()
    
    def __str__(self):
        return f"Consulta {self.id} - {self.nombre_completo} - {self.fecha}"
    
    class Meta:
        ordering = ['-fecha', '-hora']
        verbose_name = 'Consulta'
        verbose_name_plural = 'Consultas'