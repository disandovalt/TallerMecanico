from django.db import models
from django.contrib.auth.models import Group
from django.utils import timezone
from django.dispatch import receiver
from django.db.models.signals import post_migrate

class Cliente(models.Model):
    rut = models.CharField(max_length=12, unique=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20)
    email = models.EmailField(default="No info")
    direccion = models.CharField(max_length=255, blank=True, null=True) 

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

class OrdenTrabajo(models.Model):
    ESTADOS = [
        ('Pendiente', 'Pendiente'),
        ('En Proceso', 'En Proceso'),
        ('Completado', 'Completado'),
    ]
    
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, to_field='rut')
    fecha = models.DateTimeField(auto_now_add=True)  # Este es el campo que tienes
    estado = models.CharField(max_length=20, choices=ESTADOS, default='Pendiente')
    descripcion = models.TextField()

    def __str__(self):
        return f"Orden #{self.id} - {self.cliente}"

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
        if not email:
            raise ValueError('El email es obligatorio')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class Usuario(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    nombre = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20)
    direccion = models.TextField()
    rol = models.CharField(
        max_length=50,
        choices=[('mecanico', 'Mecanico'), ('recepcionista', 'Recepcionista'), ('usuario', 'Usuario'), ('administrador', 'Administrador')],
        default='usuario'
    )
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UsuarioManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nombre']

    def __str__(self):
        return self.email
    
