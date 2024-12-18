# Generated by Django 5.1.2 on 2024-11-26 02:22

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0022_alter_consulta_options_consulta_comprador_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registroservicio',
            name='archivo',
            field=models.FileField(blank=True, null=True, upload_to='archivos/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['pdf', 'doc', 'docx', 'jpg', 'jpeg', 'png'], message='Formato de archivo no soportado')]),
        ),
        migrations.AlterField(
            model_name='registroservicio',
            name='observacion',
            field=models.TextField(blank=True, null=True, validators=[django.core.validators.MinLengthValidator(10, 'La observación debe tener al menos 10 caracteres')], verbose_name='Observación'),
        ),
        migrations.AlterField(
            model_name='registroservicio',
            name='odontograma',
            field=models.ImageField(blank=True, null=True, upload_to='odontogramas/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'], message='Solo se permiten imágenes JPG o PNG')]),
        ),
        migrations.AlterField(
            model_name='servicios',
            name='description',
            field=models.TextField(blank=True, validators=[django.core.validators.MinLengthValidator(10, 'La descripción debe tener al menos 10 caracteres')], verbose_name='Descripción'),
        ),
        migrations.AlterField(
            model_name='servicios',
            name='n_procedimientos',
            field=models.PositiveIntegerField(default=0, validators=[django.core.validators.MinValueValidator(1, 'Debe haber al menos 1 procedimiento')], verbose_name='Número de sesiones'),
        ),
        migrations.AlterField(
            model_name='servicios',
            name='name',
            field=models.CharField(max_length=100, validators=[django.core.validators.MinLengthValidator(3, 'El nombre debe tener al menos 3 caracteres')], verbose_name='Nombre'),
        ),
        migrations.AlterField(
            model_name='servicios',
            name='status',
            field=models.CharField(choices=[('S', 'Solicitado'), ('A', 'Aprobado'), ('R', 'Rechazado'), ('C', 'Completado')], default='S', max_length=1, verbose_name='Estado'),
        ),
    ]
