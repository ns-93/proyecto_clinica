# Generated by Django 5.1.2 on 2024-11-04 15:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(default='usuario_defecto.jpg', upload_to='users/', verbose_name='Imagen de perfil'),
        ),
    ]
