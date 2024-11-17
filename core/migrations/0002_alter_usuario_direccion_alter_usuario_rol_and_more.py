# Generated by Django 5.0.6 on 2024-11-17 21:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuario',
            name='direccion',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='usuario',
            name='rol',
            field=models.CharField(choices=[('admin', 'Admin'), ('usuario', 'Usuario')], default='usuario', max_length=50),
        ),
        migrations.AlterField(
            model_name='usuario',
            name='telefono',
            field=models.CharField(max_length=20),
        ),
    ]
