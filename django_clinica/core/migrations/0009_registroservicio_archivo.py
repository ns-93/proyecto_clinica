# Generated by Django 5.1.2 on 2024-11-08 04:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_registroservicio_observacion'),
    ]

    operations = [
        migrations.AddField(
            model_name='registroservicio',
            name='archivo',
            field=models.FileField(blank=True, null=True, upload_to='archivos/'),
        ),
    ]
