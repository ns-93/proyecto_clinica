# Generated by Django 5.1.2 on 2024-11-08 02:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_servicios_status_alter_servicios_description_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='infocliente',
            name='imagen',
        ),
        migrations.AddField(
            model_name='infocliente',
            name='archivo',
            field=models.FileField(blank=True, null=True, upload_to='archivos/', verbose_name='Archivo'),
        ),
    ]