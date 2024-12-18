# Generated by Django 5.1.2 on 2024-11-25 23:26

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0021_alter_consulta_telefono'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='consulta',
            options={'ordering': ['-fecha', '-hora'], 'verbose_name': 'Consulta', 'verbose_name_plural': 'Consultas'},
        ),
        migrations.AddField(
            model_name='consulta',
            name='comprador',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='consultas_compradas', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='consulta',
            name='estado',
            field=models.CharField(choices=[('disponible', 'Disponible'), ('vendida', 'Vendida'), ('cancelada', 'Cancelada')], default='disponible', max_length=20),
        ),
        migrations.AddField(
            model_name='consulta',
            name='estado_pago',
            field=models.CharField(choices=[('pendiente', 'Pendiente'), ('completado', 'Completado'), ('fallido', 'Fallido')], default='pendiente', max_length=20),
        ),
        migrations.AddField(
            model_name='consulta',
            name='fecha_compra',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='consulta',
            name='payment_id',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
