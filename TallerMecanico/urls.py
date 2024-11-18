from django.contrib import admin
from django.urls import path
from core import views
from core.views import (
    ListarClientesView, 
    CrearClienteView, 
    EditarClienteView, 
    editar_cliente, 
    filtrar_clientes
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.login_view, name='login'),
    path('login/', views.login_view, name='login'),
    path('login/admin/', views.login_admin, name='login_admin'),
    path('admin_dashboards/', views.dashboard, name='admin_dashboards'),
    path('seleccion-rol/', views.seleccion_rol, name='seleccion_rol'),
    path('registrar_cliente/', views.registrar_cliente, name='registrar_cliente'),
    path('login_cliente/', views.login_cliente, name='login_cliente'),  
    
    path('listar_usuarios/', views.listar_usuarios, name='listar_usuarios'),
    path('crear_usuario/', views.crear_usuario, name='crear_usuario'),
    path('editar_usuario/<int:pk>/', views.editar_usuario, name='editar_usuario'),
    path('eliminar_usuario/<int:user_id>/', views.eliminar_usuario, name='eliminar_usuario'),

    # URLs para CRUD de Órdenes de Trabajo
    path('ordenes/', views.listar_ordenes, name='listar_ordenes'),
    path('ordenes/crear/', views.crear_orden_trabajo, name='crear_orden_trabajo'),
    path('ordenes/editar/<int:orden_id>/', views.editar_orden_trabajo, name='editar_orden'),
    path('ordenes/eliminar/<int:orden_id>/', views.eliminar_orden_trabajo, name='eliminar_orden'),

    # URLs para CRUD de Inventario
    path('listar_inventarios/', views.listar_inventarios, name='listar_inventarios'),
    path('crear_inventario/', views.crear_inventario, name='crear_inventario'),
    path('editar_inventario/<int:inventario_id>/', views.editar_inventario, name='editar_inventario'),
    path('eliminar_inventario/<int:inventario_id>/', views.eliminar_inventario, name='eliminar_inventario'),

    # URLs para Clientes
    path('clientes/', filtrar_clientes, name='listar_clientes'),  # Incluye filtro por RUT
    path('clientes/crear/', CrearClienteView.as_view(), name='crear_cliente'),
    path('clientes/eliminar/<str:rut>/', views.eliminar_cliente, name='eliminar_cliente'),
    path('clientes/editar/<str:rut>/', editar_cliente, name='editar_cliente'),

    path('login/', views.login_view, name='login'),
    path('mecanico/', views.mecanico_dashboard, name='mecanico_dashboard'),
    path('recepcionista/', views.recepcionista_dashboard, name='recepcionista_dashboard'),
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('usuario/', views.usuario_dashboard, name='usuario_dashboard'),

    path('reserva/', views.crear_reserva, name='crear_reserva'),
    path('mis-reservas/', views.ver_reservas, name='ver_reservas'),
]
