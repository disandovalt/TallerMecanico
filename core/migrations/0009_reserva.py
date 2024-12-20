# Generated by Django 5.0.6 on 2024-11-18 06:36

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_cliente_usuario'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reserva',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateField()),
                ('hora', models.CharField(choices=[('09:00', '09:00'), ('10:00', '10:00'), ('11:00', '11:00'), ('12:00', '12:00'), ('14:00', '14:00'), ('15:00', '15:00'), ('16:00', '16:00'), ('17:00', '17:00')], max_length=5)),
                ('descripcion_servicio', models.TextField()),
                ('marca_vehiculo', models.CharField(max_length=100)),
                ('modelo_vehiculo', models.CharField(max_length=100)),
                ('ano_vehiculo', models.IntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.cliente')),
            ],
            options={
                'unique_together': {('fecha', 'hora')},
            },
        ),
    ]
