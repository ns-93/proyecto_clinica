# Generated by Django 5.1.2 on 2024-11-23 21:33

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0016_about_address_about_email_about_phone'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='servicios',
            name='cliente',
            field=models.ForeignKey(blank=True, limit_choices_to={'groups__name': 'clientes'}, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='servicios_cliente', to=settings.AUTH_USER_MODEL, verbose_name='Cliente'),
        ),
        migrations.AlterField(
            model_name='servicios',
            name='profesional',
            field=models.ForeignKey(limit_choices_to={'groups__name': 'profesionales'}, on_delete=django.db.models.deletion.CASCADE, related_name='servicios_profesional', to=settings.AUTH_USER_MODEL, verbose_name='Profesional'),
        ),
    ]