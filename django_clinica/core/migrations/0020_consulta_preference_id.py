# Generated by Django 5.1.2 on 2024-11-24 07:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0019_remove_consulta_horario_consulta_fecha_consulta_hora'),
    ]

    operations = [
        migrations.AddField(
            model_name='consulta',
            name='preference_id',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]