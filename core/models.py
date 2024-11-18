from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.contrib.auth.models import Group
from django.utils import timezone
from django.dispatch import receiver
from django.db.models.signals import post_migrate
from django.contrib.auth.models import User
from django.conf import settings
from django.contrib.auth.hashers import make_password 

class Inventario(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    producto = models.CharField(max_length=100)
    cantidad = models.IntegerField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)

@receiver(post_migrate)
def create_roles(sender, **kwargs):
    roles = ['Mecánico', 'Recepcionista', 'Usuario', 'Administrador']
    for role in roles:
        Group.objects.get_or_create(name=role)


from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("El correo es obligatorio")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)

class UsuarioManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """Crea un usuario con un correo y contraseña."""
        if not email:
            raise ValueError('El correo es obligatorio')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """Crea un superusuario."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)
    
class Cliente(models.Model):
    rut = models.CharField(max_length=12, unique=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20)
    email = models.EmailField(default="No info")
    direccion = models.CharField(max_length=255, blank=True, null=True)
    contraseña = models.CharField(max_length=255,null=True,  # Add this temporarily
        blank=True)  # Campo de contraseña
    usuario = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,  # Add this temporarily
        blank=True 
        # ... any other fields you have
    )

    def save(self, *args, **kwargs):
        # Si la contraseña es proporcionada, se cifra antes de guardarla
        if self.contraseña:
            self.contraseña = make_password(self.contraseña)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.nombre} {self.apellido}"
    
class OrdenTrabajo(models.Model):
    ESTADOS = [
        ('Pendiente', 'Pendiente'),
        ('En Proceso', 'En Proceso'),
        ('Completado', 'Completado'),
    ]
    
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, to_field='rut')
    fecha = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='Pendiente')
    descripcion = models.TextField()

    def __str__(self):
        return f"Orden #{self.id} - {self.cliente}"

class Usuario(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    nombre = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20)
    direccion = models.TextField()
    rut = models.CharField(max_length=12, unique=True, null=True, blank=True)
    rol = models.CharField(
        max_length=50,
        choices=[('mecanico', 'Mecanico'), ('recepcionista', 'Recepcionista'),
                 ('usuario', 'Usuario'), ('administrador', 'Administrador')],
        default='usuario'
    )
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UsuarioManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nombre']

    def __str__(self):
        return self.email


class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    cantidad = models.IntegerField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.nombre

class Reserva(models.Model):
    HORARIOS = [
        ('09:00', '09:00'),
        ('10:00', '10:00'),
        ('11:00', '11:00'),
        ('12:00', '12:00'),
        ('14:00', '14:00'),
        ('15:00', '15:00'),
        ('16:00', '16:00'),
        ('17:00', '17:00'),
    ]

    cliente = models.ForeignKey('Cliente', on_delete=models.CASCADE)
    fecha = models.DateField()
    hora = models.CharField(max_length=5, choices=HORARIOS)
    descripcion_servicio = models.TextField()
    marca_vehiculo = models.CharField(max_length=100)
    modelo_vehiculo = models.CharField(max_length=100)
    ano_vehiculo = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['fecha', 'hora']  # Evita reservas duplicadas