# Generated by Django 5.0.4 on 2024-05-25 21:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_remove_administrador_id_alter_administrador_perfil_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='perfil',
            name='tipo',
            field=models.CharField(max_length=20),
        ),
    ]
