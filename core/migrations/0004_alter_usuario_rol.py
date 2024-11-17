# Generated by Django 5.0.6 on 2024-11-17 22:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_alter_usuario_rol'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuario',
            name='rol',
            field=models.CharField(choices=[('mecanico', 'Mecanico'), ('recepcionista', 'Recepcionista'), ('usuario', 'Usuario'), ('administrador', 'Administrador')], default='usuario', max_length=50),
        ),
    ]