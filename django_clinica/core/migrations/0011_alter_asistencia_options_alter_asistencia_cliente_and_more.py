# Generated by Django 5.1.2 on 2024-11-11 03:59

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_registroservicio_odontograma'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='asistencia',
            options={'ordering': ['date'], 'verbose_name': 'asistencia', 'verbose_name_plural': 'asistencias'},
        ),
        migrations.AlterField(
            model_name='asistencia',
            name='cliente',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Cliente'),
        ),
        migrations.AlterField(
            model_name='asistencia',
            name='date',
            field=models.DateField(blank=True, null=True, verbose_name='Fecha de asistencia'),
        ),
        migrations.AlterField(
            model_name='asistencia',
            name='present',
            field=models.BooleanField(blank=True, null=True, verbose_name='¿Asistió?'),
        ),
    ]
