from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import RegistroServicio, Asistencia, Infocliente


@receiver(post_save, sender=RegistroServicio)
def create_client_info(sender, instance, created, **kwargs):
    # Verifica si se creó un nuevo registro de servicio
    if created:
        # Crea un registro en Infocliente para almacenar información adicional del cliente
        Infocliente.objects.create(
            servicio=instance.servicio,    # El servicio asociado a la solicitud
            cliente=instance.cliente,      # El cliente que hizo la solicitud
            observacion=None,              # Observación del profesional (puede ser rellenada después)
            archivo=None,                  # Campo para cargar cualquier archivo relacionado (vacío por defecto)
            odontograma=None               # Archivo odontograma (vacío por defecto)
        )

@receiver(post_save, sender=RegistroServicio)
def create_asistencia_records(sender, instance, created, **kwargs):
    # Verifica si se creó un nuevo registro de servicio
    if created:
        # Crea registros de asistencia para cada sesión del servicio solicitado
        for i in range(1, instance.servicio.n_procedimientos + 1):
            Asistencia.objects.create(
                servicio=instance.servicio,
                cliente=instance.cliente,
                date=None,  # Asigna la fecha de la sesión o déjala en blanco para llenarla luego
                present=None  # Asigna la asistencia al cliente como no registrada inicialmente
            )

