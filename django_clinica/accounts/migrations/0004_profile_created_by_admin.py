# Generated by Django 5.1.2 on 2024-11-17 03:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_alter_profile_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='created_by_admin',
            field=models.BooleanField(blank=True, default=True, null=True, verbose_name='Creado por Admin'),
        ),
    ]
