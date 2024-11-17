from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.db import transaction
from .models import Cliente, OrdenTrabajo, Inventario

def setup_roles_and_permissions():
    with transaction.atomic():
        # Crear permisos personalizados para cada modelo
        cliente_content_type = ContentType.objects.get_for_model(Cliente)
        orden_trabajo_content_type = ContentType.objects.get_for_model(OrdenTrabajo)
        inventario_content_type = ContentType.objects.get_for_model(Inventario)

        # Permisos para Mecánicos
        mecanico_group, _ = Group.objects.get_or_create(name='Mecánico')
        mecanico_permissions = [
            # Permisos para OrdenTrabajo
            Permission.objects.get_or_create(
                codename='view_ordentrabajo',
                name='Can view orden trabajo',
                content_type=orden_trabajo_content_type,
            )[0],
            Permission.objects.get_or_create(
                codename='change_ordentrabajo',
                name='Can change orden trabajo',
                content_type=orden_trabajo_content_type,
            )[0],
            # Permisos para Inventario
            Permission.objects.get_or_create(
                codename='view_inventario',
                name='Can view inventario',
                content_type=inventario_content_type,
            )[0],
            Permission.objects.get_or_create(
                codename='change_inventario',
                name='Can change inventario',
                content_type=inventario_content_type,
            )[0],
        ]
        mecanico_group.permissions.set(mecanico_permissions)

        # Permisos para Recepcionistas
        recepcionista_group, _ = Group.objects.get_or_create(name='Recepcionista')
        recepcionista_permissions = [
            # Permisos para Cliente
            Permission.objects.get_or_create(
                codename='add_cliente',
                name='Can add cliente',
                content_type=cliente_content_type,
            )[0],
            Permission.objects.get_or_create(
                codename='view_cliente',
                name='Can view cliente',
                content_type=cliente_content_type,
            )[0],
            Permission.objects.get_or_create(
                codename='change_cliente',
                name='Can change cliente',
                content_type=cliente_content_type,
            )[0],
            # Permisos para OrdenTrabajo
            Permission.objects.get_or_create(
                codename='add_ordentrabajo',
                name='Can add orden trabajo',
                content_type=orden_trabajo_content_type,
            )[0],
            Permission.objects.get_or_create(
                codename='view_ordentrabajo',
                name='Can view orden trabajo',
                content_type=orden_trabajo_content_type,
            )[0],
            # Permisos para Inventario
            Permission.objects.get_or_create(
                codename='view_inventario',
                name='Can view inventario',
                content_type=inventario_content_type,
            )[0],
        ]
        recepcionista_group.permissions.set(recepcionista_permissions)

# Decorador para verificar permisos por rol
from django.contrib.auth.decorators import user_passes_test

def role_required(roles):
    def check_role(user):
        if user.is_superuser:
            return True
        return user.groups.filter(name__in=roles).exists()
    return user_passes_test(check_role)